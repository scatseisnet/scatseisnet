# coding: utf-8
"""Command-line module for data inventory.

Author: Leonard Seydoux
Date: June, 2021
Email: leonard.seydoux@univ-grenoble-alpes.fr
"""

import click
import numpy as np
import obspy
import os
import pandas as pd
import pickle

from matplotlib import dates as mdates
from obspy import read, Stream, UTCDateTime
from tqdm import tqdm

from .common import common_options

from .. import inventory, signal, Network, io
from ..display import show_scatterings


# def load_waveform(path, trim=None):
#     """Waveform reader."""
#     stream = read(path)
#     if trim is not None:
#         stream.trim(*trim)
#     stream.merge(method=1, fill_value="interpolate")
#     stream.detrend()
#     stream.decimate(5)
#     stream.filter(type="highpass", freq=5.0)
#     stream.taper(max_percentage=0.05)
#     return stream


def load_waveform(paths):

    stream = obspy.Stream()
    for path in paths:
        stream += obspy.read(path)
    stream.detrend("linear")
    stream.merge(method=1)
    stream.detrend("linear")
    stream.decimate(4)
    stream.detrend("linear")
    stream.filter(type="highpass", freq=1)
    starttime = max([tr.stats.starttime for tr in stream])
    endtime = min([tr.stats.endtime for tr in stream])
    stream.trim(starttime, endtime, fill_value=0)
    return stream


@click.command("transform", short_help="Calculate scattering coefficients.")
@common_options
@click.option(
    "--segment",
    type=float,
    default=200.0,
    show_default=True,
    help="Segment duration (seconds).",
)
@click.option(
    "--step",
    type=float,
    default=100.0,
    show_default=True,
    help="Step duration (seconds).",
)
@click.option(
    "--pooling",
    "-p",
    type=click.Choice(("max", "avg", "med")),
    default="max",
    show_default=True,
    help="Pooling type.",
)
@click.option(
    "--octaves",
    "-j",
    multiple=True,
    default=[4, 10],
    show_default=True,
    help="Number of octaves per layer.",
)
@click.option(
    "--resolution",
    "-q",
    multiple=True,
    default=[2, 2],
    show_default=True,
    help="Number of wavelets per octaves per layer.",
)
@click.option(
    "--quality",
    "-d",
    multiple=True,
    default=[2, 2],
    show_default=True,
    help="Quality factor per layer.",
)
@click.option(
    "--timestamp",
    type=click.DateTime(),
    default=None,
    help="Dislay given timestamp (show must be on).",
)
@click.option(
    "--reader",
    type=str,
    default="reader.py",
    help="Module where the load function is defined.",
)
def transform(
    segment,
    step,
    pooling,
    octaves,
    resolution,
    quality,
    savepath=None,
    filename_inventory=None,
    filename_network=None,
    path_scatterings=None,
    start=None,
    end=None,
    reader=None,
    **kwargs,
):
    """Transform seismograms into scattering domain."""
    # Directories
    dirpath_inventory = os.path.join(savepath, "inventories")
    dirpath_models = os.path.join(savepath, "models")
    dirpath_scats = os.path.join(savepath, path_scatterings)

    # Files
    filepath_network = os.path.join(dirpath_models, filename_network)
    filepath_inventory = os.path.join(dirpath_inventory, filename_inventory)
    filepath_scatterings = os.path.join(dirpath_scats, "scatterings_*.npz")

    # Directories
    io.mkdirs(dirpath_models, dirpath_scats)

    # Parameters
    io.stdout("Using {} for scattering coefficients", filepath_scatterings)
    io.stdout("Using {} sec windows with {} sec step", (segment, step))
    io.stdout("Using {} octaves", list(octaves))
    io.stdout("Using {} resolutions", list(resolution))
    io.stdout("Using {} quality factors", list(quality))
    io.stdout("Using {} pooling", pooling)

    # Read inventory
    database = inventory.read(filepath_inventory)

    # Trim database
    start = pd.to_datetime(start, errors="coerce")
    end = pd.to_datetime(end, errors="coerce")
    if not pd.isna(start):
        database = database[database.starttime > start]
    if not pd.isna(end):
        database = database[database.starttime < end]

    # Initialize progress bar with reading waveforms list
    progress_bar = tqdm(database.groupby("tag"))

    # Transform loop
    for tag, db in progress_bar:

        # Extract streams
        paths = db.path
        stream = load_waveform(paths)

        # Init nertwork
        if 0 in db.index:
            sampling_rate = stream[0].stats.sampling_rate
            bins = int(segment * sampling_rate)
            net = Network(octaves, resolution, quality, bins, sampling_rate)
            pickle.dump(net, open(filepath_network, "wb"))
            io.stdout("Saved network at", filepath_network)

        # Update progress bar description with current file
        progress_bar.set_description(f"Process {tag}")

        # Turn into array
        npts = np.unique([len(tr) for tr in stream])
        if len(npts) > 1:
            continue
        times = stream[0].times("matplotlib")
        seismograms = np.array([trace.data for trace in stream])
        # npts = min((len(trace) for trace in seismograms))
        # seismograms = np.array([channel[:npts] for channel in seismograms])
        # times = times[:npts]

        # Extract segments
        if npts < bins:
            continue
        slide = int(step * sampling_rate)
        seismograms = signal.segmentize(seismograms, bins, slide)
        times = signal.segmentize(times, bins, slide)[:, 0]

        # Scattering Network
        features = net.transform(seismograms, pooling)

        # Save features
        file_features = filepath_scatterings.replace("*", tag)
        features = {f"features_{i}": f for i, f in enumerate(features)}
        np.savez(file_features, times=times, **features)

    pass


def get_all_subkeys(dictionnary, subkey):
    """Get all sub entries of a dictionnary with given subkey."""
    subvalues = [dictionnary[key][subkey] for key in dictionnary.keys()]
    return subvalues
