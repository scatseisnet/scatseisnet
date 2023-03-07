Welcome to ScatSeisNet's documentation!
========================================

**ScatSeisNet** transforms seismic time series into scattering coefficients with a scattering network, which resembles a convolutional network based on wavelelts.
The code repository is hosted on github at: https://github.com/scatseisnet/scatseisnet
 
Check out the :doc:`usage` section for further information, including
how to :ref:`installation` the project.

.. note::

   This project is under active development.

Contents
--------

.. toctree::
   :maxdepth: 1

   usage
   api
   notebooks

Purpose and philosophy of this Package
---------------------------------------
In the recent years, we worked on a scattering network for seismic time series data, mainly for data exploration task involving dimensionality reduction and clustering.
We've seen an increasing interest in the seismological community for this kind of approach, and we decided to make the code available to the community. 
This package delivers the network instance and in the tutorials we introduce the scattering network together with some data exploration applications.
Please note that the task and data at hand drive the choice of the exact design of the scattering network and the tools used for data exploration.
The following papers show some possible applications and we hope that they can inspire you for your specific use case. 
If you use this package for your own scientific output, please cite one or more of the following papers:

- 2021: **Hierarchical Exploration of Continuous Seismograms With Unsupervised Learning**, this paper shows the first application of **ScatSeisNet** with Gabor wavelets in combination with hierarchical clustering for data exploration. `10.1029/2021JB022455 <https://doi.org/10.1029/2021JB022455>`_

- 2022: **AI-Based Unmixing of Medium and Source Signatures From Seismograms: Ground Freezing Patterns**, it is the second application of **ScatSeisNet** where we focus more on the aspect of interpreting the independent components retrieved from the scattering coefficients. `10.1029/2022GL098854 <https://doi.org/10.1029/2022GL098854>`_