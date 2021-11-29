# coding: utf-8
"""Deep scattering transform on segmented time series.

Authors: Leonard Seydoux and Randall Balestriero
Email: leonard.seydoux@univ-grenoble-alpes.fr
Date: May, 2021
"""


import argparse
import click
import glob
import json
import logging
import numpy as np
import os

from pathlib import Path

FILE_ARGUMENTS = "arguments.json"


def stdout(message, value):
    """Format message with click echo and style.
    
    Arguments
    ---------
    message: str
        The message to use as a base string with {} variables.
    value: str
        The values to put in place of the {}.
    """
    # Happend curly brackets if not
    if "{" not in message:
        message = message + " {}"

    # Turn into tuple for allowing several values
    if not isinstance(value, tuple):
        values = (value,)
    else:
        values = value

    # Format
    values = [click.style(value, bold=True) for value in values]
    message = message.format(*values)

    # Echo
    click.echo(message)
    pass


def mkdir(dirpath):
    """Create directory.
    
    Arguments:
    ----------
    dirpath: str
        Path to the directory to create.
    """
    if not os.path.exists(dirpath):
        Path(dirpath).mkdir(parents=True, exist_ok=True)
        stdout("Created directory", dirpath)
    else:
        stdout("Using existing directory", dirpath)
    pass


def mkdirs(*args):
    """Create directories.
    
    Arguments:
    ----------
    dirpaths: tuple or list
        Paths to the directories to create.
    """
    for dirpath in args:
        mkdir(dirpath)


