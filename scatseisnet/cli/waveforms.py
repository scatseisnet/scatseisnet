# coding: utf-8
"""Command-line module for data inventory.

Author: Leonard Seydoux
Date: June, 2021
Email: leonard.seydoux@univ-grenoble-alpes.fr
"""

import click
import os
import pickle

from .common import common_options
from .transform import load_waveform

from ..io import mkdir, stdout
from ..display import show_waveforms


@click.command("waveforms", short_help="Show waveforms from clustering.")
@common_options
@click.option(
    "--segment",
    type=float,
    default=200.0,
    show_default=True,
    help="Segment duration (seconds).",
)
@click.option(
    "--n_samples",
    type=int,
    default=10,
    show_default=True,
    help="Number of waveforms to show.",
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
def waveforms(
    segment,
    dimensions,
    normalize,
    n_samples,
    savepath=None,
    figpath=None,
    filename_inventory=None,
    filename_network=None,
    path_features=None,
    path_clusters=None,
    **kwargs,
):
    """Transform seismograms into scattering domain."""
    # Path
    dirpath_clusters = os.path.join(savepath, path_clusters)
    dirpath_features = os.path.join(savepath, path_features)
    dirpath_inventory = os.path.join(savepath, "inventories")
    dirpath_figure = os.path.join(figpath, "waveforms", "waveforms_{}_{}")

    # Files
    filepath_features = os.path.join(dirpath_features, "features_{}_{}.npz")
    filepath_clusters = os.path.join(dirpath_clusters, "clusters_{}_{}.npz")
    filepath_inventory = os.path.join(dirpath_inventory, filename_inventory)
    filepath_figure = os.path.join(dirpath_figure, "cluster_*")

    # Append
    norm = "norm" if normalize is True else "no-norm"
    dirpath_figure = dirpath_figure.format(dimensions, norm)
    filepath_features = filepath_features.format(dimensions, norm)
    filepath_clusters = filepath_clusters.format(dimensions, norm)
    filepath_figure = filepath_figure.format(dimensions, norm)

    mkdir(dirpath_figure)
    show_waveforms(
        segment,
        filepath_features,
        filepath_clusters,
        filepath_inventory,
        filepath_figure,
        n_samples=n_samples,
        reader=load_waveform,
        factor=0.8,
    )
    pass
