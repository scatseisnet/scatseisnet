"""Scattering network.

This module contains the ScatteringNetwork class that implements the scattering
network graph. The network is composed of a series of filter banks and pooling
operations. The pooling operation is defined by the `reduce_type` parameter that
can be either `max`, `avg`, or `med`. The `transform` method returns a list of
features per layer of the scattering network. The `transform_sample` method
returns the scattering coefficients per layer of the scattering network.

Made in 2019 by Léonard Seydoux (seydoux@ipgp.fr) and Randall Balestriero.
"""

import numpy as np

from .signal import pool
from .wavelet import ComplexMorletBank


class ScatteringNetwork:
    """Scattering network.

    Attributes
    ----------
    banks: list of ComplexMorletBank
        The filter banks of the scattering network.
    sampling_rate: float
        The input data sampling rate in Hz.
    """

    def __init__(self, layer_kwargs, bins=128, sampling_rate=1.0):
        """Initialize scattering network graph.

        Parameters
        ----------
        layer_kwargs: list of dict
            The list of filter bank keyword arguments. Each dictionary contains
            the keyword arguments for the ComplexMorletBank. The number of
            network layers is defined by the length of this list.
        bins: int, optional
            The number of samples per input segment.
        sampling_rate: float, optional
            The input data sampling rate in Hz. This is useful to keep track of
            physical frequencies in the filterbanks properties. The default
            value is 1.0 (reduced frequency).
        """
        self.sampling_rate = sampling_rate
        self.bins = bins
        self.banks = [
            ComplexMorletBank(bins, sampling_rate=sampling_rate, **kw)
            for kw in layer_kwargs
        ]

    def transform_sample(self, sample, reduce_type=None):
        """Scattering network transformation.

        This function transforms a single sample with the scattering network.
        The `reduce_type` parameter defines the pooling operation. It can be
        either `max`, `avg`, or `med`.

        Note that if the `reduce_type` parameter is not defined, the function
        returns the scalogram of each layer of the scattering network (i.e. the
        continuous wavelet transform of the input sample at each layer).

        Parameters
        ----------
        sample: array-like
            The input sample to calculate the scattering coefficients.
        reduce_type: str, optional
            The reduction type (max, avg, or med).

        Returns
        -------
        scattering_coefficients: list of numpy.ndarray
            The scattering coefficients per layer of the scattering network.

        Raises
        ------
        ValueError
            If the `reduce_type` parameter is not defined or is not one of
            `max`, `avg`, or `med`.

        Examples
        --------
        >>> import numpy as np
        >>> from scatseisnet import ScatteringNetwork
        >>> layer_kwargs = [
        ...     {"octaves": 8, "resolution": 8},
        ...     {"octaves": 12, "resolution": 1},
        ... ]
        >>> network = ScatteringNetwork(layer_kwargs)
        >>> sample = np.random.randn(128)
        >>> scattering_coefficients = network.transform_sample(sample, 'max')
        >>> len(scattering_coefficients)
        2
        >>> scattering_coefficients[0].shape
        (64,)
        >>> scattering_coefficients[1].shape
        (64, 24)
        """
        # Initialize the scattering coefficients list
        output = list()

        # Calculate coefficients
        for bank in self.banks:
            scalogram = bank.transform(sample.copy())
            sample = scalogram
            output.append(pool(scalogram, reduce_type))

        return output

    def transform(self, samples, reduce_type=None):
        """Transform a set of samples.

        This function is a wrapper to loop over a series of samples
        with the `transform_sample` method. The `reduce_type` parameter
        defines the pooling operation. It can be either `max`, `avg`, or `med`.

        Note that if the `reduce_type` parameter is not defined, the function
        returns the scalogram of each layer of the scattering network (i.e. the
        continuous wavelet transform of the input sample at each layer).

        Parameters
        ----------
        samples: array-like
            The input samples to calculate the scattering coefficients.
        reduce_type: str, optional
            The reduction type (max, avg, or med).

        Returns
        -------
        scattering_coefficients: list of numpy.ndarray
            The scattering coefficients per layer of the scattering network.

        Raises
        ------
        ValueError
            If the `reduce_type` parameter is not defined or is not one of
            `max`, `avg`, or `med`.

        Examples
        --------
        >>> import numpy as np
        >>> from scatseisnet import ScatteringNetwork
        >>> layer_kwargs = [
        ...     {"octaves": 8, "resolution": 8},
        ...     {"octaves": 12, "resolution": 1},
        ... ]
        >>> network = ScatteringNetwork(layer_kwargs)
        >>> samples = np.random.randn(10, 128)
        >>> scattering_coefficients = network.transform(samples, 'max')
        >>> len(scattering_coefficients)
        2
        >>> scattering_coefficients[0].shape
        (10, 64)
        >>> scattering_coefficients[1].shape
        (10, 64, 24)
        """
        # Initialize the scattering coefficients list
        features = [[] for _ in range(self.depth)]

        # Calculate coefficients
        for sample in samples:
            scatterings = self.transform_sample(sample, reduce_type)
            for layer_index, scattering in enumerate(scatterings):
                features[layer_index].append(scattering)

        return [np.array(feature) for feature in features]

    @property
    def depth(self):
        """Network depth or number of layers."""
        return len(self.banks)
