:py:mod:`scatseisnet.wavelet`
=============================

.. py:module:: scatseisnet.wavelet

.. autoapi-nested-parse::

   Wavelet class and functions.

   This module contains the wavelet class and functions to generate wavelets.

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

   ..
       !! processed by numpydoc !!


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   scatseisnet.wavelet.ComplexMorletBank



Functions
~~~~~~~~~

.. autoapisummary::

   scatseisnet.wavelet.gaussian_window
   scatseisnet.wavelet.complex_morlet



.. py:function:: gaussian_window(x: cupy.ndarray, width: Union[float, Sequence[float], cupy.ndarray]) -> cupy.ndarray

   
   Gaussian function.

   This function can generate a bank of windows at once if the width
   argument is a vector (and/or amplitude). In this case, it should have
   a new axis with respect to the time vector to allow for outer product.

   :param x: Input variable, in the same units than the width.
   :type x: :class:`numpy.ndarray` or :class:`cupy.ndarray`
   :param width: Window width (in the same units than the input variable). If an array
                 is provided, the function returns as many windows as the number of
                 elements of this parameter.
   :type width: float or np.ndarray
   :param amplitude: Window amplitude at maximum (default 1). If this parameter is a vector,
                     it should have the same number of elements than the width.
   :type amplitude: float or np.ndarray, optional

   :returns: The Gaussian window in the time domain. If the width (and possibly
             amplitude) argument is a vector, the function returns a matrix with
             shape (len(width), len(x)).
   :rtype: Same type as ``x``.















   ..
       !! processed by numpydoc !!

.. py:function:: complex_morlet(x: cupy.ndarray, center: Union[float, Sequence[float], cupy.ndarray], width: Union[float, Sequence[float], cupy.ndarray]) -> cupy.ndarray

   
   Complex Morlet wavelet.

   The complex Morlet wavelet is a complex plane wave modulated by a Gaussian
   window. The oscillatory frequency of the plane wave is the center frequency,
   and the temporal width of the Gaussian is the width argument.

   This function can generate a filter bank at once if the width and center
   arguments are vectors of the same size. In this case, they should have a new
   axis with respect to the time vector to allow for outer product.

   :param x: Time vector in seconds.
   :type x: :class:`numpy.ndarray` or :class:`cupy.ndarray`
   :param width: Temporal signal width in seconds.
   :type width: float or :class:`numpy.ndarray` or :class:`cupy.ndarray`.
   :param center: Center frequency in Hertz.
   :type center: float or :class:`numpy.ndarray` or :class:`cupy.ndarray`.

   :returns: The complex Mortlet wavelet in the time domain. If the center and width
             (and possibly amplitude) arguments are vectors, the function returns a
             matrix with shape ``(len(width), len(x))``.
   :rtype: Same type as ``x``.















   ..
       !! processed by numpydoc !!

.. py:class:: ComplexMorletBank(bins: int, octaves: int = 8, resolution: int = 1, quality: float = 4.0, taper_alpha=None, sampling_rate: float = 1.0)

   
   Complex Morlet filter bank.
















   ..
       !! processed by numpydoc !!
   .. py:property:: times
      :type: numpy.ndarray

      
      Wavelet bank symmetric time vector in seconds.
















      ..
          !! processed by numpydoc !!

   .. py:property:: frequencies
      :type: numpy.ndarray

      
      Wavelet bank frequency vector in Hertz.
















      ..
          !! processed by numpydoc !!

   .. py:property:: nyquist
      :type: float

      
      Nyqyust frequency in Hertz.
















      ..
          !! processed by numpydoc !!

   .. py:property:: shape
      :type: tuple

      
      Filter bank total number of filters.
















      ..
          !! processed by numpydoc !!

   .. py:property:: ratios
      :type: numpy.ndarray

      
      Wavelet bank ratios.
















      ..
          !! processed by numpydoc !!

   .. py:property:: scales
      :type: numpy.ndarray

      
      Wavelet bank scaling factors.
















      ..
          !! processed by numpydoc !!

   .. py:property:: centers
      :type: numpy.ndarray

      
      Wavelet bank center frequencies.
















      ..
          !! processed by numpydoc !!

   .. py:property:: widths
      :type: numpy.ndarray

      
      Wavelet bank temporal widths.
















      ..
          !! processed by numpydoc !!

   .. py:method:: __repr__() -> str

      
      Representation of the filter bank.
















      ..
          !! processed by numpydoc !!

   .. py:method:: __len__() -> int

      
      Length of the filter bank.
















      ..
          !! processed by numpydoc !!

   .. py:method:: transform(segment: cupy.ndarray) -> numpy.ndarray

      
      Compute the scalogram for a given segment.

      :param segment: The segment to be transformed of shape ``(..., channels, bins)``. The
                      number of bins should be the same as the number of bins of the
                      filter bank.
      :type segment: :class:`numpy.ndarray`

      :returns: **scalogram** -- The scalograms for all channels with shape (the ellipsis stands for
                unknown number of input dimensions)
                `n_channels, ..., n_filters, n_bins`.
      :rtype: :class:`numpy.ndarray`















      ..
          !! processed by numpydoc !!


