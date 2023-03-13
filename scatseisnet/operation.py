"""Miscellaneous operations for scatseisnet.

This module contains miscellaneous operations for scatseisnet, such as
segmentation and pooling.

.. dropdown:: Terms of use

    .. code-block:: text

        Copyright (C) 2021 Léonard Seydoux.

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

import numpy as np


def segment(
    x: np.ndarray,
    window_size: int,
    stride: T.Union[int, None] = None,
) -> T.Generator[np.ndarray, None, None]:
    """Segment array into overlapping windows.

    Arguments
    ---------
    x: :class:`numpy.ndarray`
        Array to segment.
    window_size: int
        Sliding window size in numpy of points
    stride: int, optional
        Sliding window stride in numpy of points. If None, stride is equal to
        window_size.

    Yields
    ------
    The elements of the segmented array.
    """
    bins = x.shape[-1]
    index = 0
    stride = window_size if stride is None else stride
    while (index + window_size) <= bins:
        yield x[..., index : index + window_size]
        index += stride


def segmentize(
    x: np.ndarray,
    window_size: int,
    stride: T.Union[int, None] = None,
) -> np.ndarray:
    """Segment array into overlapping windows.

    Arguments
    ---------
    x: :class:`numpy.ndarray`
        Array to segment.
    window_size: int
        Sliding window size in numpy of points
    stride: int, optional
        Sliding window stride in numpy of points. If None, stride is equal to
        window_size.

    Returns
    -------
    The segmented array with shape ``(n_windows, n_channels, n_times)``.
    """
    return np.array([x for x in segment(x, window_size, stride)])


def pool(
    x: np.ndarray,
    reduce_type: T.Union[T.Callable, None] = None,
) -> np.ndarray:
    """Pooling operation performed on the last axis.

    Arguments
    ---------
    x: :class:`numpy.ndarray`
        The input data to pool.
    reduce_type: callable, optional
        The reducing operation (e.g. :func:`numpy.mean()`). If None, no
        operation is performed.

    Returns
    -------
    pooled: :class:`numpy.ndarray`
        The data pooled with same shape of input data minus last dimension.
    """
    if reduce_type is None:
        return x
    else:
        return reduce_type(x, axis=-1)
