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

    def __init__(self, octaves, resolution, quality, bins, sampling_rate=1.0):
        """Initialize graph.

        Arguments
        ---------
        args: :class:`argparse.Namespace`
            The input arguments. Since most of the input arguments are
            dedicated to the scattering newtork architecture, they are all
            passed to this constructor. Note that almost all the attributes
            of the args are attributed to the present class.

        Keyword arguments
        -----------------
        sampling: float (optional)
            The input data sampling rate. This is useful to keep track of
            physical frequencies in the filterbanks properties.

        channels: list (optional)
            A list with channels names. At the time this is used only for
            getting the number of channels for each data samples, but it can
            later be used for naming the scalograms and scatterings.
        """

        # define banks
        bank_properties = zip(octaves, resolution, quality)
        self.banks = [ComplexMorletBank(bins, *p) for p in bank_properties]
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

        if cp.__name__ == "numpy": # if using numpy instead of cupy
            return [cp.array(feature) for feature in features]
        else:
            return [cp.array(feature).get() for feature in features]

    @property
    def depth(self):
        """Network depth."""
        return len(self.banks)
