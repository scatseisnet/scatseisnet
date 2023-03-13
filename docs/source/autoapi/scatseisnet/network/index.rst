:py:mod:`scatseisnet.network`
=============================

.. py:module:: scatseisnet.network

.. autoapi-nested-parse::

   Scattering network graph definition.

   This module contains the :class:`~.ScatteringNetwork` class that implements the
   scattering network graph. The network is composed of a series of wavelet filter
   banks (so far limited to :class:`~.ComplexMorletBank` instances) and pooling
   operations.

   The :class:`~.ScatteringNetwork` class is a container for the filter banks and
   the pooling operations. It is used to transform time samples (waveforms with an
   artibtrary number of channels) with the scattering network graph. The
   :class:`~.ScatteringNetwork` class is also used to compute the scattering
   network graph properties, such as the number of output channels, the number of
   output bins, etc.

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

   scatseisnet.network.ScatteringNetwork




.. py:class:: ScatteringNetwork(*layer_kwargs: dict, bins: int = 128, sampling_rate: float = 1.0)

   
   Scattering network graph.

   :param layer_kwargs: The keyword argiments of each filter bank keyword arguments, in the form
                        of a :series of :class:`dict` objects with the keyword arguments for
                        :class:`~.ComplexMorletBank`. The number of network layers is defined by
                        the number of arguments. Please see the :class:`~.ComplexMorletBank`
                        documentation for more information about the keyword arguments themselves.
   :type layer_kwargs: :class:`dict`
   :param bins: Number of time samples per signal windows. By default, this value is
                128. Note that once set, the value cannot be changed.
   :type bins: :class:`int`, optional
   :param sampling_rate: Input data sampling rate in Hertz. This is useful to keep track of
                         physical frequencies in the filterbanks properties. The default value is
                         1.0 (reduced frequency).
   :type sampling_rate: :class:`float`, optional

   .. attribute:: banks

      Filter banks of the scattering network. The length of this list is equal
      to the number of layers of the scattering network. Each filter bank is
      an instance of the :class:`~.ComplexMorletBank` class.

      :type: :class:`list` of :class:`~.ComplexMorletBank`

   .. attribute:: sampling_rate

      Input data sampling rate in Hertz.

      :type: float















   ..
       !! processed by numpydoc !!
   .. py:method:: __len__() -> int

      
      Number of layers (or depth) of the scattering network.
















      ..
          !! processed by numpydoc !!

   .. py:method:: __repr__() -> str

      
      String representation of the scattering network.
















      ..
          !! processed by numpydoc !!

   .. py:method:: transform_segment(segment: numpy.ndarray, reduce_type: Union[Callable, None] = None) -> list

      
      Scattering network transformation.

      This function transforms a single segment with the scattering network.
      The `reduce_type` parameter defines the pooling operation. It can be
      either `max`, `avg`, or `med`.

      .. note::

         If the ``reduce_type`` parameter is not defined, the function returns
         the scalogram of each layer of the scattering network (i.e. the
         continuous wavelet transform of the input segment at each layer) without
         any pooling operation.

      :param segment: The input segment time series to calculate the scattering
                      coefficients from. The shape of the array must be ``(bins,
                      n_channels)``, where ``bins`` is the number of time samples per
                      segment and ``n_channels`` is the number of channels. The number of
                      channels can be 1 or more.
      :type segment: :class:`numpy.ndarray`
      :param reduce_type: The reduction function (e.g. :func:`numpy.mean`). If not defined,
                          the function returns the scalogram of each layer of the scattering
                          network, without any pooling operation.
      :type reduce_type: callable, optional

      :returns: **scattering_coefficients** -- The scattering coefficients per layer of the scattering network.
      :rtype: :class:`list` of array-like

      .. rubric:: Examples

      >>> import numpy as np
      >>> from scatseisnet import ScatteringNetwork
      >>> layer_kwargs = [
      ...     {"octaves": 8, "resolution": 8},
      ...     {"octaves": 12, "resolution": 1},
      ... ]
      >>> network = ScatteringNetwork(layer_kwargs)
      >>> segment = np.random.randn(128)
      >>> scattering_coefficients = network.transform_segment(segment, 'max')
      >>> len(scattering_coefficients)
      2
      >>> scattering_coefficients[0].shape
      (64,)
      >>> scattering_coefficients[1].shape
      (64, 24)















      ..
          !! processed by numpydoc !!

   .. py:method:: transform(segments: numpy.ndarray, reduce_type: Union[Callable, None] = None) -> list

      
      Transform a set of segments.

      This function is a wrapper to loop over a series of segments with the
      :meth:`~.transform_segment` method. Please refer to this method for more
      information.

      :param segments: The input segment time series to calculate the scattering
                       coefficients from. The shape of the array must be ``(n_segments,
                       bins, n_channels)``, where ``bins`` is the number of time samples
                       per segment and ``n_channels`` is the number of channels. The number
                       of channels can be 1 or more.
      :type segments: :class:`numpy.ndarray`
      :param reduce_type: The reduction function (e.g. :func:`numpy.mean`). If not defined,
                          the function returns the scalogram of each layer of the scattering
                          network, without any pooling operation.
      :type reduce_type: callable, optional

      :returns: **scattering_coefficients** -- The scattering coefficients per layer of the scattering network.
      :rtype: :class:`list` of array-like

      .. rubric:: Examples

      >>> import numpy as np
      >>> from scatseisnet import ScatteringNetwork
      >>> layer_kwargs = [
      ...     {"octaves": 8, "resolution": 8},
      ...     {"octaves": 12, "resolution": 1},
      ... ]
      >>> network = ScatteringNetwork(layer_kwargs)
      >>> segments = np.random.randn(10, 128)
      >>> scattering_coefficients = network.transform(segments, 'max')
      >>> len(scattering_coefficients)
      2
      >>> scattering_coefficients[0].shape
      (10, 64)
      >>> scattering_coefficients[1].shape
      (10, 64, 24)















      ..
          !! processed by numpydoc !!


