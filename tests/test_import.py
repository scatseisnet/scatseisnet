"""Test package imports and version detection."""

import sys
import unittest


class TestImport(unittest.TestCase):
    """Test basic package imports."""

    def test_package_import(self):
        """Test that the package can be imported."""
        import scatseisnet
        self.assertIsNotNone(scatseisnet)

    def test_version_exists(self):
        """Test that version string exists."""
        import scatseisnet
        self.assertTrue(hasattr(scatseisnet, '__version__'))
        self.assertIsInstance(scatseisnet.__version__, str)
        self.assertGreater(len(scatseisnet.__version__), 0)

    def test_version_format(self):
        """Test that version follows semantic versioning."""
        import scatseisnet
        version_parts = scatseisnet.__version__.split('.')
        self.assertGreaterEqual(len(version_parts), 2)
        # Check that first parts are numeric
        self.assertTrue(version_parts[0].isdigit())
        self.assertTrue(version_parts[1].isdigit())

    def test_importlib_metadata_available(self):
        """Test that importlib.metadata is available (Python 3.8+)."""
        if sys.version_info >= (3, 8):
            from importlib.metadata import version
            pkg_version = version('scatseisnet')
            self.assertIsInstance(pkg_version, str)

    def test_main_classes_available(self):
        """Test that main classes can be imported."""
        from scatseisnet import ScatteringNetwork
        self.assertIsNotNone(ScatteringNetwork)

    def test_submodules_available(self):
        """Test that submodules are accessible."""
        import scatseisnet
        self.assertTrue(hasattr(scatseisnet, 'network'))
        self.assertTrue(hasattr(scatseisnet, 'wavelet'))
        self.assertTrue(hasattr(scatseisnet, 'operation'))


if __name__ == '__main__':
    unittest.main()
