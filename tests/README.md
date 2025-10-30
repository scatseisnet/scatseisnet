# ScatSeisNet Test Suite

This directory contains the comprehensive test suite for the scatseisnet package.

## Test Structure

- `test_import.py` - Tests for package imports and version detection
- `test_wavelet.py` - Tests for wavelet functions and ComplexMorletBank
- `test_network.py` - Tests for ScatteringNetwork functionality
- `test_operation.py` - Tests for operation functions (pooling)
- `test_compatibility.py` - Tests for Python version compatibility

## Running Tests

### Basic test run
```bash
pytest tests/
```

### With verbose output
```bash
pytest tests/ -v
```

### With coverage report
```bash
pytest tests/ --cov=scatseisnet --cov-report=term-missing
```

### Run specific test file
```bash
pytest tests/test_network.py -v
```

### Run specific test class or function
```bash
pytest tests/test_network.py::TestScatteringNetworkCreation -v
pytest tests/test_network.py::TestScatteringNetworkCreation::test_network_creation_single_layer -v
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

All tests pass on Python 3.13 with:
- NumPy 2.3.4
- SciPy 1.16.3
- pytest 8.4.2

Key compatibility updates:
- Replaced `pkg_resources` with `importlib.metadata`
- Updated minimum Python version to 3.8
- All tests verify cross-version compatibility
