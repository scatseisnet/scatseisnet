"""Scattering network graph definition.

This module contains the :class:`~.ScatteringNetwork` class that implements the
scattering network graph. The network is composed of a series of filter banks
and pooling operations. 
"""

# Copyright (C) 2023 Léonard Seydoux

# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <https://www.gnu.org/licenses/>.

import typing as T

import numpy as np

from .operation import pool
from .wavelet import ComplexMorletBank


class ScatteringNetwork:
    """Scattering network model.

    Parameters
    ----------
    layer_kwargs: :class:`list` of :class:`dict`
        The keyword argiments of each filter bank keyword arguments, in the form
        of a :class:`list`. Each :class:`dict` object contains the keyword
        arguments for the :class:`~.ComplexMorletBank`. The number of network
        layers is defined by the length of this list. Please see the
        :class:`~.ComplexMorletBank` documentation for more information about
        the keyword arguments.
    bins: :class:`int`, optional
        Number of time samples per signal windows. By default, this value is
        128. Note that once set, the value cannot be changed.
    sampling_rate: :class:`float`, optional
        Input data sampling rate in Hertz. This is useful to keep track of
        physical frequencies in the filterbanks properties. The default value is
        1.0 (reduced frequency).

    Attributes
    ----------
    banks: :class:`list` of :class:`~.ComplexMorletBank`
        Filter banks of the scattering network. The length of this list is equal
        to the number of layers of the scattering network. Each filter bank is
        an instance of the :class:`~.ComplexMorletBank` class.
    sampling_rate: float
        Input data sampling rate in Hertz.
    """

    def __init__(
        self,
        *layer_kwargs: dict,
        bins: int = 128,
        sampling_rate: float = 1.0,
    ) -> None:
        self.sampling_rate = sampling_rate
        self.bins = bins
        self.banks = [
            ComplexMorletBank(bins, sampling_rate=sampling_rate, **kw)
            for kw in layer_kwargs
        ]

    def __len__(self) -> int:
        """Return the number of layers of the scattering network."""
        return len(self.banks)

    def transform_sample(
        self, sample, reduce_type: T.Union[T.Callable, None] = None
    ) -> list:
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

    def transform(
        self, samples, reduce_type: T.Union[T.Callable, None] = None
    ) -> list:
        """Transform a set of samples.

        This function is a wrapper to loop over a series of samples with the
        :meth:`~.transform_sample` method. The parameter ``reduce_type`` defines
        the pooling operation. It can be either ``"max"``, ``"avg"``, or
        ``"med"``. Note that if ``reduce_type`` is ``None``, the function
        returns the scalogram of each layer of the scattering network (i.e. the
        continuous wavelet transform of the input sample at each layer) without
        any pooling operation.

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
    def depth(self) -> int:
        """Network depth or number of layers. This property returns the number
        of layers of the scattering network. It is equivalent to the length of
        the :attr:`banks` attribute.
        """
        return len(self.banks)
