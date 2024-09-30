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

    return xp.exp(-0.5 *((x / width) ** 2)) / (width**2 * np.pi)**0.25


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
            if normalize_wavelet == 'l1':
                self.norm_factor = xp.abs(self.wavelets).sum(axis=1)[:, xp.newaxis]
            elif normalize_wavelet == 'l2':
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



##################


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


def morlet_1d(N, xi, sigma, normalize='l1', P_max=5, eps=1e-7):
    """ Computes the Fourier transform of a Morlet filter.

    A Morlet filter is the sum of a Gabor filter and a low-pass filter
    to ensure that the sum has exactly zero mean in the temporal domain.
    It is defined by the following formula in time:
    psi(t) = g_{sigma}(t) (e^{i xi t} - beta)
    where g_{sigma} is a Gaussian envelope, xi is a frequency and beta is
    the cancelling parameter.

    Parameters
    ----------
    N : int
        size of the temporal support
    xi : float
        central frequency (in [0, 1])
    sigma : float
        bandwidth parameter
    normalize : string, optional
        normalization types for the filters. Defaults to 'l1'.
        Supported normalizations are 'l1' and 'l2' (understood in time domain).
    P_max: int, optional
        integer controlling the maximal number of periods to use to ensure
        the periodicity of the Fourier transform. (At most 2*P_max - 1 periods
        are used, to ensure an equal distribution around 0.5). Defaults to 5
        Should be >= 1
    eps : float
        required machine precision (to choose the adequate P)

    Returns
    -------
    morlet_f : array_like
        numpy array of size (N,) containing the Fourier transform of the Morlet
        filter at the frequencies given by np.fft.fftfreq(N).
    """
    if type(P_max) != int:
        raise ValueError('P_max should be an int, got {}'.format(type(P_max)))
    if P_max < 1:
        raise ValueError('P_max should be non-negative, got {}'.format(P_max))
    # Find the adequate value of P
    P = min(adaptive_choice_P(sigma, eps=eps), P_max)
    assert P >= 1
    # Define the frequencies over [1-P, P[
    freqs = xp.arange((1 - P) * N, P * N, dtype=float) / float(N)
    if P == 1:
        # in this case, make sure that there is continuity around 0
        # by using the interval [-0.5, 0.5]
        freqs_low = xp.fft.fftfreq(N)
    elif P > 1:
        freqs_low = freqs
    else:
        raise ValueError("Invalid P value in morlet_1d.")
    # define the gabor at freq xi and the low-pass, both of width sigma
    gabor_f = xp.exp(-(freqs - xi)**2 / (2 * sigma**2))
    low_pass_f = xp.exp(-(freqs_low**2) / (2 * sigma**2))
    # discretize in signal <=> periodize in Fourier
    gabor_f = periodize_filter_fourier(gabor_f, nperiods=2 * P - 1)
    low_pass_f = periodize_filter_fourier(low_pass_f, nperiods=2 * P - 1)
    # find the summation factor to ensure that morlet_f[0] = 0.
    kappa = gabor_f[0] / low_pass_f[0]
    morlet_f = gabor_f - kappa * low_pass_f
    # normalize the Morlet if necessary
    morlet_f *= get_normalizing_factor(morlet_f, normalize=normalize)
    return morlet_f


