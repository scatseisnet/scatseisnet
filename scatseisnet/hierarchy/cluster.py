#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Clustering.

author:
    Leonard Seydoux and Randall Balestriero
"""

import numpy as np

from fastcluster import linkage_vector
from scipy.cluster import hierarchy


def get_leaves(d, ax):
    """Get dendrogram list of leaves coordinates and colors.

    Arguments
    ---------
    d: dict
        Output of the scipy.hierarchy.dendrogram function.

    Returns
    -------
    coords, colors: array-like
        The x coordinates and color of each leave.
    """
    coords = list()
    for icoord, dcoord in zip(d["icoord"], d["dcoord"]):
        if dcoord[0] == 0:
            coords.append(icoord[0])

        if dcoord[-1] == 0:
            coords.append(icoord[-1])

    isort = np.argsort(coords)
    coords = np.array(coords)[isort]

    # Cardinality
    card = list()
    for y in ax.get_yticklabels():
        y = y.get_text()
        card.append(int(y[1:-1]) if "(" in y else 1)
    card = np.array(card)
    return coords, card


def linkage(x, distance="ward"):
    """Calculate linkage matrix on reduced matrix.

    The reduction is performed with independant component analysis.

    Arguments
    ---------
    x: np.ndarray
        Design matrix.

    Keyword arguments
    -----------------
    reduction: int
        The number of dimensions to consider for the linkage calculation.

    distance: str
        The metric to use for calculating the linkage matrix.

    Returns
    -------
    link:
        Linkage matrix.
    """
    # linkage
    link = linkage_vector(x, distance)
    print("Linkage calculated")
    return link


def fcluster(link, threshold):
    """Cluster data based on linkage matrix and threshold.

    Arguments
    ---------
    linkage:
        The linkage matrix

    threshold:
        The threshold to cluster the data with from a distance argument.

    Returns
    -------
    clusters: np.ndarray
        The per-sample cluster attribution.
    """
    return hierarchy.fcluster(link, t=threshold, criterion="distance")
