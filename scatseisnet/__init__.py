# coding=utf-8
"""Deep scattering transform clustering on segmented time series."""

__all__ = [
    "ScatteringNetwork",
    "signal",
    "wavelet",
]

from . import wavelet
from . import signal
from .network import ScatteringNetwork

from pkg_resources import get_distribution

__version__ = get_distribution("scatseisnet").version
