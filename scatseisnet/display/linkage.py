# coding: utf-8
"""Display features.

Author: Leonard Seydoux
Date: June, 2021
Email: leonard.seydoux@univ-grenoble-alpes.fr
"""
import numpy as np
import pandas as pd

from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from string import ascii_lowercase as letters
from scipy.cluster import hierarchy


COLORS = [
    "0.8",
    "#222222",
    "#F3C300",
    "#875692",
    "#F38400",
    "#A1CAF1",
    "#BE0032",
    "#C2B280",
    "#848482",
    "#008856",
    "#E68FAC",
    "#0067A5",
    "#F99379",
    "#604E97",
    "#F6A600",
    "#B3446C",
    "#DCD300",
    "#882D17",
    "#8DB600",
    "#654522",
    "#E25822",
    "#2B3D26",
]


def get_leaves(dendrogram_info, ax):
    """Get dendrogram list of leaves coordinates and colors.

    Arguments
    ---------
    d: dict
        Output of the scipy.hierarchy.dendrogram function.

    Returns
    -------
    coords, colors: array-like
        The x coordinates and color of each leave.
    """
    # Extract coordinates of each leave (with a depth coordinate indexed 0)
    infos = (key for key in dendrogram_info)
    node_index, node_depth, *_ = (dendrogram_info[key] for key in infos)
    leaves_coordinates = list()
    for index, depth in zip(node_index, node_depth):
        if depth[0] == 0:
            leaves_coordinates.append(index[0])
        if depth[-1] == 0:
            leaves_coordinates.append(index[-1])
    leaves_coordinates = sorted(set(leaves_coordinates))

    # Cardinality
    leaves_population_size = list()
    for label in ax.get_yticklabels():
        label = label.get_text()
        label = label.replace("(", "").replace(")", "")
        population_size = int(label)
        leaves_population_size.append(population_size)

    return leaves_coordinates, leaves_population_size


def get_prediction(linkage, population_size):
    """Get cluster predection for each sample.

    Arguments
    ---------
    linkage: np.ndarray
        Output of the linkage function.
    population_size: list
        The size of every cluster
    """
    indexes_flat = hierarchy.leaves_list(linkage)
    predictions = np.zeros_like(indexes_flat)
    start = 0
    for index, size in enumerate(population_size):
        predictions[indexes_flat[start : start + size]] = index + 1
        start += size
    return predictions


def show_dendrogram(linkage, ax=None, depth=30):
    """Show dendrogram and returns basic cluster informations.

    Arguments
    ---------
    linkage: np.ndarray
        Linkage matrix.

    Keyword arguments
    -----------------
    ax: plt.Axes
        The axes to draw the dendrogram into.
    depth: str
        The dendrogram depth

    Return
    ------
    prediction: np.ndarray
        The cluster prediction per sample.
    """
    # Generate axes
    ax = ax or plt.gca()

    # Show and get dendrogram
    with plt.rc_context({"lines.linewidth": 0.7}):
        dendrogram_infos = hierarchy.dendrogram(
            linkage,
            p=depth,
            truncate_mode="lastp",
            color_threshold=0,
            ax=ax,
            orientation="left",
            above_threshold_color="0.3",
            count_sort=True,
            labels=None,
        )

    # Extract informations
    coordinates, population_sizes = get_leaves(dendrogram_infos, ax)
    predictions = get_prediction(linkage, population_sizes)

    # Plot leave nodes
    node_style = dict(ms=5, mec="0.3", mew=0.7, clip_on=False)
    for coordinate, color in zip(coordinates, COLORS):
        ax.plot(0, coordinate, "o", mfc=color, **node_style)
        index = int((coordinate - 5) / 10) + 1
        label = "{:d}".format(index)
        ax.text(-0.1, coordinate, label, color=color, va="center")

    return predictions


def dendrogram(linkage, times, n_clusters, n_cal_bins=150):

    # Deactivate axes basic properties
    spines_off = {
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.spines.top": False,
        "axes.facecolor": "none",
        "xtick.top": False,
        "ytick.left": False,
    }

    # Generate axes
    gs = dict(width_ratios=[2, 4, 1, 2])
    figsize = 6, n_clusters * 0.35
    with plt.rc_context(spines_off):
        figure_kwargs = dict(sharey=True, figsize=figsize, gridspec_kw=gs)
        figure, axes = plt.subplots(1, 4, **figure_kwargs)

    # Calendar bins
    cal = pd.date_range(times[0], times[-1], n_cal_bins)

    # Show dendrogram
    predictions = show_dendrogram(linkage, ax=axes[0], depth=n_clusters)
    classes = sorted(set(predictions))

    # Show other cluster properties
    for cluster, color in zip(classes, COLORS):

        # Cluster coordinates
        y0 = (cluster - 1) * 10 + 5
        indexes = predictions == cluster

        # Population size
        size = np.sum(predictions == cluster)
        ratio = 100 * size / len(times)

        # Calendar occurrences
        rate, _ = np.histogram(times[indexes], cal)
        rate = 5 * rate / rate.max()
        rate += y0
        axes[1].step(cal[:-1], rate, "k", lw=0.5, where="post")
        axes[1].fill_between(
            cal[:-1], y0, rate, step="post", lw=0, color=color
        )

        # Hourly occurrences
        hours = times[indexes].hour
        hours_counts, _ = np.histogram(hours, np.arange(25))
        hours_counts = 5 * hours_counts / hours_counts.max()
        hours_counts += y0
        axes[2].step(np.arange(24), hours_counts, "k", lw=0.5, where="post")
        axes[2].fill_between(
            np.arange(24), y0, hours_counts, lw=0, step="post", color=color
        )

        # Population graph
        bar_style = dict(height=3, color=color, ec="k", lw=0.5, align="edge")
        text_style = dict(va="center", color=color, size="small")
        text_label = f" {size}"
        axes[-1].barh(y0, ratio, **bar_style)
        axes[-1].text(ratio, y0 + 1.8, text_label, **text_style)

    # Labels dendrogram
    axes[0].set_xlabel("Distance", loc="left")
    axes[0].set_yticklabels([])
    axes[0].yaxis.set_label_position("right")

    # Labels population
    axes[-1].set_yticks(10 * np.arange(len(classes)) + 5)
    axes[-1].set_xlabel("Relative\npopulation size (%)", loc="left")

    # # Labels calendar
    axes[1].set_yticks(10 * np.arange(len(classes)) + 5)
    axes[1].set_xlabel("Calendar date", loc="left")
    dateticks = mdates.AutoDateLocator()
    datelabels = mdates.ConciseDateFormatter(dateticks, show_offset=False)
    axes[1].xaxis.set_major_locator(dateticks)
    axes[1].xaxis.set_major_formatter(datelabels)
    plt.setp(axes[1].get_xticklabels(), rotation="vertical")

    # Labels hourly
    hours_ticks = range(0, 25, 12)
    hours_labels = [f"{h:0d}" for h in hours_ticks]
    axes[2].set_xlim(0, 24)
    axes[2].set_xlabel("Local\ntime (hours)", loc="left")
    axes[2].set_xticks(hours_ticks)
    axes[2].set_xticklabels(hours_labels)

    # All-axes cosmetics
    for ax, letter in zip(axes, letters):
        ax.grid(clip_on=False)
        ax.set_title(letter, loc="left", weight="bold")

    return figure, predictions
