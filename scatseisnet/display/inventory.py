# coding: utf-8
"""Display inventory elements.

Author: Leonard Seydoux
Date: June, 2021
Email: leonard.seydoux@univ-grenoble-alpes.fr
"""

import numpy as np

from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from matplotlib import ticker
from string import ascii_lowercase as letters

# from ..inventory import read
from ..io import stdout

plt.rcParams["figure.figsize"] = 5, 5
plt.rcParams["figure.constrained_layout.use"] = True


def show_availability(start, end, ax=plt.gca()):
    """Show the daily data availability along calendar.
    
    Arguments
    ---------
    start: array-like
        Series of starttimes for each segment.
    end: array-like
        Series of endtimes for each segment. Should have same number of
        elements than start.
    ax: plt.Axes, optional
        Axes to use for drawing.
    """
    # Subproducts
    duration_days = end - start
    duration_hour = duration_days * 24
    start_hour = (start - np.fix(start)) * 24

    # Plot
    ax.bar(
        start,
        duration_hour,
        width=duration_days,
        bottom=start_hour,
        align="edge",
        label="Available",
    )

    # Normal duration
    ax.axhspan(0, 24, fc="C0", alpha=0.1, zorder=0, label="Normal")

    # Labels
    ax.legend()
    ax.set_xlabel("Calendar date")
    ax.set_ylabel("Time (H:M)")
    ax.grid(which="both")

    # Y-axis
    y_min = min(0, np.min(start_hour))
    y_max = max(24, np.max(start_hour + duration_hour))
    ax.set_ylim(y_min, y_max)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(base=6))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%02d:00"))

    # X-axis
    dateticks = mdates.AutoDateLocator()
    datelabels = mdates.ConciseDateFormatter(dateticks)
    ax.xaxis.set_major_locator(dateticks)
    ax.xaxis.set_major_formatter(datelabels)

    pass


def show_gaps(start, end, ax=plt.gca()):
    """Show the daily data gaps along calendar.
    
    Arguments
    ---------
    start: array-like
        Series of starttimes for each segment.
    end: array-like
        Series of endtimes for each segment. Should have same number of
        elements than start.
    ax: plt.Axes, optional
        Axes to use for drawing.
    """
    gaps = (start[1:] - end[:-1]).clip(0, None)

    # Show
    ax.bar(
        end[:-1],
        gaps,
        width=gaps,
        bottom=0.1,
        align="edge",
        facecolor="C1",
        label="Gap",
    )

    # Labels
    ax.legend()
    ax.set_xlabel("Calendar date")
    ax.set_ylabel("Gap duration (days)")
    ax.grid(which="both")

    # Indicate typical durations
    x_max = ax.get_xlim()[1]
    y_max = ax.get_ylim()[1]
    durations = {" day": 1, " week": 7, " month": 30, " year": 365}
    text_style = {"va": "center", "color": "0.3"}
    for duration_name, duration_days in durations.items():
        if duration_days < y_max:
            ax.axhline(duration_days, c="0.3", ls="--")
            ax.text(x_max, duration_days, duration_name, **text_style)

    # Y-axis
    ax.set_yscale("log")
    ax.set_ylim(bottom=0.1)

    # X-axis
    dateticks = mdates.AutoDateLocator()
    datelabels = mdates.ConciseDateFormatter(dateticks)
    ax.xaxis.set_major_locator(dateticks)
    ax.xaxis.set_major_formatter(datelabels)


def show_sampling_rate(start, sampling_rate, ax=plt.gca()):
    """Show the number of zeros in segments.
    
    Arguments
    ---------
    start: array-like
        Series of starttimes for each segment.
    sampling_rate: array-like
        Sampling rate for each segment. Should have same number of
        elements than start.
    ax: plt.Axes, optional
        Axes to use for drawing.
    """
    # Show
    ax.step(start, sampling_rate, where="post", c="C3")
    ax.fill_between(start, 0, sampling_rate, step="post", fc="C3", alpha=0.2)

    # Labels
    ax.set_ylabel("Sampling rate (Hz)")
    ax.set_xlabel("Calendar date")
    ax.grid(which="both")

    # Y-axis
    ax.set_ylim(bottom=0)

    # X-axis
    dateticks = mdates.AutoDateLocator()
    datelabels = mdates.ConciseDateFormatter(dateticks)
    ax.xaxis.set_major_locator(dateticks)
    ax.xaxis.set_major_formatter(datelabels)


