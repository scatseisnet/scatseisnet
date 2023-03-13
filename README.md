# Welcome to the __scatseisnet__ repository

<div align=center>

<img src=docs/source/_static/logo_scatseisnet.png width=250px/>

[![Python Version](https://img.shields.io/pypi/pyversions/covseisnet)](https://pypi.org/project/covseisnet/)
[![PyPI Version](https://img.shields.io/pypi/v/covseisnet.svg)](https://pypi.org/project/covseisnet/)\
[![Code style:black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub last commit](https://img.shields.io/github/last-commit/scatseisnet/scatseisnet)

</div>

## About

This library contains programs to transform time series into scattering
coefficients with a scattering network. The scattering network is a deep
neural network with wavelet filters as convolutional layers.
The __scatseisnet__ package is under construction. A target release date will be
around April 2023.

This package was written and documented by [Léonard Seydoux](https://github.com/leonard-seydoux) 
and [René Steinmann](https://github.com/ReneSteinmann).
The notebooks were written by Leonard Seydoux and René
Steinmann, and are a simplified product of the papers published by René
Steinmann et al. and Seydoux et al. listed in the documentation. 

This work was supported by the European Advanced Grant _F-IMAGE_ (ERC PE10,
ERC-2016-ADG) and by the Multidisciplinary Institute of Artificial Intelligence
(MIAI) at the University of Grenoble Alpes.

> __Scatseisnet: a toolbox for scattering networks in seismology__\
> Copyright ©️ 2023 Léonard Seydoux and René Steinmann
> 
> This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
> This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
> You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

## Installation

We are planning to release the package on pypi, for now you can install the
package with the following command. Please consider installing the package at a
location where you have write access, and which should not change over time.
You may also want to run the command in a virtual environment (e.g. conda) for a
clean installation.

### CPU-only installation

```bash
git clone https://github.com/scatseisnet/scatseisnet.git 
cd scatseisnet
pip install -e .
```

### GPU usage

If you want to use a GPU, you need to install the package with the package CuPy.
The code will try to find it and use it if it is installed. You can install it
with the following command.

```bash
pip install cupy
```

## Documentation

Please check the [documentation](https://scatseisnet.readthedocs.io/en/latest/). You can find tutorials thererin in the form of notebooks.