def parse(init=False):
    """Command-line argument parser.

    The usage and help for every command-line arguments for the main program is
    avaialbe from the main running script:

        python main.py -h

    assuming that the main.py script implements at least the following lines:

        import scat
        scat.parse()

    Keyword arguments
    -----------------
    readonly: bool
        A safe switch to use in order to prevent from erasing the data.

    Returns
    -------
    args: :class:`scat.argparse.Namespace`
        The parsed arguments.

    reader: module
        The imported data reading module.
    """

    # Instanciate parser with description and module's docstring.
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Logging level.
    parser.add_argument(
        "--log",
        default="INFO",
        metavar="LEVEL",
        choices=["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="""Logging level. The level name can either be NOTSET, DEBUG,
        INFO, WARNING (default), ERROR or CRITICAL. Please visit
        https://docs.python.org/3/howto/logging.html for further info.""",
    )

    # Output directory.
    parser.add_argument(
        "--outdir",
        metavar="PATH",
        type=str,
        default="out/case",
        help="""Specify output directory path. The directory should exist
        already.""",
    )

    # Window duration
    parser.add_argument(
        "--segment",
        metavar="DURATION",
        type=float,
        default=1800.0,
        help="""Segment duration in seconds. A default window duration of 20
        seconds is set, but this argument should be considered as a required
        argument. This segment also defines the pooling size, since the pooling
        is performed over the full segment duration.""",
    )

    # Window step
    parser.add_argument(
        "--step",
        metavar="DURATION",
        type=float,
        default=900.0,
        help="""Segment step in seconds. This defines the time interval between
        the starting time of two consecutive segments. The clustering
        performances with respect to the step is still under debate. for
        cleaner results, the step should be set with the segment duration.""",
    )

    # Number of octaves at each layer
    parser.add_argument(
        "--octaves",
        type=int,
        default=[7, 12],
        nargs="+",
        metavar="J",
        help="""Number of octaves for each scattering layer. The number of
        octaves define the freequency extent of each layer. The number of
        octaves is defined from the Nyquist frequency. The scattering network
        depth depends on the length of this list.""",
    )

    # Number of filter per octaves at each layer
    parser.add_argument(
        "--resolution",
        type=int,
        default=[6, 1],
        nargs="+",
        metavar="Q",
        help="""Number of wavelets per octaves for each scattering layer. This
        define the frequency resolution of each scattering layer, and
        consequently, the representation density. Note that the length of this
        argument must be the same that the number of octaves.""",
    )

    # Wavelet banks quality factors
    parser.add_argument(
        "--quality",
        type=int,
        default=[1, 1],
        nargs="+",
        metavar="Qc",
        help="""Wavelet bank qulity factor. This defines the ratio bewteen
        the center frequency qnd the frequency bandwitdh, and therefore
        represents the selectivity of the filter, or quality. It allows to
        choose the density level of each representation.""",
    )

    # Pooling type
    parser.add_argument(
        "--pooling",
        metavar="TYPE",
        type=str,
        default="max",
        choices=["max", "avg"],
        help="""Pooling reduction operation. The pooling is performed on a
        the duration of a full segment. By default, the maximum pooling
        is performed (choices: max or avg).""",
    )

    # Waveform inventory
    parser.add_argument(
        "--inventory",
        metavar="PATH",
        type=str,
        default="INVENTORY",
        help="""Waveform inventory to read with obspy.""",
    )

    # Features files
    parser.add_argument(
        "--file_features",
        metavar="PATH",
        type=str,
        default="out/case/features/*.npz",
        help="""Path to features, where the wildcard is replaced by the
        tag.""",
    )

    # Network file
    parser.add_argument(
        "--file_network",
        metavar="PATH",
        type=str,
        default="out/case/models/network.pickle",
        help="""Path to network pickle file for saving.""",
    )

    if parser.prog == "make_latent.py":

        parser.add_argument(
            "dim",
            metavar="DIM",
            type=int,
            default=10,
            help="""Latent space dimensions.""",
        )

        parser.add_argument(
            "--file_latent",
            metavar="PATH",
            type=str,
            default="out/case/latent/latent.npz",
            help="""Path to latent file for saving.""",
        )

        parser.add_argument(
            "--file_reduction",
            metavar="PATH",
            type=str,
            default="out/case/model/reduce.pickle",
            help="""Path to reduction model pickle file for saving.""",
        )

        parser.add_argument(
            "--normalize",
            metavar="NORM",
            type=int,
            default=0,
            help="""If 1, the higher-order scatterings are normalized.""",
        )

    if parser.prog == "make_cluster.py":

        parser.add_argument(
            "--depth",
            metavar="depth",
            type=int,
            default=40,
            help="""Number of dendrogram splits.""",
        )

        parser.add_argument(
            "--threshold",
            metavar="THRESHOLD",
            type=float,
            default=0.5,
            help="""Threshold for cluster definition.""",
        )

        parser.add_argument(
            "--distance",
            metavar="distance",
            type=str,
            default="ward",
            help="""Method to calculate clusters.""",
        )

        parser.add_argument(
            "--file_leaves",
            metavar="FILE_LEAVES",
            type=str,
            default="out/case/model/leaves.pickle",
            help="""Save file for leaves.""",
        )

        parser.add_argument(
            "--file_clustering",
            metavar="FILE_CLUSTERING",
            type=str,
            default="out/case/model/clusters.pickle",
            help="""Save file for clusters.""",
        )

        parser.add_argument(
            "--file_latent",
            metavar="PATH",
            type=str,
            default="out/case/latent/latent.npz",
            help="""Path to latent file for saving.""",
        )

        parser.add_argument(
            "--file_linkage",
            metavar="PATH",
            type=str,
            default="out/case/cluster/linkage.pickle",
            help="""Path to linkage file for saving.""",
        )

        parser.add_argument(
            "--linkage",
            metavar="linkage",
            type=int,
            default=1,
            help="""Recalculate linkage.""",
        )
    # Parse command-line arguments
    args = parser.parse_args()

    # Set logging
    logging.basicConfig(format="[%(levelname)s] %(message)s", level=args.log)
    logging.info(f"Logging level set to {args.log}")

    if init == True:
        args = parser.parse_args()
        save_arguments(args)
        return args

    else:
        return load_arguments(args)


def save_arguments(args, skip=["log"]):
    """Save arguments.

    The input arguments out of the parser function are saved into a JSON file
    format in order to ensure readability by the user.

    Arguments
    ---------
    args: :class:`scat.argparse.Namespace`
        The argument to save.

    skip: list
        A list of arguments not to save. Useful for avoiding saved arguments
        to overwrite new arguments in later runs like log or mode.
    """
    # Filename
    json_filename = os.path.join(args.outdir, FILE_ARGUMENTS)

    # Skip arguments from the list that are not to be saved
    args_dict = args.__dict__.copy()
    for arg_skip in skip:
        args_dict.pop(arg_skip)

    # Save
    with open(json_filename, "w") as json_file:
        json.dump(args_dict, json_file, indent=4)

    # Logging checkpoint
    logging.info("Saved arguments at {}".format(json_filename))
    pass


def load_arguments(args=argparse.Namespace(), filename=None):
    """Load arguments.

    This function allows to update the arguments pre-loaded by the parser from
    a JSON file previously saved with the save_arguments function. It allows to
    recover a set of arguments of a previous run.

    Arguments
    ---------
    args: :class:`argparse.Namespace`
        The default arguments to overwrite.

    Returns
    -------
    args: :class:`argparse.Namespace`
        The updated arguments.
    """
    # Filename
    if filename is not None:
        json_filename = filename
    else:
        json_filename = os.path.join(args.outdir, FILE_ARGUMENTS)

    # Read and update arguments
    with open(json_filename, "r") as json_file:
        args.__dict__.update(json.load(json_file))

    # Logging checkpoint
    logging.info("Loaded arguments from {}".format(json_filename))
    logging.debug("Arguments list {}".format(args))
    return args


def load_features(path):
    """Read scattering coefficients and return design matrix."""
    # init
    x = list()
    t = list()

    # loop over available npz files
    for datafile in sorted(glob.glob(path)):
        data = np.load(datafile)
        features = [data[key] for key in data if "features" in key]

        # reshape and stack
        if features[0].shape[0]:
            features = [feat.reshape(feat.shape[0], -1) for feat in features]
            x.append(np.hstack(features))
            t.append(data["times"])

    return np.vstack(x), np.hstack(t)


def load_feature_file(path):
    """Read scattering coefficients and return design matrix."""
    data = np.load(path)
    features = [data[key] for key in data if "features" in key]
    if features[0].shape[0]:
        features = [feat.reshape(feat.shape[0], -1) for feat in features]
        x = np.hstack(features)
        t = data["times"]
    return x, t
