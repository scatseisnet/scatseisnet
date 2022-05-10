# -*- coding: utf-8 -*-
"""Scattering network.

author:
    Leonard Seydoux and Randall Balestriero
"""

import cupy as cp

from .signal import pool
from .wavelet import ComplexMorletBank


class Network:
    """Scattering network."""

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
        # Define banks
        self.banks = [ComplexMorletBank(bins, **p) for p in layer_properties]
        self.sampling_rate = sampling_rate
        pass

    def transform_sample(self, sample, reduce_type=None):
        """Scattering network transformation.

        Arguments
        ---------
        sample: np.ndarray
            The input
        """
        # loop over banks
        input_sample = sample
        output = list()
        for bank in self.banks:
            scalogram = bank.transform(input_sample)
            input_sample = scalogram
            output.append(pool(scalogram, reduce_type))
        return output

    def transform(self, samples, reduce_type=None):
        """Transform a series of samples into scattering domain.

        Arguments
        ---------
        samples: np.ndarray
            The input data to transform.

        reduce_type: str
            The reduction type (max, avg, med).

        Returns
        -------
        features: list
            The features per layer of the scattering network.
        """
        # initialize empty lists for each layer
        features = [[] for _ in range(self.depth)]

        # transform each sample
        for sample in samples:
            scatterings = self.transform_sample(sample, reduce_type)
            for index, scattering in enumerate(scatterings):
                features[index].append(scattering)

        if cp.__name__ == "numpy":  # if using numpy instead of cupy
            return [cp.array(feature) for feature in features]
        else:
            return [cp.array(feature).get() for feature in features]

    @property
    def depth(self):
        """Network depth."""
        return len(self.banks)
