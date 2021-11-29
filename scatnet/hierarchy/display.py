#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Display routines."""

import numpy as np
import os
import seaborn as sns

from . import cluster

from matplotlib import pyplot as plt
from matplotlib import dates as mdates


def set_style(name):
    """Set matplotlib style for the current session.

    This function affects the display codes globally. For a more specific style
    manipulation, the plt.rc_context is more adapted.

    Arguments
    ---------
    name: str
        The style name. This name should be registered in the config repository
        of Matplotlib.

    Returns
    -------
    The returns of the plt.style.use function.
    """
    return plt.style.use(name)


def dateticks(axis):
    """Automatic date formatting for given axes.

    This function wraps the AutoDateLocator and the ConciseDateFormatter
    routines of matplotlib for better code readability.

    Arguments
    ---------
    axis: plt.Axis()
        The axis instance to format with automatic dateticks. This can be for
        instance the currrent x-axis for the current axes (ax.xaxis).
    """
    locator = mdates.AutoDateLocator()
    axis.set_major_locator(locator)
    axis.set_major_formatter(mdates.ConciseDateFormatter(locator))
    pass


def symmetrize(axis):
    """Force symmetric limits for the given axis.

    Arguments
    ---------
    axis: plt.Axis()
        The axis instance to format with automatic dateticks. This can be for
        instance the currrent x-axis for the current axes (ax.xaxis).
    """
    limits = axis.get_view_interval()
    maximum = np.abs(limits).max()
    axis.set_view_interval(-maximum, maximum)
    pass


def save(figure, directory, filename):
    """Save given axes figure in output directory.

    This function behaves similarly than the scat.io.save function for pickle
    files but for images. The output image format can be specified with adding
    an explicit extension.

    Note that the figure is closed at the end of the routine in order to
    prevent large number of opened figures in loops.

    Arguments
    ---------
    figure: plt.Figure()
        The current figure instance.

    directory: str
        The current output directory.

    filename: str
        The figure file name.
    """
    # figure name and save
    filename = os.path.join(directory, f"{filename}")
    figure.savefig(filename)

    # checkout
    # logger.info(f"saved figure at {bold(filename)}")

    # close figure to disable large number of figures in loops
    plt.close(figure)


def show_dendrogram(linkage, threshold, ax=plt.gca(), depth=30):
    """Show dendrogram and returns basic cluster informations.

    Arguments
    ---------
    linkage: np.ndarray
        Output of the linkage function.

    threshold: float
        Threshold value from which the clustering is made.

    Keyword arguments
    -----------------
    ax: plt.Axes
        The axes to draw the dendrogram into.

    depth: str
        The dendrogram depth

    Return
    ------

    """
    # Show and get dendrogram
    with plt.rc_context({"lines.linewidth": 0.7}):
        dendrogram_infos = cluster.hierarchy.dendrogram(
            linkage,
            p=depth,
            truncate_mode="lastp",
            color_threshold=0,
            ax=ax,
            orientation="left",
            above_threshold_color="0.3",
            count_sort=True,
        )

    # Extract informations
    coords, sizes = cluster.get_leaves(dendrogram_infos, ax)
    colors = sns.color_palette("husl", n_colors=len(coords))

    # Get leave indexes
    indexes_flat = cluster.hierarchy.leaves_list(linkage)
    indexes = list()
    i = 0
    for size in sizes:
        indexes.append(indexes_flat[i : i + size])
        i += size

    # Labels
    ax.set_ylim(bottom=2.5)
    ax.set_xlabel("Rescaled distance")
    ax.grid(axis="x")
    ax.tick_params(width=0)
    for side in ax.spines:
        ax.spines[side].set_visible(0)

    # Leaves
    for coord, color in zip(coords, colors):
        ax.plot(0, coord, ".", ms=10, c=color, clip_on=False)

        index = int((coord - 5) / 10) + 1
        label = "{:d} ".format(index)
        ax.text(-0.1, coord, label, color=color, va="center", weight="bold")

    return coords, sizes, colors, indexes


def violin(data, bins, bottom=0, ax=plt.gca(), **kwargs):
    """Handmade violin from fill_between.

    Arguments
    ---------
    x, y: np.ndarray
        The data to violin.

    Keyword arguments
    -----------------
    bottom: float
        The baseline.

    ax: plt.Axes
        The axes to draw into.
    """
    y, x = np.histogram(data, bins)
    # bottom -= 2.5
    if len(y):
        y = 5.0 * y / y.max()
        x = x[:-1]
        kwargs.setdefault("clip_on", False)
        ax.step(x, bottom + y, lw=0.2, where="post", **kwargs)
        ax.fill_between(x, bottom, bottom + y, alpha=1, step="post", **kwargs)


