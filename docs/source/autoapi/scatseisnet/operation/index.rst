:py:mod:`scatseisnet.operation`
===============================

.. py:module:: scatseisnet.operation

.. autoapi-nested-parse::

   Miscellaneous operations for scatseisnet.

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

   ..
       !! processed by numpydoc !!


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   scatseisnet.operation.segment
   scatseisnet.operation.segmentize
   scatseisnet.operation.pool



.. py:function:: segment(x: numpy.ndarray, window_size: int, stride: Union[int, None] = None) -> Generator[numpy.ndarray, None, None]

   
   Segment array into overlapping windows.

   :param x: Array to segment.
   :type x: :class:`numpy.ndarray`
   :param window_size: Sliding window size in numpy of points
   :type window_size: int
   :param stride: Sliding window stride in numpy of points. If None, stride is equal to
                  window_size.
   :type stride: int, optional

   :Yields: *The elements of the segmented array.*















   ..
       !! processed by numpydoc !!

.. py:function:: segmentize(x: numpy.ndarray, window_size: int, stride: Union[int, None] = None) -> numpy.ndarray

   
   Segment array into overlapping windows.

   :param x: Array to segment.
   :type x: :class:`numpy.ndarray`
   :param window_size: Sliding window size in numpy of points
   :type window_size: int
   :param stride: Sliding window stride in numpy of points. If None, stride is equal to
                  window_size.
   :type stride: int, optional

   :rtype: The segmented array with shape ``(n_windows, n_channels, n_times)``.















   ..
       !! processed by numpydoc !!

.. py:function:: pool(x: numpy.ndarray, reduce_type: Union[Callable, None] = None) -> numpy.ndarray

   
   Pooling operation performed on the last axis.

   :param x: The input data to pool.
   :type x: :class:`numpy.ndarray`
   :param reduce_type: The reducing operation (e.g. :func:`numpy.mean()`). If None, no
                       operation is performed.
   :type reduce_type: callable, optional

   :returns: **pooled** -- The data pooled with same shape of input data minus last dimension.
   :rtype: :class:`numpy.ndarray`















   ..
       !! processed by numpydoc !!

