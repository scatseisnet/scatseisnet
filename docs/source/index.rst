Welcome to **scatseisnet**'s documentation!
===========================================

.. image:: _static/logo_scatseisnet.png
   :width: 0
   :align: center

.. raw:: html

   <p align="center">
      <img src="_images/logo_scatseisnet.png" width=250px
      style="background-color: transparent;"/>
   </p>

|


Contents
--------

.. toctree::
   :maxdepth: 2

   guide
   tutorials

About
-----

The **scatseisnet** library contains programs to transform time series into scattering
coefficients with a scattering network. The scattering network is a deep
neural network with wavelet filters as convolutional layers. 

This package was written and documented by Léonard Seydoux and René Steinmann.
The core of the package and docstrings was written by Léonard Seydoux, the
documentation was generated using ReadTheDocs and the tutorials were written
by René Steinmann and Léonard Seydoux. The tutorial notebooks are a simplified product of the papers published by René Steinmann.
The repository is hosted on `GitHub <https://github.com/scatseisnet/scatseisnet>`_ and the documentation is available on `ReadTheDocs <https://scatseisnet.readthedocs.io>`_.

This work was supported by the `European Advanced Grant F-IMAGE <https://f-image.osug.fr/?lang=en>`_ (ERC PE10, ERC-2016-ADG) and by the `Multidisciplinary Institute of Artificial Intelligence <https://miai.univ-grenoble-alpes.fr/>`_ (MIAI) at the University of Grenoble Alpes.
If you use this package for your own scientific output, please cite one or more of the papers mentionned in the References section below.

.. important::

   This project is still in development. The API is not stable and may change
   without notice. Once a stable version is released, the API will be
   considered stable and will not change without a major version bump.
   A target release date will be around April 2023.

License
-------

**Copyright ©️ 2023 Léonard Seydoux and René Steinmann**

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Please use the following dropdown menu to see the full terms of use, or directrly have a look at the LICENCE file in the root directory of the repository.

.. dropdown:: Full terms of use

   .. include:: ../../LICENCE
      :literal:

Installation
------------

The package is available from the PyPI repository. To install using pip, execute the following line:


.. code-block:: bash
   :caption: CPU-only installation

   pip install scatseisnet

If you want to use a GPU, you need to install the package with the package CuPy.
The code will try to find it and use it if it is installed. You can install it
with the following command.

.. code-block:: bash
   :caption: GPU usage

   pip install cupy


References
----------

1. Seydoux, L., Balestriero, R., Poli, P. et al. *Clustering earthquake signals and background noises in continuous seismic data with unsupervised deep learning.* Nat Commun 11, 3972 (2020). https://doi.org/10.1038/s41467-020-17841-x

2. Barkaoui, S., Lognonné, P., Kawamura, T., Stutzmann, É., Seydoux, L., de Hoop, M. V., ... & Banerdt, W. B. (2021). *Anatomy of continuous Mars SEIS and pressure data from unsupervised learning.* Bulletin of the Seismological Society of America, 111(6), 2964-2981. https://doi.org/10.1785/0120210095

3. Steinmann, R., Seydoux, L., Beaucé, E., & Campillo, M. (2022). *Hierarchical exploration of continuous seismograms with unsupervised learning.* Journal of Geophysical Research: Solid Earth, 127(1), e2021JB022455. https://doi.org/10.1029/2021JB022455

4. Steinmann, R., Seydoux, L., & Campillo, M. (2022). *AI-Based Unmixing of Medium and Source Signatures From Seismograms: Ground Freezing Patterns* Geophysical Research Letters, 49(15), e2022GL098854. https://doi.org/10.1029/2022GL098854