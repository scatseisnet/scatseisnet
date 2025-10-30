"""Test operation module functionality."""

import unittest
import numpy as np
from scatseisnet.operation import pool


class TestPoolOperation(unittest.TestCase):
    """Test the pool operation."""

    def test_pool_basic(self):
        """Test basic pooling operation."""
        data = np.random.randn(100, 128)
        result = pool(data)
        
        self.assertIsInstance(result, np.ndarray)

    def test_pool_with_mean(self):
        """Test pooling with mean reduction."""
        data = np.random.randn(100, 128)
        result = pool(data, reduce_type=np.mean)
        
        self.assertIsInstance(result, np.ndarray)
        # Result should be 1D after pooling
        self.assertEqual(result.ndim, 1)

    def test_pool_with_max(self):
        """Test pooling with max reduction."""
        data = np.random.randn(100, 128)
        result = pool(data, reduce_type=np.max)
        
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.ndim, 1)

    def test_pool_with_median(self):
        """Test pooling with median reduction."""
        data = np.random.randn(100, 128)
        result = pool(data, reduce_type=np.median)
        
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.ndim, 1)

    def test_pool_consistency(self):
        """Test that pooling is consistent."""
        data = np.random.randn(100, 128)
        result1 = pool(data, reduce_type=np.mean)
        result2 = pool(data, reduce_type=np.mean)
        
        self.assertTrue(np.allclose(result1, result2))

    def test_pool_different_shapes(self):
        """Test pooling with different input shapes."""
        shapes = [(50, 64), (100, 128), (200, 256)]
        
        for shape in shapes:
            data = np.random.randn(*shape)
            result = pool(data, reduce_type=np.mean)
            self.assertIsInstance(result, np.ndarray)


if __name__ == '__main__':
    unittest.main()
