# coding: utf-8
"""Wavelet definition and transform.

author:
    Leonard Seydoux and Randall Balestriero
"""


import numpy as np

from scipy.signal import tukey
from scipy.signal import deconvolve


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
    x = np.array(x)
    width = np.array(width)

    # add new axis for outer product if several widths are given
    width = width[:, None] if width.shape and (width.ndim == 1) else width

    return np.exp(-((x / width) ** 2))


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
    x = np.array(x)
    width = np.array(width)
    center = np.array(center)

    # add new axis for outer product if several widths are given
    width = width[:, None] if width.shape else width
    center = center[:, None] if center.shape else center

    # check compatibility between arguments
    if width.shape and center.shape:
        assert (
            width.shape == center.shape
        ), f"Shape for widths {width.shape} and centers {center.shape} differ."

    return gaussian_window(x, width) * np.exp(2j * np.pi * center * x)


class ComplexMorletBank:
    """Complex Morlet filter bank."""

    def __init__(
        self,
        bins,
        octaves,
        resolution=1,
        quality=4,
        input_taper_alpha=1e-3,
        sampling_rate=1.0,
    ):
        """Filter bank creation.

        This function creates the filter bank in the time domain, and obtains
        it in the frequency domain with a fast Fourier transform.

        Arguments
        ---------
        bins: int
            Number of samples in the time domain.
        octaves: int
            Number of octaves spanned by the filter bank.
        resolution: int, optional
            Number of filters per octaves (default 1).
        quality: float, optional
            Filter bank quality factor (constant, default 4).
        input_taper_alpha: float, optional
            Filter bank quality factor (constant, default 4).
        sampling_rate: float, optional
            Input data sampling rate (default 1 Hz).
        """
        # Static properties
        self.bins = bins
        self.octaves = octaves
        self.resolution = resolution
        self.quality = quality
        self.sampling_rate = sampling_rate

        # generate bank
        self.wavelets = complex_morlet(self.times, self.centers, self.widths)
        self.spectra = np.fft.fft(self.wavelets)
        self.size = self.wavelets.shape[0]
        self.input_taper = np.array(tukey(bins, alpha=input_taper_alpha))
        pass

    def transform(self, sample):
        """Scalogram applied to a data sample.

        Arguments
        ---------
        x: np.ndarray
            A data sample of shape `(..., channels, bins)`, with the same
            number of bins than the filter bank.

        Returns
        -------
        wx: np.ndarray
            The scalograms for all channels with shape (the ellipsis stands for
            unknown number of input dimensions)
            `n_channels, ..., n_filters, n_bins`.
        """
        sample = np.fft.fft(np.array(sample) * self.input_taper)
        convolved = sample[..., None, :] * self.spectra
        scalogram = np.fft.fftshift(np.fft.ifft(convolved), axes=-1)
        return np.abs(scalogram)

    def inverse_transform(self, sample):
        return deconvolve(sample, self.spectra)

    @property
    def times(self):
        """Wavelet bank symmetric time vector in seconds."""
        duration = self.bins / self.sampling_rate
        return np.linspace(-0.5, 0.5, num=self.bins) * duration

    @property
    def frequencies(self):
        """Wavelet bank frequency vector in hertz."""
        return np.linspace(0, self.sampling_rate, self.bins)

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
        ratios = np.linspace(self.octaves, 0.0, self.shape[0], endpoint=False)
        return -ratios[::-1]

    @property
    def scales(self):
        """Wavelet bank scaling factors."""
        return 2**self.ratios

    @property
    def centers(self):
        """Wavelet bank center frequencies."""
        return self.scales * self.nyquist

    @property
    def widths(self):
        """Wavelet bank temporal widths."""
        return self.quality / self.centers
