# coding: utf-8
"""Command-line interface module.

The subcommands are defined in dedicated modules. Note that all subcommands
share a subset of options defined in the "common.py" module. The "main"
function defined here is a group for attaching all the subcommands, and it
establishes the program's entry point.

Author: Leonard Seydoux Date: June, 2021 Email:
leonard.seydoux@univ-grenoble-alpes.fr
"""

import click

from .inventory import inventory
from .linkage import linkage
from .features import features
from .transform import transform
from .waveforms import waveforms


@click.group()
def main():
    """Deep scattering transform on segmented time series.

    This program contains a series of command-line tools for clustering
    continuous time series with a deep scattering network. The following
    sub-commands must be run in a specific order from the continuous data to
    the cluster results.

    1. The inventorize command lists and selects the data based on usual meta
    parameters (sampling rate, duration, channels) and stores the relevant
    datapaths into an inventory file. This first command helps explore the data
    coverage in time, selecting appropriate time segments, and running the
    remaining steps on the actual data.

    2. The transform command runs the deep scattering transform on the
    segmented time series and stores the scattering coefficients for later
    feature extraction. 

    3. With the features command, the large-dimensional scattering coefficients
    are reduced to a low-dimensional space which dimensions are considered
    features here. These features are used in the clustering step next.

    4. The command calculates the linkage matrix that helps cluster the data
    based on some criteria of similarity (a metric and a method). Once this
    matrix is calculated, the clusters are extracted for further analyses.

    Created in May, 2021 by Leonard Seydoux
    (leonard.seydoux@univ-grenoble-alpes.fr) and Randall Balestriero.

    """
    pass


# Add subcommands
main.add_command(inventory)
main.add_command(transform)
main.add_command(features)
main.add_command(linkage)
main.add_command(waveforms)
