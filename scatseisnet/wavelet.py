"""Wavelet class and functions.

This module contains the wavelet class and functions to generate wavelets.

.. dropdown:: Terms of use

    .. code-block:: text

        Copyright (C) 2023 Léonard Seydoux.

        This program is free software: you can redistribute it and/or modify it
        under the terms of the GNU General Public License as published by the
        Free Software Foundation, either version 3 of the License, or (at your
        option) any later version.
        
        This program is distributed in the hope that it will be useful, but
        WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
        General Public License for more details.

        You should have received a copy of the GNU General Public License along
        with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import typing as T

try:
    import cupy as xp  # type: ignore
except ImportError:
    import numpy as xp
import numpy as np

def gaussian_window(
    x: xp.ndarray,
    width: T.Union[float, T.Sequence[float], xp.ndarray],
) -> xp.ndarray:
    """Gaussian function.

    This function can generate a bank of windows at once if the width
    argument is a vector (and/or amplitude). In this case, it should have
    a new axis with respect to the time vector to allow for outer product.

    Parameters
    ----------
    x : :class:`numpy.ndarray` or :class:`cupy.ndarray`
        Input variable, in the same units than the width.
    width : float or np.ndarray
        Window width (in the same units than the input variable). If an array
        is provided, the function returns as many windows as the number of
        elements of this parameter.
    amplitude : float or np.ndarray, optional
        Window amplitude at maximum (default 1). If this parameter is a vector,
        it should have the same number of elements than the width.

    Returns
    -------
    Same type as ``x``.
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


def complex_morlet(
    x: xp.ndarray,
    center: T.Union[float, T.Sequence[float], xp.ndarray],
    width: T.Union[float, T.Sequence[float], xp.ndarray],
) -> xp.ndarray:
    """Complex Morlet wavelet.

    The complex Morlet wavelet is a complex plane wave modulated by a Gaussian
    window. The oscillatory frequency of the plane wave is the center frequency,
    and the temporal width of the Gaussian is the width argument.

    This function can generate a filter bank at once if the width and center
    arguments are vectors of the same size. In this case, they should have a new
    axis with respect to the time vector to allow for outer product.

    Arguments
    ---------
    x: :class:`numpy.ndarray` or :class:`cupy.ndarray`
        Time vector in seconds.
    width: float or :class:`numpy.ndarray` or :class:`cupy.ndarray`.
        Temporal signal width in seconds.
    center: float or :class:`numpy.ndarray` or :class:`cupy.ndarray`.
        Center frequency in Hertz.

    Returns
    -------
    Same type as ``x``.
        The complex Mortlet wavelet in the time domain. If the center and width
        (and possibly amplitude) arguments are vectors, the function returns a
        matrix with shape ``(len(width), len(x))``.
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
        normalize_wavelet=None,
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

        # Normalize filter bank or not
        if normalize_wavelet is not None:
            if normalize_wavelet == 'L1':
                self.norm_factor = xp.abs(self.wavelets).sum(axis=1)[:, xp.newaxis]
            elif normalize_wavelet == 'L2':
                self.norm_factor = xp.sqrt((xp.abs(self.wavelets)**2).sum(axis=1))[:, xp.newaxis]
            else:
                AttributeError(f"'normalize_wavelet' has no attribute {normalize_wavelet}",
                               "Supported are normalization by the 'L1'- and 'L2'-norm'.")

            # Normalize filter bank
            self.wavelets /= self.norm_factor

        # Obtain the filter bank in the frequency domain
        self.spectra = xp.fft.fft(self.wavelets)

        # Size attributes
        self.size = self.wavelets.shape[0]
        
    def __repr__(self) -> str:
        """Representation of the filter bank."""
        return (
            f"ComplexMorletBank(bins={self.bins}, octaves={self.octaves}, "
            f"resolution={self.resolution}, quality={self.quality}, "
            f"sampling_rate={self.sampling_rate}, len={len(self)})"
        )

    def __len__(self) -> int:
        """Length of the filter bank."""
        return self.octaves * self.resolution

    def transform(self, segment: xp.ndarray) -> np.ndarray:
        """Compute the scalogram for a given segment.

        Parameters
        ----------
        segment: :class:`numpy.ndarray`
            The segment to be transformed of shape ``(..., channels, bins)``. The
            number of bins should be the same as the number of bins of the
            filter bank.

        Returns
        -------
        scalogram: :class:`numpy.ndarray`
            The scalograms for all channels with shape (the ellipsis stands for
            unknown number of input dimensions)
            `n_channels, ..., n_filters, n_bins`.
        """
        segment = xp.fft.fft(xp.array(segment))
        convolved = segment[..., None, :] * xp.array(self.spectra)
        scalogram = xp.fft.fftshift(xp.fft.ifft(convolved), axes=-1)
        if xp.__name__ == "cupy":
            return np.abs(xp.asnumpy(scalogram))
        else:
            return xp.abs(scalogram)

    @property
    def times(self) -> np.ndarray:
        """Wavelet bank symmetric time vector in seconds."""
        duration = self.bins / self.sampling_rate
        if xp.__name__ == "cupy":
            return xp.asnumpy(xp.linspace(-0.5, 0.5, num=self.bins) * duration)
        else:
            return xp.linspace(-0.5, 0.5, num=self.bins) * duration

    @property
    def frequencies(self) -> np.ndarray:
        """Wavelet bank frequency vector in Hertz."""
        if xp.__name__ == "cupy":
            return xp.asnumpy(xp.linspace(0, self.sampling_rate, self.bins))
        else:
            return xp.linspace(0, self.sampling_rate, self.bins)

    @property
    def nyquist(self) -> float:
        """Nyqyust frequency in Hertz."""
        return self.sampling_rate / 2

    @property
    def shape(self) -> tuple:
        """Filter bank total number of filters."""
        return len(self), self.bins

    @property
    def ratios(self) -> np.ndarray:
        """Wavelet bank ratios."""
        ratios = xp.linspace(self.octaves, 0.0, self.shape[0], endpoint=False)
        if xp.__name__ == "cupy":
            return xp.asnumpy(-ratios[::-1])
        else:
            return -ratios[::-1]

    @property
    def scales(self) -> np.ndarray:
        """Wavelet bank scaling factors."""
        if xp.__name__ == "cupy":
            return xp.asnumpy(2**self.ratios)
        else:
            return 2**self.ratios

    @property
    def centers(self) -> np.ndarray:
        """Wavelet bank center frequencies."""
        if xp.__name__ == "cupy":
            return xp.asnumpy(self.scales * self.nyquist)
        else:
            return self.scales * self.nyquist

    @property
    def widths(self) -> np.ndarray:
        """Wavelet bank temporal widths."""
        if xp.__name__ == "cupy":
            return xp.asnumpy(self.quality / self.centers)
        else:
            return self.quality / self.centers
