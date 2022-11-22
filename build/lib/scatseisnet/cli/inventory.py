# coding: utf-8
"""Command-line module for data inventory.

Author: Leonard Seydoux
Date: June, 2021
Email: leonard.seydoux@univ-grenoble-alpes.fr
"""

import click
import os

from .common import common_options

from ..inventory import inventorize
from .. import io


@click.command("inventory", short_help="Create dataset inventory.")
@common_options
@click.option(
    "--tags",
    type=str,
    default="*",
    show_default=True,
    help="Tags to search for in the datapath. Accepts wildcards.",
)
def inventory(
    tags=None,
    channels=None,
    savepath=None,
    datapath=None,
    filename_inventory=None,
    **kwargs,
):
    """Create an inventory of available data.

    The script generates an inventory of the data files from a parsable path.
    This inventory allows later to connect the calculated features and the
    input data quickly. In addition, this script enables selecting the input
    data based on different criteria, such as the sampling rate, duration,
    channel, or dates. 

    The parser determines two elements from the given parsable path: a "tag"
    identifier for each file and a "channel" variable. Note that these two
    variables can appear multiple times in the string. 

    Let us consider the example list of files below containing three days of
    data (tagged as 2014.14, 2014.15, and 2014.16) recorded with two channels
    (E and Z).

        /path/to/data/2010.014/HHE/2010.014.HHE.sac
        /path/to/data/2010.014/HHZ/2010.014.HHZ.sac
        /path/to/data/2010.015/HHE/2010.015.HHE.sac
        /path/to/data/2010.015/HHZ/2010.015.HHZ.sac
        /path/to/data/2010.016/HHE/2010.016.HHE.sac
        /path/to/data/2010.016/HHZ/2010.016.HHZ.sac

    The idea is to generate a list of file paths that can read all channels of
    the same date at once with the obspy's read routine with the following
    command: 

        scatseisnet inventory --datapath /path/to/data/{tag}/HH{channel}/{tag}.HH{channel} --channels Z E --tag * --filename_inventory inventory

    From this command, the parser will determine the following list of tags
    (that can be restricted to more specific regular expression with the --tag
    command-line argument) with corresponding paths and save them in the
    "inventory" file specified in the --file_inventory option.

        2014.014 /path/to/data/2010.014/HH[Z,E]/2010.014.HH[Z,E].sac
        2014.015 /path/to/data/2010.015/HH[Z,E]/2010.015.HH[Z,E].sac
        2014.016 /path/to/data/2010.015/HH[Z,E]/2010.016.HH[Z,E].sac

    Note that the notation "[Z,E]" enables obspy to read both channels Z and E
    in the same stream at once, given the path expansion capabilities of the
    obspy read routine (based on the glob Python library). 
    """
    # Resolve paths
    dirpath_inventory = os.path.join(savepath, "inventories")
    filepath_inventory = os.path.join(dirpath_inventory, filename_inventory)

    # Calculate inventory
    io.mkdir(dirpath_inventory)
    db = inventorize(datapath, channels, tags)

    # Save inventory
    db.to_pickle(filepath_inventory)
    io.stdout("Inventory complete saved at", filepath_inventory)

