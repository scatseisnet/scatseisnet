# coding=utf-8
"""Deep scattering transform clustering on segmented time series."""

__all__ = [
    "display",
    "parse",
    "Network",
    "inventory",
    "signal",
    "wavelet",
    "hierarchy",
]

from . import display
from . import wavelet
from . import inventory
from . import signal
from . import hierarchy
from .io import parse
from .network import Network

from pkg_resources import get_distribution

__version__ = get_distribution('scatseisnet').version