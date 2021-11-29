# coding: utf-8
"""Signal utilities.

Authors: Leonard Seydoux and Randall Balestriero
Email: leonard.seydoux@univ-grenoble-alpes.fr
Date: May, 2021
"""

import numpy as np


def segment(x, window_size, stride=None):
    """Segment a given array into (possibly overlapping) windows.

    Arguments
    ---------
    x: :class:`np.ndarray`
        The input array to segment.
    
    window_size: int
        The size of the sliding window.
    
    stride: int, optional
        The number of bins to slide the window with.
    
    Yields
    ------
    The segmented array with shape.
    """
    bins = x.shape[-1]
    index = 0
    stride = window_size if stride is None else stride
    while (index + window_size) <= bins:
        yield x[..., index : index + window_size]
        index += stride


def segmentize(x, window_size, stride=None):
    """Segment a given array into (possibly overlapping) windows.

    Arguments
    ---------
    x: :class:`np.ndarray`
        The input array to segment.
    
    window_size: int
        The size of the sliding window.
    
    stride: int, optional
        The number of bins to slide the window with.
    
    Returns
    -------
    The segmented array with shape (n_windows, n_channels, n_times).
    """
    return np.array([x for x in segment(x, window_size, stride)])


def pool(x, reduce_type="avg"):
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
    if reduce_type == "avg":
        return x.mean(axis=-1)
    if reduce_type == "max":
        return x.max(axis=-1)
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
