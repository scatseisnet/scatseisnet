# coding=utf-8
"""Deep scattering transform clustering on segmented time series.

This package implements the deep scattering transform clustering on segmented
time series. The deep scattering transform is a deep learning architecture
that can be used to extract features from time series. 

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

__all__ = [
    "ScatteringNetwork",
    "operation",
    "wavelet",
    "network",
]

from . import wavelet
from . import operation
from . import network
from .network import ScatteringNetwork
from pkg_resources import get_distribution

__version__ = get_distribution("scatseisnet").version