# Welcome to the __scatseisnet__ repository

<div align=center>

<img src=docs/source/_static/logo_scatseisnet.png width=250px/>

[![Python Version](https://img.shields.io/pypi/pyversions/scatseisnet)](https://pypi.org/project/scatseisnet/)
[![PyPI Version](https://img.shields.io/pypi/v/scatseisnet.svg)](https://pypi.org/project/scatseisnet/)\
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
Any contributions are very welcomed.

This work was supported by the European Advanced Grant [F-IMAGE](https://f-image.osug.fr/?lang=en) (ERC PE10,
ERC-2016-ADG) and by the [Multidisciplinary Institute of Artificial Intelligence](https://miai.univ-grenoble-alpes.fr/)
(MIAI) at the University of Grenoble Alpes.

> Scatseisnet: a toolbox for scattering networks in seismology\
> __Copyright ©️ 2023 Léonard Seydoux and René Steinmann__
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

The package is available from the PyPI repository. To install using pip, execute the following line:

### CPU-only installation

```bash
pip install scatseisnet
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

## Contribution guidelines

Thank you for your interest in contributing to this project! Here are some guidelines to help ensure a smooth and successful contribution process. Please read them carefully before contributing. We are happy to answer any questions you may have, and to welcome you as a contributor.

1. __Fork__ the project to your own GitHub account by clicking the "Fork" button in the top right corner of the repository page. This will allow you to make changes to the project without affecting the main project.

2. Create a __new branch__ for your contribution. This will keep your changes separate from the main branch and make it easier to review and merge your changes. The name of your branch should be concise and descriptive. For example, if you are adding a new feature, you might call your branch "add-feature".

3. Write concise __commit messages__ that describe the changes you made. Use the present tense and avoid redundant information. We try to follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

4. Make sure your changes work as intended and do not introduce new bugs or problems. Write __tests__ if applicable.

5. __Document__ your changes with following the [numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html) format. This step is important to ensure that the package documentation is up to date and complete. If you are not sure about this step, we can help you.

6. When you are ready to submit your changes, create a __pull request__ from your branch to the main branch of the original repository. Provide a clear description of your changes and why they are necessary, and we will review your contribution.

Thank you again for your interest in contributing to this project!
