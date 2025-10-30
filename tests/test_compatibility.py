"""Test Python version compatibility."""

import sys
import unittest
import numpy as np


class TestPythonCompatibility(unittest.TestCase):
    """Test compatibility across Python versions."""

    def test_python_version_minimum(self):
        """Test that Python version is at least 3.8."""
        self.assertGreaterEqual(sys.version_info.major, 3)
        self.assertGreaterEqual(sys.version_info.minor, 8)

    def test_numpy_available(self):
        """Test that NumPy is available."""
        self.assertTrue(hasattr(np, '__version__'))
        self.assertIsInstance(np.__version__, str)

    def test_numpy_basic_operations(self):
        """Test basic NumPy operations work."""
        arr = np.array([1, 2, 3, 4, 5])
        self.assertEqual(np.mean(arr), 3.0)
        self.assertEqual(np.max(arr), 5)
        self.assertEqual(np.min(arr), 1)

    def test_scipy_available(self):
        """Test that SciPy is available."""
        import scipy
        self.assertTrue(hasattr(scipy, '__version__'))
        self.assertIsInstance(scipy.__version__, str)

    def test_scipy_signal_windows(self):
        """Test SciPy signal windows module."""
        from scipy.signal.windows import tukey
        window = tukey(128, alpha=0.5)
        self.assertEqual(len(window), 128)
        self.assertTrue(np.all(window >= 0))
        self.assertTrue(np.all(window <= 1))

    def test_complex_operations(self):
        """Test complex number operations."""
        z = np.exp(2j * np.pi * 0.25)
        self.assertTrue(np.iscomplexobj(z))
        self.assertAlmostEqual(np.abs(z), 1.0)

    def test_fft_operations(self):
        """Test FFT operations work."""
        signal = np.random.randn(128)
        fft_result = np.fft.fft(signal)
        self.assertEqual(len(fft_result), len(signal))
        self.assertTrue(np.iscomplexobj(fft_result))

    def test_memory_operations(self):
        """Test memory-intensive operations."""
        large_array = np.random.randn(1000, 1000)
        result = np.mean(large_array, axis=0)
        self.assertEqual(len(result), 1000)


class TestImportlibMetadata(unittest.TestCase):
    """Test importlib.metadata functionality."""

    def test_importlib_metadata_import(self):
        """Test that importlib.metadata can be imported."""
        if sys.version_info >= (3, 8):
            from importlib.metadata import version
            self.assertIsNotNone(version)

    def test_version_function(self):
        """Test version function works for installed packages."""
        if sys.version_info >= (3, 8):
            from importlib.metadata import version
            # Test with numpy (always installed)
            numpy_version = version('numpy')
            self.assertIsInstance(numpy_version, str)
            self.assertGreater(len(numpy_version), 0)

    def test_package_metadata(self):
        """Test that package metadata can be retrieved."""
        if sys.version_info >= (3, 8):
            from importlib.metadata import version, PackageNotFoundError
            try:
                pkg_version = version('scatseisnet')
                self.assertIsInstance(pkg_version, str)
            except PackageNotFoundError:
                # Package might not be installed in test environment
                self.skipTest("Package not installed")


class TestDataTypes(unittest.TestCase):
    """Test data type compatibility."""

    def test_float_types(self):
        """Test different float types."""
        for dtype in [np.float32, np.float64]:
            arr = np.array([1.0, 2.0, 3.0], dtype=dtype)
            self.assertEqual(arr.dtype, dtype)

    def test_complex_types(self):
        """Test different complex types."""
        for dtype in [np.complex64, np.complex128]:
            arr = np.array([1+2j, 3+4j], dtype=dtype)
            self.assertEqual(arr.dtype, dtype)

    def test_integer_types(self):
        """Test different integer types."""
        for dtype in [np.int32, np.int64]:
            arr = np.array([1, 2, 3], dtype=dtype)
            self.assertEqual(arr.dtype, dtype)

    def test_type_conversions(self):
        """Test type conversions."""
        arr_float = np.array([1.5, 2.5, 3.5])
        arr_int = arr_float.astype(np.int32)
        self.assertEqual(arr_int.dtype, np.int32)
        self.assertTrue(np.all(arr_int == [1, 2, 3]))


if __name__ == '__main__':
    unittest.main()