def adaptive_choice_P(sigma, eps=1e-7):
    """ Adaptive choice of the value of the number of periods in the frequency
    domain used to compute the Fourier transform of a Morlet wavelet.

    This function considers a Morlet wavelet defined as the sum
    of
    * a Gabor term hat psi(omega) = hat g_{sigma}(omega - xi)
    where 0 < xi < 1 is some frequency and g_{sigma} is
    the Gaussian window defined in Fourier by
    hat g_{sigma}(omega) = e^{-omega^2/(2 sigma^2)}
    * a low pass term \\hat \\phi which is proportional to \\hat g_{\\sigma}.

    If \\sigma is too large, then these formula will lead to discontinuities
    in the frequency interval [0, 1] (which is the interval used by numpy.fft).
    We therefore choose a larger integer P >= 1 such that at the boundaries
    of the Fourier transform of both filters on the interval [1-P, P], the
    magnitude of the entries is below the required machine precision.
    Mathematically, this means we would need P to satisfy the relations:

    |\\hat \\psi(P)| <= eps and |\\hat \\phi(1-P)| <= eps

    Since 0 <= xi <= 1, the latter implies the former. Hence the formula which
    is easily derived using the explicit formula for g_{\\sigma} in Fourier.

    Parameters
    ----------
    sigma: float
        Positive number controlling the bandwidth of the filters
    eps : float, optional
        Positive number containing required precision. Defaults to 1e-7

    Returns
    -------
    P : int
        integer controlling the number of periods used to ensure the
        periodicity of the final Morlet filter in the frequency interval
        [0, 1[. The value of P will lead to the use of the frequency
        interval [1-P, P[, so that there are 2*P - 1 periods.
    """
    val = xp.sqrt(-2 * (sigma**2) * xp.log(eps))
    P = int(xp.ceil(val + 1))
    return P


def periodize_filter_fourier(h_f, nperiods=1):
    """ Computes a periodization of a filter provided in the Fourier domain.

    Parameters
    ----------
    h_f : array_like
        complex numpy array of shape (N*n_periods,)
    nperiods: int, optional
        Number of periods which should be used to periodize

    Returns
    -------
    v_f : array_like
        complex numpy array of size (N,), which is a periodization of
        h_f as described in the formula:
        v_f[k] = sum_{i=0}^{n_periods - 1} h_f[i * N + k]
    """
    N = h_f.shape[0] // nperiods
    v_f = h_f.reshape(nperiods, N).mean(axis=0)
    return v_f


def get_normalizing_factor(h_f, normalize='l1'):
    """ Computes the desired normalization factor for a filter defined in Fourier.

    Parameters
    ----------
    h_f : array_like
        numpy vector containing the Fourier transform of a filter
    normalize : string, optional
        desired normalization type, either 'l1' or 'l2'. Defaults to 'l1'.

    Returns
    -------
    norm_factor : float
        such that h_f * norm_factor is the adequately normalized vector.
    """
    h_real = np.fft.ifft(h_f)
    if xp.abs(h_real).sum() < 1e-7:
        raise ValueError('Zero division error is very likely to occur, ' +
                         'aborting computations now.')
    if normalize == 'l1':
        norm_factor = 1. / (xp.abs(h_real).sum())
    elif normalize == 'l2':
        norm_factor = 1. / xp.sqrt((xp.abs(h_real)**2).sum())
    else:
        raise ValueError("Supported normalizations only include 'l1' and 'l2'")
    return norm_factor


def gauss_1d(N, sigma, normalize='l1', P_max=5, eps=1e-7):
    """ Computes the Fourier transform of a low pass gaussian window.

    \\hat g_{\\sigma}(\\omega) = e^{-\\omega^2 / 2 \\sigma^2}

    Parameters
    ----------
    N : int
        size of the temporal support
    sigma : float
        bandwidth parameter
    normalize : string, optional
        normalization types for the filters. Defaults to 'l1'
        Supported normalizations are 'l1' and 'l2' (understood in time domain).
    P_max : int, optional
        integer controlling the maximal number of periods to use to ensure
        the periodicity of the Fourier transform. (At most 2*P_max - 1 periods
        are used, to ensure an equal distribution around 0.5). Defaults to 5
        Should be >= 1
    eps : float, optional
        required machine precision (to choose the adequate P)

    Returns
    -------
    g_f : array_like
        numpy array of size (N,) containing the Fourier transform of the
        filter (with the frequencies in the np.fft.fftfreq convention).
    """
    # Find the adequate value of P
    if type(P_max) != int:
        raise ValueError('P_max should be an int, got {}'.format(type(P_max)))
    if P_max < 1:
        raise ValueError('P_max should be non-negative, got {}'.format(P_max))
    P = min(adaptive_choice_P(sigma, eps=eps), P_max)
    assert P >= 1
    # switch cases
    if P == 1:
        freqs_low = xp.fft.fftfreq(N)
    elif P > 1:
        freqs_low = xp.arange((1 - P) * N, P * N, dtype=float) / float(N)
    else:
        raise ValueError("Invalid P value in gauss_1d.")
    # define the low pass
    g_f = xp.exp(-freqs_low**2 / (2 * sigma**2))
    # periodize it
    g_f = periodize_filter_fourier(g_f, nperiods=2 * P - 1)
    # normalize the signal
    g_f *= get_normalizing_factor(g_f, normalize=normalize)
    # return the Fourier transform
    return g_f