def show_cluster(link, threshold, times, depth=30):
    """Display the main clustering summary.

    Arguments
    ---------
    link:
        The linkage matrix.

    clusters: np.ndarray
        The per-samples cluster attribution.

    times: np.ndarray
        The time indexes

    Returns
    -------
    fig, ax: plt.Figure, plt.Axes
        The matplotlib figure and axes instance.
    """
    # deactivate axes basic properties
    spines_off = {
        "axes.spines.right": False,
        "axes.spines.bottom": False,
        "axes.spines.top": False,
        "axes.facecolor": "none",
        "xtick.top": False,
        "xtick.bottom": False,
    }

    # generate axes
    gs = dict(width_ratios=[2, 3, 1, 2])
    figsize = 7, depth * 0.35
    with plt.rc_context(spines_off):
        fig, ax = plt.subplots(
            1, 4, sharey=True, figsize=figsize, gridspec_kw=gs
        )

    # occurences vectors
    dt = times[1] - times[0]
    calendar = np.linspace(times[0], times[-1], 100)
    daily = np.linspace(0, 24, 24)

    # show dendrogram
    leaves = show_dendrogram(link, threshold, ax=ax[0], depth=depth)

    # loop over clusters
    for clust, size, color, indexes in zip(*leaves):

        # overall duration
        ratio = 100 * size / len(times)
        duration = f" {size}"
        ax[-1].barh(clust, ratio, height=7, color=color)
        ax[-1].text(ratio, clust, duration, color=color, size=6, va="center")

        # occurences
        if len(indexes) > 1:

            # calendar occurence
            violin(times[indexes], calendar, clust, ax[1], color=color)

            # daily occurence
            hours = 24 * (times[indexes] - np.fix(times[indexes]))
            violin(hours, daily, clust, ax=ax[2], color=color)

    # labels
    ax[-1].set_xlabel("Relative size (%)")
    ax[1].set_xlabel("Calendar occurence")
    ax[1].set_ylabel("Normalized detection rate")
    # ax[1].set_yticks(range(len(l)))
    ax[2].set_xlabel("Local time")
    # ax[4].set_xlabel("Frequency (Hz)")
    ax[0].set_title("a", loc="left", weight="bold")
    ax[-1].set_title("d", loc="left", weight="bold")
    ax[1].set_title("b", loc="left", weight="bold")
    ax[2].set_title("c", loc="left", weight="bold")
    # ax[4].set_title("e\n", loc="left", weight="bold")

    # calendar occurence
    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator, show_offset=False)
    ax[1].set_xlim(times.min(), times.max())
    ax[1].xaxis.set_major_locator(locator)
    ax[1].xaxis.set_major_formatter(formatter)
    plt.setp(ax[1].get_xticklabels(), rotation="vertical")

    # daily occurence
    ax[2].set_xlim([0, 24])
    ax[2].set_xticks([0, 6, 12, 18, 24])
    ax[2].set_xticklabels(["00:00", "06:00", "12:00", "18:00", "00:00"])
    plt.setp(ax[2].get_xticklabels(), rotation="vertical")

    # scatterings
    # ax[4].set_xlim(frequencies.min(), frequencies.max())
    # ax[4].set_xscale("log")
    # ax[4].set_xticks([1, 10])

    # grids
    for a in ax[1:]:
        a.grid(axis="x")
    for a in ax:
        a.set_yticklabels([])

    # return
    return fig, ax, leaves


def show_cumulated(times, leaves, clusters):
    """Show cumulated detection curves."""
    fig, ax = plt.subplots(1, figsize=(8, 8))
    for clust, size, color, indexes in zip(*leaves):
        indexes = sorted(indexes)
        cumulated = np.cumsum(np.ones_like(times[indexes]))
        ax.step(times[indexes], cumulated, color=color)

    ax.grid(lw=0.2)
    ax.set_xlim(times.min(), times.max())
    dateticks = mdates.AutoDateLocator()
    ax.xaxis.set_major_locator(dateticks)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(dateticks))
    ax.set_ylabel("Cumulated detections")
    return fig, ax
