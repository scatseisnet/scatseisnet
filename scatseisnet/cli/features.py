# coding: utf-8
"""Command-line module for data inventory.

Author: Leonard Seydoux
Date: June, 2021
Email: leonard.seydoux@univ-grenoble-alpes.fr
"""

import click
import numpy as np
import os
import pickle

from sklearn.decomposition import FastICA as skmodel
from sklearn.metrics import r2_score, mean_squared_error
from .common import common_options

from .. import signal, io
from ..display import show_features


@click.command("features", short_help="Calculate features.")
@common_options
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
    "--medfilt",
    type=int,
    default=101,
    show_default=True,
    help="Median filter kernel size.",
)
def features(
    dimensions,
    normalize=False,
    savepath=None,
    figpath=None,
    filename_network=None,
    filename_reduction=None,
    path_scatterings=None,
    path_features=None,
    show=False,
    medfilt=None,
    **kwargs,
):
    """Reduce scattering domain dimensions."""
    # Path
    dirpath_models = os.path.join(savepath, "models")
    dirpath_scats = os.path.join(savepath, path_scatterings)
    dirpath_features = os.path.join(savepath, path_features)
    dirpath_figure = os.path.join(figpath, "features")

    # Files
    filepath_network = os.path.join(dirpath_models, filename_network)
    filepath_reduction = os.path.join(dirpath_models, filename_reduction)
    filepath_scatterings = os.path.join(dirpath_scats, "scatterings_*.npz")
    filepath_features = os.path.join(dirpath_features, "features_{}_{}.npz")
    filepath_figure = os.path.join(dirpath_figure, "features_{}_{}")

    # Append parameters to filenames
    norm = "norm" if normalize is True else "no-norm"
    filepath_reduction = filepath_reduction.format(dimensions)
    filepath_features = filepath_features.format(dimensions, norm)
    filepath_figure = filepath_figure.format(dimensions, norm)

    if show is True:
        io.mkdir(dirpath_figure)
        show_features(
            filepath_features, filepath_figure, medfilt_kernel=medfilt
        )
    else:
        # Directories
        io.mkdir(dirpath_features)

        # Parameters
        io.stdout("Using {} for scattering coefficients", filepath_scatterings)
        io.stdout("Using {} for features", filepath_features)
        io.stdout("Using {} dimensions", dimensions)
        io.stdout("Using normalization", normalize)

        # Load features
        features, times = io.load_features(filepath_scatterings)

        # Normalize features
        if normalize is True:
            io.stdout("Read newtork from", filepath_network)
            net = pickle.load(open(filepath_network, "rb"))
            for index in range(features.shape[0]):
                feature = signal.reshape_features(features[index], net)
                feature = signal.normalize_features(feature)
                features[index] = signal.vectorize_features(feature)

        # Preprocess
        keep = features.sum(axis=1) > 1e-3
        times = times[keep]
        features = features[keep]
        features = np.log10(features + 1e-3)
        features = (features - features.min()) / (
            features.max() - features.min()
        )

        # Reduce
        print("Performing reduction")
        model = skmodel(n_components=dimensions)
        latents = model.fit_transform(features)
        inversed = model.inverse_transform(latents)
        io.stdout("Mean squared error", mean_squared_error(features, inversed))
        io.stdout("R2 coefficient", r2_score(features, inversed))

        # Save latent variables
        np.savez(filepath_features, times=times, features=latents)
        io.stdout("Saved features at", filepath_features)

        # save model
        pickle.dump(model, open(filepath_reduction, "wb"))
        io.stdout("Saved model at", filepath_reduction)

    pass
