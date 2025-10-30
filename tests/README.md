# ScatSeisNet Test Suite

This directory contains the comprehensive test suite for the scatseisnet package.

## Overview

- **51 tests** covering all major functionality
- **82% code coverage**
- **Python 3.8 - 3.13** compatible (including Python 3.13.7 ✅)
- **CI/CD** via GitHub Actions on Linux, macOS, and Windows

## Test Structure

- `test_import.py` (6 tests) - Package imports and version detection
- `test_wavelet.py` (10 tests) - Wavelet functions and ComplexMorletBank
- `test_network.py` (14 tests) - ScatteringNetwork functionality
- `test_operation.py` (6 tests) - Operation functions (pooling)
- `test_compatibility.py` (15 tests) - Python version compatibility

## Running Tests

### Using pytest (recommended)

```bash
# Basic test run
pytest tests/

# With verbose output
pytest tests/ -v

# With coverage report
pytest tests/ --cov=scatseisnet --cov-report=term-missing

# With HTML coverage report
pytest tests/ --cov=scatseisnet --cov-report=html

# Run specific test file
pytest tests/test_network.py -v

# Run specific test class
pytest tests/test_network.py::TestScatteringNetworkCreation -v

# Run specific test function
pytest tests/test_network.py::TestScatteringNetworkCreation::test_network_creation_single_layer -v
```

### Using unittest (built-in)

```bash
# Run all tests
python -m unittest discover tests/

# Run specific test file
python -m unittest tests.test_network

# Run with verbose output
python -m unittest discover tests/ -v
```

## Test Coverage

Current test coverage: **82%**

Coverage breakdown:
- `__init__.py`: 80%
- `network.py`: 95%
- `wavelet.py`: 81%
- `operation.py`: 53%

## Running Tests Across Python Versions

### Using tox
```bash
# Test on all configured Python versions
tox

# Test on specific Python version
tox -e py313

# Generate coverage report
tox -e coverage
```

### Using UV (faster)
```bash
# Create environment and run tests
uv venv --python 3.13
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
uv pip install pytest pytest-cov
pytest tests/ -v
```

## Test Requirements

Install test dependencies:
```bash
pip install -r requirements-test.txt
```

Or with uv:
```bash
uv pip install pytest pytest-cov
```

## CI/CD

Tests are automatically run on:
- **Operating Systems**: Ubuntu, macOS, Windows
- **Python Versions**: 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
- **Triggers**: Push to main/development, Pull requests

See `.github/workflows/tests.yml` for CI configuration.

## Writing New Tests

Follow these guidelines when adding new tests:

1. **Use descriptive names**: `test_network_creation_single_layer` not `test1`
2. **Test one thing**: Each test should verify a single behavior
3. **Use setUp/tearDown**: For common initialization
4. **Include docstrings**: Explain what the test verifies
5. **Test edge cases**: Zero, negative, large values, etc.

Example:
```python
class TestNewFeature(unittest.TestCase):
    """Test new feature functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.data = create_test_data()
    
    def test_feature_basic_case(self):
        """Test that feature works with basic input."""
        result = new_feature(self.data)
        self.assertIsNotNone(result)
        self.assertEqual(result.shape, expected_shape)
```

## Python 3.13 Compatibility

All tests pass on Python 3.13.7 with:
- **NumPy 2.3.4** (NumPy 2.x compatible)
- **SciPy 1.16.3** (latest compatible version)
- **pytest 8.4.2**

### Key Compatibility Updates

The package was updated to support Python 3.13:

1. **Replaced deprecated `pkg_resources`**: Now uses `importlib.metadata` for version detection (Python 3.8+)
2. **Updated classifiers**: Added Python 3.12 and 3.13 support in `pyproject.toml`
3. **Minimum Python**: Raised from 3.7 to 3.8 (Python 3.7 reached EOL)
4. **Dependencies**: Works with both NumPy 1.x (older Python) and NumPy 2.x (Python 3.9+)

### Testing Across Versions

The test suite verifies:
- Import system works with `importlib.metadata`
- NumPy 2.x compatibility (new dtypes, API changes)
- SciPy 1.14+ compatibility
- FFT operations, complex numbers, type conversions
- All core functionality (wavelets, networks, operations)