def show_zeros(start, zeros, ax=plt.gca()):
    """Show the number of zeros in segments.
    
    Arguments
    ---------
    start: array-like
        Series of starttimes for each segment.
    zeros: array-like
        Number of zeros for each segment. Should have same number of
        elements than start.
    ax: plt.Axes, optional
        Axes to use for drawing.
    """
    # Show
    ax.step(start, zeros, where="post", c="C2")
    ax.fill_between(start, 0, zeros, step="post", fc="C2", alpha=0.2)

    # Labels
    ax.set_ylabel("Number of zeros")
    ax.set_xlabel("Calendar date")
    ax.grid(which="both")

    # Y-axis
    ax.set_yscale("log")

    # X-axis
    dateticks = mdates.AutoDateLocator()
    datelabels = mdates.ConciseDateFormatter(dateticks)
    ax.xaxis.set_major_locator(dateticks)
    ax.xaxis.set_major_formatter(datelabels)


def show_npts(start, npts, ax=plt.gca()):
    """Show the number of zeros in segments.
    
    Arguments
    ---------
    start: array-like
        Series of starttimes for each segment.
    zeros: array-like
        Number of zeros for each segment. Should have same number of
        elements than start.
    ax: plt.Axes, optional
        Axes to use for drawing.
    """
    # Show
    npts = np.array(npts)
    for npt in npts.T:
        ax.step(start, npt, where="post", c="C5")
        ax.fill_between(start, 0, npt, step="post", fc="C5", alpha=0.2)

    # Labels
    ax.set_ylabel("Number of points")
    ax.set_xlabel("Calendar date")
    ax.grid(which="both")

    # Y-axis
    ax.set_yscale("log")

    # X-axis
    dateticks = mdates.AutoDateLocator()
    datelabels = mdates.ConciseDateFormatter(dateticks)
    ax.xaxis.set_major_locator(dateticks)
    ax.xaxis.set_major_formatter(datelabels)


def show_main(start, end, zeros, sampling_rate, npts):
    """Show different elements of inventory."""
    # Create figure
    figure, axes = plt.subplots(5, sharex=True, figsize=(5, 6))

    # Plot
    show_availability(start, end, axes[0])
    show_gaps(start, end, axes[1])
    show_zeros(start, zeros, axes[2])
    show_sampling_rate(start, sampling_rate, axes[3])
    show_npts(start, npts, axes[4])

    # Common labels
    dateticks = mdates.AutoDateLocator()
    datelabels = mdates.ConciseDateFormatter(dateticks)
    for letter, axe in zip(letters, axes):
        axe.xaxis.set_major_locator(dateticks)
        axe.xaxis.set_major_formatter(datelabels)
        axe.set_xlabel("")
        axe.set_title(letter, loc="left")
    axes[-1].set_xlabel("Calendar date", loc="left")

    return figure


def get_all_subkeys(dictionnary, subkey):
    """Get all sub entries of a dictionnary with given subkey."""
    subvalues = [dictionnary[key][subkey] for key in dictionnary.keys()]
    return subvalues


def show_inventory(database, file_figure):
    """Show inventory and save figure.
    
    Arguments
    ---------
    database: dict
        The inventory.
    file_figure:
        The figure file.
    """
    start = get_all_subkeys(database, "date_start")
    end = get_all_subkeys(database, "date_end")
    zeros = get_all_subkeys(database, "n_zeros")
    sampling_rate = get_all_subkeys(database, "sampling_rate")
    npts = get_all_subkeys(database, "n_pts")
    start = mdates.date2num(start)
    end = mdates.date2num(end)

    # Make and save figure
    fig = show_main(start, end, zeros, sampling_rate, npts)
    fig.savefig(file_figure)
    stdout("Figure saved at", file_figure)

