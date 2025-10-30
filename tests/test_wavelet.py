"""Test wavelet functionality."""

import unittest
import numpy as np
from scatseisnet.wavelet import complex_morlet, ComplexMorletBank


class TestComplexMorletWindow(unittest.TestCase):
    """Test the complex Morlet window function."""

    def test_complex_morlet_basic(self):
        """Test basic complex Morlet window generation."""
        x = np.linspace(-1, 1, 128)
        window = complex_morlet(x, width=0.5, center=0.0)

        self.assertEqual(len(window), len(x))
        self.assertTrue(np.iscomplexobj(window))

    def test_complex_morlet_multiple_widths(self):
        """Test complex Morlet with multiple widths."""
        x = np.linspace(-1, 1, 128)
        widths = np.array([0.3, 0.5, 0.7])
        windows = complex_morlet(x, width=widths, center=0.0)

        self.assertEqual(windows.shape, (len(widths), len(x)))
        self.assertTrue(np.iscomplexobj(windows))

    def test_complex_morlet_symmetry(self):
        """Test that Morlet window is symmetric."""
        x = np.linspace(-1, 1, 128)
        window = complex_morlet(x, width=0.5, center=0.0)

        # The magnitude should be symmetric
        magnitude = np.abs(window)
        self.assertTrue(np.allclose(magnitude, magnitude[::-1], rtol=1e-10))

    def test_complex_morlet_different_centers(self):
        """Test Morlet wavelets with different center frequencies."""
        x = np.linspace(-1, 1, 128)
        window1 = complex_morlet(x, width=0.5, center=0.1)
        window2 = complex_morlet(x, width=0.5, center=0.2)

        # Different centers should give different wavelets
        self.assertFalse(np.allclose(window1, window2))


class TestComplexMorletBank(unittest.TestCase):
    """Test the ComplexMorletBank class."""

    def test_bank_creation(self):
        """Test basic filter bank creation."""
        bank = ComplexMorletBank(bins=128, octaves=4, resolution=2)
        self.assertIsNotNone(bank)
        self.assertEqual(bank.bins, 128)

    def test_bank_attributes(self):
        """Test that filter bank has required attributes."""
        bank = ComplexMorletBank(bins=128, octaves=4, resolution=2)

        self.assertTrue(hasattr(bank, "bins"))
        self.assertTrue(hasattr(bank, "octaves"))
        self.assertTrue(hasattr(bank, "resolution"))
        self.assertTrue(hasattr(bank, "quality"))
        self.assertTrue(hasattr(bank, "sampling_rate"))

    def test_bank_filter_count(self):
        """Test that filter bank has correct number of filters."""
        octaves = 4
        resolution = 2
        bank = ComplexMorletBank(
            bins=128, octaves=octaves, resolution=resolution
        )

        # Number of filters should be octaves * resolution
        expected_filters = octaves * resolution
        self.assertTrue(hasattr(bank, "wavelets"))
        self.assertEqual(len(bank), expected_filters)
        self.assertEqual(bank.wavelets.shape[0], expected_filters)

    def test_bank_different_parameters(self):
        """Test bank creation with different parameters."""
        params = [
            {"bins": 64, "octaves": 3, "resolution": 1},
            {"bins": 128, "octaves": 6, "resolution": 2},
            {"bins": 256, "octaves": 8, "resolution": 4},
        ]

        for param in params:
            bank = ComplexMorletBank(**param)
            self.assertEqual(bank.bins, param["bins"])
            self.assertEqual(bank.octaves, param["octaves"])
            self.assertEqual(bank.resolution, param["resolution"])

    def test_bank_sampling_rate(self):
        """Test bank with different sampling rates."""
        bank1 = ComplexMorletBank(bins=128, octaves=4, sampling_rate=1.0)
        bank2 = ComplexMorletBank(bins=128, octaves=4, sampling_rate=100.0)

        self.assertEqual(bank1.sampling_rate, 1.0)
        self.assertEqual(bank2.sampling_rate, 100.0)

    def test_bank_quality_factor(self):
        """Test bank with different quality factors."""
        bank1 = ComplexMorletBank(bins=128, octaves=4, quality=4.0)
        bank2 = ComplexMorletBank(bins=128, octaves=4, quality=8.0)

        self.assertEqual(bank1.quality, 4.0)
        self.assertEqual(bank2.quality, 8.0)

    def test_transform_returns_real_values(self):
        """Test that transform returns real-valued (not complex) scalograms.
        
        Regression test for issue #19: Scattering coefficients are complex when using cupy.
        The transform should return real values regardless of NumPy or CuPy backend.
        """
        bank = ComplexMorletBank(bins=128, octaves=4, resolution=2)
        
        # Test with random signal
        segment = np.random.randn(128)
        scalogram = bank.transform(segment)
        
        # Check that output is real (not complex)
        self.assertFalse(np.iscomplexobj(scalogram), 
                        "Scalogram should be real-valued, not complex")
        self.assertEqual(scalogram.dtype.kind, 'f',
                        f"Scalogram should have float dtype, got {scalogram.dtype}")
        
        # Test with multiple channels
        segments = np.random.randn(10, 128)
        scalogram = bank.transform(segments)
        
        self.assertFalse(np.iscomplexobj(scalogram),
                        "Multi-channel scalogram should be real-valued, not complex")
        self.assertEqual(scalogram.dtype.kind, 'f',
                        f"Multi-channel scalogram should have float dtype, got {scalogram.dtype}")


if __name__ == "__main__":
    unittest.main()
