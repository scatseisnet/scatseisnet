# Welcome to the __scatseisnet__ repository

<div align=center>

<img src="https://github.com/scatseisnet/scatseisnet/blob/main/docs/source/logo/logo_scatseisnet_anim.png?raw=true" width=200/>

**Scatseisnet**\
Scattering network for seismic data analysis.

[![Python Version](https://img.shields.io/pypi/pyversions/scatseisnet)](https://pypi.org/project/scatseisnet/)
[![PyPI Version](https://img.shields.io/pypi/v/scatseisnet.svg)](https://pypi.org/project/scatseisnet/)
![GitHub last commit](https://img.shields.io/github/last-commit/scatseisnet/scatseisnet)

</div>

## About

This library contains programs to transform time series into scattering
coefficients with a scattering network. The scattering network is a deep
neural network with wavelet filters as convolutional layers.

The package supports Python 3.8+ including the latest Python 3.13.

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

### Basic installation (CPU only)

```bash
pip install scatseisnet
```

### GPU acceleration (optional)

For GPU acceleration with CUDA, install with the GPU extras:

```bash
pip install scatseisnet[gpu]
```

Or install CuPy separately:

```bash
pip install cupy
```

The package will automatically detect and use CuPy if available, providing significant speedup for large-scale computations.

### Tutorials and examples

To run the tutorial notebooks, install with tutorial dependencies:

```bash
pip install scatseisnet[tutorials]
```

## Documentation

Please check the [documentation](https://scatseisnet.github.io/scatseisnet/). You can find tutorials therein in the form of notebooks.

## Testing

The package includes a comprehensive test suite with 51 tests covering all major functionality. Tests are compatible with Python 3.8+ including Python 3.13.

```bash
# Run tests with pytest
pytest tests/ -v

# Run tests with unittest (no additional dependencies)
python -m unittest discover tests/ -v

# With coverage report
pytest tests/ --cov=scatseisnet --cov-report=html
```

See `tests/README.md` for detailed testing documentation and CI/CD information.

## Citation

```
Seydoux, L. S., Steinmann, R., Gärtner, M., Tong, F., Esfahani, R., & Campillo, M. (2025). Scatseisnet, a Scattering network for seismic data analysis (0.3). Zenodo. https://doi.org/10.5281/zenodo.15110686
```

## Contribution guidelines

Thank you for your interest in contributing to this project! Here are some guidelines to help ensure a smooth and successful contribution process. Please read them carefully before contributing. We are happy to answer any questions you may have, and to welcome you as a contributor.

1. __Fork__ the project to your own GitHub account by clicking the "Fork" button in the top right corner of the repository page. This will allow you to make changes to the project without affecting the main project.

2. Create a __new branch__ for your contribution. This will keep your changes separate from the main branch and make it easier to review and merge your changes. The name of your branch should be concise and descriptive. For example, if you are adding a new feature, you might call your branch "add-feature".

3. Write concise __commit messages__ that describe the changes you made. Use the present tense and avoid redundant information. We try to follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

4. Make sure your changes work as intended and do not introduce new bugs or problems. Write __tests__ if applicable.

5. __Document__ your changes with following the [numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html) format. This step is important to ensure that the package documentation is up to date and complete. If you are not sure about this step, we can help you.

6. When you are ready to submit your changes, create a __pull request__ from your branch to the main branch of the original repository. Provide a clear description of your changes and why they are necessary, and we will review your contribution.

Thank you again for your interest in contributing to this project!
