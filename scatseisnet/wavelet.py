"""Wavelet class and functions.

Copyright (C) 2023 Léonard Seydoux

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <https://www.gnu.org/licenses/>.
"""

try:
    import cupy as xp
except:
    import numpy as xp

from scipy.signal import tukey


def gaussian_window(x, width):
    """Gaussian window.

    This function can generate a bank of windows at once if the width
    argument is a vector (and/or amplitude). In this case, it should have
    a new axis with respect to the time vector to allow for outer product.

    Parameters
    ----------
    x : :class:`T.ndarray` or np.ndarray
        Input variable (in the same units than the width).
    width : float or np.ndarray
        Window width (in the same units than the input variable). If an array
        is provided, the function returns as many windows as the number of
        elements of this parameter.
    amplitude : float or np.ndarray, optional
        Window amplitude at maximum (default 1). If this parameter is a vector,
        it should have the same number of elements than the width.

    Returns
    -------
    :class:`T.ndarray`
        The Gaussian window in the time domain. If the width (and possibly
        amplitude) argument is a vector, the function returns a matrix with
        shape (len(width), len(x)).
    """
    # turn parameters into a numpy arrays for dimension check
    x = xp.array(x)
    width = xp.array(width)

    # add new axis for outer product if several widths are given
    width = width[:, None] if width.shape and (width.ndim == 1) else width

    return xp.exp(-((x / width) ** 2))


def complex_morlet(x, center, width):
    """Complex Morlet wavelet.

    The complex Morlet wavelet is a complex plane wave modulated by a
    Gaussian window. The oscillatory frequency of the plane wave is the
    center frequency, and the temporal width of the Gaussian is the width
    argument.

    This function can generate a filter bank at once if the width and center
    arguments are vectors of the same size. In this case, they should have a
    new axis with respect to the time vector to allow for outer product.

    Arguments
    ---------
    x: :class:`T.ndarray` or np.ndarray
        Time vector in seconds.

    width: float or :class:`T.ndarray` or np.ndarray
        Temporal signal width in seconds.

    center: float or :class:`T.ndarray` or np.ndarray
        Center frequency in hertz.

    Keyword arguments
    -----------------
    amplitude: float (optional)
        Wavelet normalization (default 1). If amplitude is a vector, it should
        have the same dimension than width (and center).

    Returns
    -------
    filter: :class:`T.ndarray`
        The complex Mortlet wavelet in the time domain. If the center and width
        (and possibly amplitude) arguments are vectors, the function returns
        a matrix with shape (len(width), len(x)).
    """
    # turn parameters into a numpy arrays for dimension check
    x = xp.array(x)
    width = xp.array(width)
    center = xp.array(center)

    # add new axis for outer product if several widths are given
    width = width[:, None] if width.shape else width
    center = center[:, None] if center.shape else center

    # check compatibility between arguments
    if width.shape and center.shape:
        assert (
            width.shape == center.shape
        ), f"Shape for widths {width.shape} and centers {center.shape} differ."

    return gaussian_window(x, width) * xp.exp(2j * xp.pi * center * x)


class ComplexMorletBank:
    """Complex Morlet filter bank."""

    def __init__(
        self,
        bins: int,
        octaves: int = 8,
        resolution: int = 1,
        quality: float = 4.0,
        taper_alpha=None,
        sampling_rate: float = 1.0,
    ):
        """Filter bank creation.

        This function creates the filter bank in the time domain, and obtains
        it in the frequency domain with a fast Fourier transform.

        Parameters
        ----------
        bins: int
            Number of bins in the time domain. The filter bank will be
            symmetric around the center of the time vector.
        octaves: int
            Number of octaves in the frequency domain.
        resolution: int, optional
            Number of filters per octaves (default 1).
        quality: float, optional
            Filter bank quality factor (constant, default 4).
        taper_alpha: float, optional
            Tapering factor for the time domain. If None, no tapering is
            applied (default None).
        sampling_rate: float, optional
            Sampling rate of the signal (default 1).
        """
        self.bins = bins
        self.octaves = octaves
        self.resolution = resolution
        self.quality = quality
        self.sampling_rate = sampling_rate

        # Generate the filter bank
        self.wavelets = complex_morlet(self.times, self.centers, self.widths)

        # Obtain the filter bank in the frequency domain
        self.spectra = xp.fft.fft(self.wavelets)

        # Size attributes
        self.size = self.wavelets.shape[0]

        # Tapering or not
        if taper_alpha is None:
            self.taper = xp.array(xp.ones(bins))
        else:
            self.taper = xp.array(tukey(bins, alpha=taper_alpha))

    def transform(self, sample):
        """Compute the scalogram for a given sample.

        Parameters
        ----------
        sample: np.ndarray
            The sample to be transformed of shape `(..., channels, bins)`. The
            number of bins should be the same as the number of bins of the
            filter bank.

        Returns
        -------
        scalogram: np.ndarray
            The scalograms for all channels with shape (the ellipsis stands for
            unknown number of input dimensions)
            `n_channels, ..., n_filters, n_bins`.
        """
        sample = xp.fft.fft(xp.array(sample) * xp.array(self.taper))
        convolved = sample[..., None, :] * xp.array(self.spectra)
        scalogram = xp.fft.fftshift(xp.fft.ifft(convolved), axes=-1)
        if xp.__name__ == "cupy":
            return xp.asnumpy(scalogram)
        else:
            return xp.abs(scalogram)

    @property
    def times(self):
        """Wavelet bank symmetric time vector in seconds."""
        duration = self.bins / self.sampling_rate
        if xp.__name__ == "cupy":
            return xp.asnumpy(xp.linspace(-0.5, 0.5, num=self.bins) * duration)
        else:
            return xp.linspace(-0.5, 0.5, num=self.bins) * duration

    @property
    def frequencies(self):
        """Wavelet bank frequency vector in hertz."""
        if xp.__name__ == "cupy":
            return xp.asnumpy(xp.linspace(0, self.sampling_rate, self.bins))
        else:
            return xp.linspace(0, self.sampling_rate, self.bins)

    @property
    def nyquist(self):
        """Wavelet bank frequency vector in hertz."""
        return self.sampling_rate / 2

    @property
    def shape(self):
        """Filter bank total number of filters."""
        return self.octaves * self.resolution, self.bins

    @property
    def ratios(self):
        """Wavelet bank ratios."""
        ratios = xp.linspace(self.octaves, 0.0, self.shape[0], endpoint=False)
        if xp.__name__ == "cupy":
            return xp.asnumpy(-ratios[::-1])
        else:
            return -ratios[::-1]

    @property
    def scales(self):
        """Wavelet bank scaling factors."""
        if xp.__name__ == "cupy":
            return xp.asnumpy(2**self.ratios)
        else:
            return 2**self.ratios

    @property
    def centers(self):
        """Wavelet bank center frequencies."""
        if xp.__name__ == "cupy":
            return xp.asnumpy(self.scales * self.nyquist)
        else:
            return self.scales * self.nyquist

    @property
    def widths(self):
        """Wavelet bank temporal widths."""
        if xp.__name__ == "cupy":
            return xp.asnumpy(self.quality / self.centers)
        else:
            return self.quality / self.centers
