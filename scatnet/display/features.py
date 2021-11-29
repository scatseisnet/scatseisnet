# coding: utf-8
"""Show selected features in time and latent spaces."""

import nmmn.plots
import numpy as np
import os

from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from scipy.stats import median_abs_deviation
from scipy.signal import medfilt

from ..io import stdout


def demad(x, factor=10.0):
    """Normalize signal with median absolute deviation.
    
    Arguments
    ---------
    x: np.ndarray
        The input signal.
    factor: float, optional
        An additional normalization factor.
    
    Returns
    -------
    The data normalized with median absolute deviation.
    """
    mad = median_abs_deviation(x)
    return x / np.mean(mad) / factor


def show_time(times, features, factor=0.4, medfilt_kernel=101):
    """Latent variables in time domain."""
    # Preprocess
    features = features.T
    features = demad(features)
    n_features, n_bins = features.shape

    # Figure
    fig, ax = plt.subplots(1, figsize=(5, 7))

    # Show
    for index, feature in enumerate(features):
        color = f"C{index % 3}"
        feature += index + 1
        feature_filtered = medfilt(feature, medfilt_kernel)
        ax.plot(times, feature, ".", ms=1, alpha=0.5, mew=0, color=color)
        ax.plot(times, feature_filtered, lw=0.7, color=color)

    # Labels
    ax.grid()
    ax.set_ylim(0, n_features + factor)
    ax.set_yticks(np.arange(n_features) + 1)
    ax.set_ylabel("Independant component index")

    # Date labels
    dateticks = mdates.AutoDateLocator()
    datelabels = mdates.ConciseDateFormatter(dateticks)
    ax.xaxis.set_major_locator(dateticks)
    ax.xaxis.set_major_formatter(datelabels)
    ax.set_xlim(times.min(), times.max())

    # Remove borders
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)

    return fig


def show_latent(features, cmap=nmmn.plots.wolframcmap(), nbins=800):
    """Latent variables in versus diagram."""
    # Preprocess
    features = features.T
    features = demad(features)
    n_features = features.shape[0] - 1

    # Figure
    figsize = 2 * [n_features]
    gridspec_kw = dict(hspace=0.1, wspace=0.1)
    fig, ax = plt.subplots(
        n_features,
        n_features,
        figsize=figsize,
        gridspec_kw=gridspec_kw,
        constrained_layout=False,
        sharex="col",
        sharey="row",
    )

    # Versus diagrams
    for i in range(n_features):

        x = features[i]
        x_min, x_max = x.min(), x.max()
        x_bins = np.linspace(x_min, x_max, nbins)

        for j in range(0, n_features):

            y = features[j + 1]
            y_min, y_max = y.min(), y.max()
            y_bins = np.linspace(y_min, y_max, nbins)

            # Lower triangular
            if j >= i:

                # Histogram
                counts, _, _ = np.histogram2d(x, y, (x_bins, y_bins))
                counts = counts.T
                counts[counts == 0] = 1e-4
                counts = np.log(counts)
                extent = [x_min, x_max, y_min, y_max]
                ax[j, i].imshow(
                    counts, cmap=cmap, extent=extent, aspect="auto"
                )
                ax[j, i].grid()
                ax[j, i].set_xticks([])
                ax[j, i].set_yticks([])
                ax[j, i].set_ylim(y_min, y_max)
                ax[j, i].set_xlim(x_min, x_max)

                # Style
                for side in ax[j, i].spines:
                    ax[j, i].spines[side].set_visible(False)

            # Upper triangular
            else:
                ax[j, i].set_axis_off()

            # Labels
            if j == n_features - 1:
                ax[j, i].set_xlabel(f"Latent {i + 1}")
            if i == 0:
                ax[j, i].set_ylabel(f"Latent {j + 2}")

    return fig


def show_features(file_features, file_figure, medfilt_kernel=101):

    # Basename
    basename = os.path.basename(file_features)
    basename = basename.split(".")[0]

    # Load features
    with np.load(file_features) as data:
        features = data["features"]
        times = data["times"]
    stdout("Loaded features from", file_features)

    # Show in time and save
    fig = show_time(times, features, medfilt_kernel=medfilt_kernel)
    print("figure created")
    file_figure_time = file_figure + "_time.png"
    fig.show()
    fig.savefig(file_figure_time, dpi=600)
    print("figure saved")
    stdout("Figure saved at", file_figure_time)

    # Show in latent space and save
    fig = show_latent(features)
    file_figure_space = file_figure + "_space.png"
    fig.savefig(file_figure_space)
    stdout("Figure saved at", file_figure_space)