class ComplexMorletBank_new:
    """Complex Morlet filter bank."""

    def __init__(
        self,
        bins: int,
        octaves: int = 8,
        quality: float = 4.0,
        resolution: int = np.sqrt(0.5),
        max_frequency: float = 0.35,
        sampling_rate: float = 1.0,
        normalization: str = "l1",
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
        self.quality = quality
        self.sampling_rate = sampling_rate
        self.max_frequency = max_frequency
        self.normalization = normalization
        self.resolution = resolution

        # Generate the filter bank
        self.spectra = xp.asarray(
            [morlet_1d(self.bins, xi, sig, normalize=normalization, 
                       P_max=10, eps=1e-10) 
                       for xi, sig in zip(self.center_normalized, self.widths)
                       ])

        self.wavelets = xp.fft.ifftshift(xp.fft.ifft(self.spectra, axis = -1), axes = -1)


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
        scalogram = (xp.fft.ifft(convolved))
        if xp.__name__ == "cupy":
            return (xp.asnumpy(scalogram))
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
    def scales(self) -> np.ndarray:
        """Wavelet bank scaling factors."""
        if xp.__name__ == "cupy":
            return xp.asnumpy(2**self.ratios)
        else:
            return xp.logspace(0, -self.octaves, num=self.octaves * self.quality, endpoint=False, base=2)

    @property
    def centers(self) -> np.ndarray:
        """Wavelet bank center frequencies."""
        if xp.__name__ == "cupy":
            return xp.asnumpy(self.scales * self.nyquist)
        else:
            return self.max_frequency * self.scales * self.sampling_rate
        
    @property
    def center_normalized(self) -> np.ndarray:
        """Wavelet bank center frequencies."""
        if xp.__name__ == "cupy":
            return xp.asnumpy(self.scales * self.nyquist)
        else:
            return self.max_frequency * self.scales
        
    @property
    def widths(self) -> np.ndarray:
        """Wavelet bank temporal widths."""
        if xp.__name__ == "cupy":
            return xp.asnumpy(self.quality / self.centers)
        else:
            return xp.array([self.compute_sigma_psi(m, self.quality, r = self.resolution) for m in self.center_normalized])
    
    def compute_sigma_psi(self, xi, Q, r=xp.sqrt(0.5)):
        """ Computes the frequential width sigma for a Morlet filter of frequency xi
        belonging to a family with Q wavelets.
        
        The frequential width is adapted so that the intersection of the
        frequency responses of the next filter occurs at a r-bandwidth specified
        by r, to ensure a correct coverage of the whole frequency axis.
        """

        factor = 1. / (2. ** (1. / Q))
        term1 = (1 - factor) / (1 + factor)
        term2 = 1. / xp.sqrt(2 * xp.log(1. / r))
        return xi * term1 * term2
    
    @property
    def ratios(self) -> np.ndarray:
        """Wavelet bank ratios."""
        #ratios = xp.linspace(self.octaves, 0.0, self.shape[0], endpoint=False)
        if xp.__name__ == "cupy":
            return xp.asnumpy(-self.scales[::-1])
        else:
            return np.arange(len(self.scales))
        