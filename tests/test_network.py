"""Test ScatteringNetwork functionality."""

import unittest
import numpy as np
from scatseisnet import ScatteringNetwork


class TestScatteringNetworkCreation(unittest.TestCase):
    """Test ScatteringNetwork creation and initialization."""

    def test_network_creation_single_layer(self):
        """Test creating a single-layer network."""
        network = ScatteringNetwork(
            {'octaves': 4, 'resolution': 2},
            bins=128,
            sampling_rate=100.0
        )
        self.assertEqual(len(network), 1)

    def test_network_creation_multi_layer(self):
        """Test creating a multi-layer network."""
        network = ScatteringNetwork(
            {'octaves': 6, 'resolution': 2},
            {'octaves': 4, 'resolution': 1},
            {'octaves': 2, 'resolution': 1},
            bins=128,
            sampling_rate=100.0
        )
        self.assertEqual(len(network), 3)

    def test_network_attributes(self):
        """Test that network has required attributes."""
        network = ScatteringNetwork(
            {'octaves': 4, 'resolution': 2},
            bins=128,
            sampling_rate=100.0
        )
        
        self.assertTrue(hasattr(network, 'banks'))
        self.assertTrue(hasattr(network, 'bins'))
        self.assertTrue(hasattr(network, 'sampling_rate'))
        self.assertEqual(network.bins, 128)
        self.assertEqual(network.sampling_rate, 100.0)

    def test_network_bins_parameter(self):
        """Test different bin sizes."""
        for bins in [64, 128, 256, 512]:
            network = ScatteringNetwork(
                {'octaves': 4},
                bins=bins,
                sampling_rate=1.0
            )
            self.assertEqual(network.bins, bins)

    def test_network_sampling_rate_parameter(self):
        """Test different sampling rates."""
        for rate in [1.0, 50.0, 100.0, 200.0]:
            network = ScatteringNetwork(
                {'octaves': 4},
                bins=128,
                sampling_rate=rate
            )
            self.assertEqual(network.sampling_rate, rate)


class TestScatteringTransform(unittest.TestCase):
    """Test scattering transform operations."""

    def setUp(self):
        """Set up network for transform tests."""
        self.network = ScatteringNetwork(
            {'octaves': 4, 'resolution': 2},
            {'octaves': 2, 'resolution': 1},
            bins=128,
            sampling_rate=100.0
        )

    def test_transform_segment_basic(self):
        """Test basic segment transformation."""
        segment = np.random.randn(128)
        coefficients = self.network.transform_segment(segment)
        
        self.assertIsInstance(coefficients, list)
        self.assertGreater(len(coefficients), 0)

    def test_transform_segment_with_reduce(self):
        """Test segment transformation with reduction function."""
        segment = np.random.randn(128)
        
        for reduce_func in [np.mean, np.max, np.median]:
            coefficients = self.network.transform_segment(
                segment, 
                reduce_type=reduce_func
            )
            self.assertIsInstance(coefficients, list)
            self.assertGreater(len(coefficients), 0)

    def test_transform_segment_shape(self):
        """Test that output shape is consistent."""
        segment = np.random.randn(128)
        coeffs1 = self.network.transform_segment(segment, reduce_type=np.mean)
        coeffs2 = self.network.transform_segment(segment, reduce_type=np.mean)
        
        # Same input should give same output shape
        self.assertEqual(len(coeffs1), len(coeffs2))

    def test_transform_multiple_segments(self):
        """Test transforming multiple segments."""
        segments = np.random.randn(10, 128)
        coefficients = self.network.transform(segments, reduce_type=np.mean)
        
        self.assertIsInstance(coefficients, list)
        self.assertEqual(len(coefficients), len(self.network))

    def test_transform_consistency(self):
        """Test that same input gives consistent output."""
        segment = np.random.randn(128)
        
        coeffs1 = self.network.transform_segment(segment, reduce_type=np.mean)
        coeffs2 = self.network.transform_segment(segment, reduce_type=np.mean)
        
        # Same input should give same output
        for c1, c2 in zip(coeffs1, coeffs2):
            if isinstance(c1, np.ndarray) and isinstance(c2, np.ndarray):
                self.assertTrue(np.allclose(c1, c2))

    def test_transform_different_inputs(self):
        """Test that different inputs give different outputs."""
        segment1 = np.random.randn(128)
        segment2 = np.random.randn(128)
        
        coeffs1 = self.network.transform_segment(segment1, reduce_type=np.mean)
        coeffs2 = self.network.transform_segment(segment2, reduce_type=np.mean)
        
        # Different inputs should give different outputs
        different = False
        for c1, c2 in zip(coeffs1, coeffs2):
            if isinstance(c1, np.ndarray) and isinstance(c2, np.ndarray):
                if not np.allclose(c1, c2):
                    different = True
                    break
        self.assertTrue(different)


class TestScatteringNetworkEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def test_zero_input(self):
        """Test with zero input."""
        network = ScatteringNetwork(
            {'octaves': 4, 'resolution': 2},
            bins=128,
            sampling_rate=100.0
        )
        segment = np.zeros(128)
        coefficients = network.transform_segment(segment, reduce_type=np.mean)
        
        self.assertIsInstance(coefficients, list)

    def test_constant_input(self):
        """Test with constant input."""
        network = ScatteringNetwork(
            {'octaves': 4, 'resolution': 2},
            bins=128,
            sampling_rate=100.0
        )
        segment = np.ones(128)
        coefficients = network.transform_segment(segment, reduce_type=np.mean)
        
        self.assertIsInstance(coefficients, list)

    def test_large_amplitude(self):
        """Test with large amplitude input."""
        network = ScatteringNetwork(
            {'octaves': 4, 'resolution': 2},
            bins=128,
            sampling_rate=100.0
        )
        segment = np.random.randn(128) * 1000
        coefficients = network.transform_segment(segment, reduce_type=np.mean)
        
        self.assertIsInstance(coefficients, list)
        # Check for no NaN or inf values
        for coeff in coefficients:
            if isinstance(coeff, np.ndarray):
                self.assertFalse(np.any(np.isnan(coeff)))
                self.assertFalse(np.any(np.isinf(coeff)))


if __name__ == '__main__':
    unittest.main()
