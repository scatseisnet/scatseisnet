# coding: utf-8
"""Calculate scattering transform on segmented time series."""

import click
import numpy as np
import os
import pickle

from dateutil import tz
from matplotlib import dates as mdates

from .common import common_options

from .. import hierarchy
from ..display import dendrogram
from ..io import stdout, mkdir


@click.command("linkage", short_help="Calculate linkage matrix.")
@common_options
@click.option(
    "--method",
    type=click.Choice(("single", "centroid", "median", "ward")),
    default="ward",
    help="Number of clusters splits.",
)
@click.option(
    "--dimensions",
    default=10,
    show_default=True,
    help="Number of latent space dimensions.",
    type=int,
)
@click.option(
    "--normalize",
    is_flag=True,
    default=False,
    show_default=True,
    help="Normalization flag.",
)
@click.option(
    "--n_clusters",
    "-n",
    type=int,
    default=10,
    show_default=True,
    help="Number of clusters.",
)
@click.option(
    "--time-zone",
    default="Mexico/General",
    type=str,
    show_default=True,
    help="Time zone for local time histogram.",
)
def linkage(
    method,
    n_clusters,
    dimensions,
    normalize,
    time_zone,
    path_features=None,
    path_clusters=None,
    savepath=None,
    figpath=None,
    show=False,
    **kwargs,
):
    # Path
    dirpath_clusters = os.path.join(savepath, path_clusters)
    dirpath_features = os.path.join(savepath, path_features)

    # Files
    filepath_features = os.path.join(dirpath_features, "features_{}_{}.npz")
    filepath_linkage = os.path.join(dirpath_clusters, "linkage_{}_{}.npz")
    filepath_clusters = os.path.join(dirpath_clusters, "clusters_{}_{}.npz")
    filepath_dendrogram = os.path.join(figpath, "dendrogram_{}_{}.png")

    # Append
    norm = "norm" if normalize is True else "no-norm"
    filepath_features = filepath_features.format(dimensions, norm)
    filepath_linkage = filepath_linkage.format(dimensions, norm)
    filepath_clusters = filepath_clusters.format(dimensions, norm)
    filepath_dendrogram = filepath_dendrogram.format(dimensions, norm)

    if show is True:
        mkdir(figpath)
        linkage = pickle.load(open(filepath_linkage, "rb"))
        stdout("Loaded linkage matrix from", filepath_linkage)
        with np.load(filepath_features) as data:
            timestamps = data["times"]
        times = np.array(mdates.num2date(timestamps, tz=tz.gettz(time_zone)))

        # Show dendrogram
        fig, predictions = dendrogram(linkage, times, n_clusters)
        fig.savefig(filepath_dendrogram)
        stdout("Saved figure at", filepath_dendrogram)

        # Save predictions
        np.savez(filepath_clusters, predictions=predictions, times=timestamps)
        stdout("Saved predictions at", filepath_clusters)

    else:
        mkdir(dirpath_clusters)

        # Load features
        with np.load(filepath_features) as data:
            features = data["features"]
        stdout("Features loaded from", filepath_features)

        # Calculate and save linkage
        linkage = hierarchy.linkage(features, method)
        pickle.dump(linkage, open(filepath_linkage, "wb"))
        stdout("Saved linkage matrix at", filepath_linkage)
