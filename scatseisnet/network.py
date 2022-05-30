# coding: utf-8
"""Scattering network.

author:
    Leonard Seydoux and Randall Balestriero
"""

import numpy as np

from .signal import pool
from .wavelet import ComplexMorletBank


class ScatteringNetwork:
    """Scattering network.

    Attributes
    ----------
    banks: list of :class:`wavelet.ComplexMorletBank`
        The filter banks of the scattering network at each layer.
    sampling_rate: float
        The sampling rate of the input time series. Default to 1.
    """

    def __init__(self, layer_properties, bins=128, sampling_rate=1.0):
        """Initialize scattering network graph.

        Parameters
        ----------
        layer_properties: list of dict
            The wavelet bank properties at each layer. Check the
            ComplexMorletBank class for details about the arguments.
        bins: int, optional
            The number of samples per input segment.
        sampling_rate: float, optional
            The input data sampling rate. This is useful to keep track of
            physical frequencies in the filterbanks properties.
        """
        self.banks = [ComplexMorletBank(bins, **p) for p in layer_properties]
        self.sampling_rate = sampling_rate

    def transform_sample(self, sample, reduce_type=None):
        """Scattering network transformation.

        Parameters
        ----------
        samples: np.ndarray
            The input set of samples to transform.
        reduce_type: str, optional
            The reduction type (max, avg, or med).
        """
        # Initialize
        input_sample = sample
        output = list()

        # Network transforms
        for bank in self.banks:
            scalogram = bank.transform(input_sample)
            input_sample = scalogram
            output.append(pool(scalogram, reduce_type))

        return output

    def transform(self, samples, reduce_type=None):
        """Transform a series of samples.

        This function is a wrapper to loop over a series of samples
        with the `transform_sample` method.

        Parameters
        ----------
        samples: np.ndarray
            The input set of samples to transform.
        reduce_type: str, optional
            The reduction type (max, avg, or med).

        Returns
        -------
        features: list of numpy.ndarray
            The features per layer of the scattering network.
        """
        # Empty feature lists for each layer
        features = [[] for _ in range(self.depth)]

        # Transform each sample
        for sample in samples:
            scatterings = self.transform_sample(sample, reduce_type)
            for layer_index, scattering in enumerate(scatterings):
                features[layer_index].append(scattering)

        return [np.array(feature) for feature in features]


    @property
    def depth(self):
        """Network depth or number of layers."""
        return len(self.banks)
