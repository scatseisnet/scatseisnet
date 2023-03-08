"""Signal utilities.

Authors: Leonard Seydoux and Randall Balestriero
Email: lseydoux@mit.edu
Date: May, 2022
"""

import numpy as np


def extract_segment(x, window_size, stride=None):
    """Segment array into (possibly overlapping) windows.

    The function operates on the last dimension, e.g., considering an array x
    of shape (a, b, c, d), the function will yield subarrays of dimension
    (a, b, c, d') where d' is of size `window_size`.

    Parameters
    ----------
    x: array_like
        The input array to segment.
    window_size: int
        The number of samples per segment.
    stride: int, optional
        The number of sliding samples between consecutive segments.

    Yields
    ------
    segment: array_like
        A data segment of shape (x.shape[:-1], window_size)
    """
    # Convert sizes
    input_size = x.shape[-1]
    stride_size = stride or window_size

    # Extract and yield segments until bound is reached
    start_index, end_index = 0, window_size
    while end_index <= input_size:
        yield x[..., start_index:end_index]
        start_index += stride_size
        end_index = start_index + window_size


def segmentize(x, window_size, stride=None):
    """Segment a array into (possibly overlapping) windows.

    This function allows to recover all at once the different segments. It
    operates on the last dimension, e.g., considering an array x of shape (a,
    b, c, d), the function will return subarrays of dimension (a, b, c, d', n)
    where d' is of size `window_size` and `n` is the number of batches.

    Parameters
    ----------
    x: array_like
        The input array to segment.
    window_size: int
        The number of samples per segment.
    stride: int, optional
        The number of sliding samples between consecutive segments.

    Returns
    -------
    segments: array_like
        All data segments of shape (x.shape[:-1], window_size, n_windows)
    """
    return np.array([y for y in extract_segment(x, window_size, stride)])


def pool(x, reduce_function= "max"):
    """Pooling operation performed on the last axis.

    Arguments
    ---------
    data: symjax.tensor or np.ndarray
        The input data to pool.

    Keyword arguments
    -----------------
    reduce_type: str
        The reducing operation (default: avg).

    Returns
    -------
    data_pooled: symjax.tensor
        The data pooled with same shape of input data minus last dimension.
    """

    if reduce_type == "avg" :
        return x.mean(axis=-1)
    if reduce_type == "max" :
        return x.max(axis=-1)
    if reduce_type == "med":
        return np.median(x, axis=-1)
    if reduce_type is None:
        return x


def reshape_features(features, net):
    """Extract features from vector features in a single window."""
    # Extract dimensions
    n_filters_per_bank = [bank.shape[0] for bank in net.banks]
    n_features_per_layer = np.cumprod(n_filters_per_bank)
    n_features_per_channel = n_features_per_layer.sum()
    n_channels = features.shape[0] // n_features_per_channel

    # Loop over layers
    reshaped_features = list()
    start = 0
    for layer, n_features in enumerate(n_features_per_layer):
        end = start + n_channels * n_features
        feature = features[start:end]
        feature = feature.reshape(n_channels, *n_filters_per_bank[: layer + 1])
        reshaped_features.append(feature)
        start = end
    return reshaped_features


def normalize_features(features):
    """Normalized higher-order scattering coefficients."""
    n_layers = len(features)
    for layer in range(n_layers - 1):
        for channel in range(features[0].shape[0]):
            features[layer + 1][channel] /= (
                features[layer][channel][:, None] + 1e-5
            )
            # THIS IS FOR TESTING FULL NORM
            # for index, feature in enumerate(features[layer + 1][channel].T):
            #     features[layer + 1][channel][:, index] = (
            #         feature - feature.min()
            #     ) / (feature.max() - feature.min())

            # FULL NORM WITH SUM (PROBA)
            for index, _ in enumerate(features[layer + 1][channel].T):
                features[layer + 1][channel][:, index] /= np.sqrt(
                    features[layer + 1][channel][:, index].sum()
                )

    return features


def vectorize_features(features):
    """Extract features from vector features in a single window."""
    return np.hstack([f.reshape(-1) for f in features])
