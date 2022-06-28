# coding: utf-8
"""Display features.

Author: Leonard Seydoux
Date: June, 2021
Email: leonard.seydoux@univ-grenoble-alpes.fr
"""
import nmmn.plots
import numpy as np
import pickle

from matplotlib import dates as mdates
from matplotlib import pyplot as plt

from .. import inventory
from .. import signal
from ..io import load_feature_file, stdout

plt.rcParams["figure.constrained_layout.use"] = True


def show(t, x, sx, net, timestamp, channel=1):

    # Create figure
    fig, ax = plt.subplots(3, figsize=(5, 6))

    # Metadata
    sampling_rate = net.sampling_rate
    freq = [bank.centers(sampling_rate) for bank in net.banks]

    # Log-transformatino
    sx = np.log10(sx + 1)
    scats_0, scats_1 = signal.reshape_features(sx, net)

    # show single window
    sx1 = np.squeeze(scats_1[channel]).T
    # cmap = nmmn.plots.wolframcmap()
    cmap = "Spectral_r"
    img = ax[0].pcolormesh(freq[0], freq[1], sx1[:-1, :-1], cmap=cmap)
    ax[0].set_xscale("log")
    ax[0].set_yscale("log")
    ax[0].set_xlim(freq[0].min(), freq[0].max())
    ax[0].set_ylim(freq[1].min(), freq[1].max())
    ax[0].set_xlabel("First-order frequency (Hz)")
    ax[0].set_ylabel("Second-order frequency (Hz)")
    ax[0].grid()
    ax[0].set_title("a", loc="left")

    cb = plt.colorbar(img, ax=ax[0], aspect=10)
    cb.set_label("Second-order\nscattering coefficients")

    # show first-oder scatterings
    ax[1].step(freq[0], scats_0[channel], where="post")
    ax[1].fill_between(freq[0], 0, scats_0[channel], alpha=0.2, step="post")
    ax[1].set_ylim(bottom=0, top=40)
    ax[1].set_xscale("log")
    ax[1].set_xlim(freq[0].min(), freq[0].max())
    ax[1].set_xlabel("First-order frequency (Hz)")
    ax[1].grid(which="both")
    ax[1].set_ylabel("First-order\nscattering coefficients")
    ax[1].set_title("b", loc="left")

    # show single window
    ax[2].plot(t, x[channel], "k")
    dateticks = mdates.AutoDateLocator()
    datelabels = mdates.ConciseDateFormatter(dateticks)
    ax[2].xaxis.set_major_locator(dateticks)
    ax[2].xaxis.set_major_formatter(datelabels)
    ax[2].set_xlim(t.min(), t.max())
    ax[2].set_ylim(-1, 1)
    ax[2].axvline(
        timestamp, c="C1", zorder=0, lw=4, alpha=0.4, label="Timestamp"
    )
    ax[2].legend()
    ax[2].grid()
    ax[2].set_ylabel("Amplitude")
    ax[2].set_title("c", loc="left")

    return fig


def show_scatterings(
    file_features,
    file_inventory,
    file_network,
    file_figure,
    timestamp,
    step,
    reader=None,
):
    """Show features on given time stamp."""
    # Read inventory
    tags, paths, start, end, _ = inventory.read(file_inventory)
    start, end = mdates.datestr2num(np.vstack((start, end)))

    # Get closest path to timestamp
    timestamp = mdates.date2num(timestamp)
    timestamp_index = np.searchsorted(start, timestamp) - 1
    timestamp_index = 0 if timestamp_index < 0 else timestamp_index
    path = paths[timestamp_index]
    tag = tags[timestamp_index]
    file_features = file_features.replace("*", tag)
    file_figure = file_figure.replace("*", tag)

    # load network
    net = pickle.load(open(file_network, "rb"))
    stdout("Loaded scatterings network from", file_network)
    bins = net.banks[0].bins

    # load features
    scatterings, scattering_times = load_feature_file(file_features)
    stdout("Loaded scatterings from", file_features)

    # Read seismograms
    stream = reader(path)
    stdout("Loaded seismogram from", path)
    times = stream[0].times("matplotlib")
    seismograms = [trace.data for trace in stream]
    npts = min((len(trace) for trace in seismograms))
    seismograms = np.array([component[:npts] for component in seismograms])
    times = times[:npts]
    step = int(step * stream[0].stats.sampling_rate)
    seismograms = signal.segmentize(seismograms, bins, step)
    times = signal.segmentize(times, bins, step)

    # Find corresponding window index
    window_index = np.searchsorted(scattering_times, timestamp) - 1
    window_index = 0 if window_index < 0 else window_index

    # select window
    scatterings = scatterings[window_index]
    t = times[window_index]
    x = seismograms[window_index]
    x = 0.9 * x / (np.abs(x).max() + 1e-5)

    # Reshape features
    sx = signal.reshape_features(scatterings, net)
    sx = signal.normalize_features(sx)
    sx = signal.vectorize_features(sx)

    # show
    show(t, x, sx, net, timestamp).savefig(file_figure)
    stdout("Saved figure at", file_figure + ".png")

