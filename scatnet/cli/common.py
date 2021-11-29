# coding: utf-8
"""Common subcomands options for command-line interface.

Authors: Leonard Seydoux and Randall Balestriero
Email: leonard.seydoux@univ-grenoble-alpes.fr
Date: May, 2021
"""


import click
import os
import functools

COMMON_OPTIONS = [
    click.option(
        "--savepath",
        default=os.environ.get("SAVEPATH", "."),
        show_default=".",
        help="output directory",
        type=click.Path(resolve_path=True, writable=True),
    ),
    click.option(
        "--datapath",
        default=os.environ.get("DATAPATH", "."),
        show_default=".",
        help="input data path to scan",
    ),
    click.option(
        "--figpath",
        default=os.environ.get("FIGPATH", "."),
        show_default=".",
        help="path to save figures",
        type=click.Path(resolve_path=True, writable=True),
    ),
    click.option(
        "--start",
        type=click.DateTime(),
        default="0001-01-01 00:00:00",
        help="Select data after start time.",
    ),
    click.option(
        "--end",
        type=click.DateTime(),
        default="9999-01-01 00:00:00",
        help="Select data after start time.",
    ),
    click.option(
        "--channels",
        type=str,
        default="*",
        show_default=True,
        help="Channels to search for.",
    ),
    click.option(
        "--filename_inventory",
        type=str,
        default="inventory",
        show_default=True,
        help="Basename for inventory file.",
    ),
    click.option(
        "--filename_network",
        type=str,
        default="network",
        show_default=True,
        help="Basename for network file.",
    ),
    click.option(
        "--filename_reduction",
        type=str,
        default="reduction_{}",
        show_default=True,
        help="Basename for network file.",
    ),
    click.option(
        "--path_scatterings",
        type=str,
        default="scatterings",
        show_default=True,
        help="Name of scattering files directory.",
    ),
    click.option(
        "--path_features",
        type=str,
        default="features",
        show_default=True,
        help="Name of feature files directory.",
    ),
    click.option(
        "--path_clusters",
        type=str,
        default="clusters",
        show_default=True,
        help="Name of cluster files directory.",
    ),
    click.option(
        "--show",
        is_flag=True,
        default=False,
        show_default=True,
        help="Excluding flag to show or calculate.",
    ),
]


def common_options(f):
    return functools.reduce(lambda x, opt: opt(x), COMMON_OPTIONS, f)

