# coding: utf-8
"""Routines for inventorizing data.

Author: Leonard Seydoux
Date: June, 2021
Email: leonard.seydoux@univ-grenoble-alpes.fr
"""

import obspy
import pandas as pd

from glob import glob
from parse import parse
from tqdm import tqdm

from .io import stdout


def inventorize(parsable_path, channel_pattern, tag_pattern):
    """Glob files with expansion on tag and channel, and get headers.
    
    Arguments
    ---------
    parsable_path: str
        The path to data with a tag and a channel string variables.
    channel_pattern: str
        Pattern to expand for channels.
    tag_pattern: str
        Pattern to expand for tag.
    
    Returns
    -------
    db: pandas.DataFrame
        The extracted availability and metadata.
    """
    # File pattern creation
    pattern = dict(tag=tag_pattern, channel=channel_pattern)
    filepath_pattern = parsable_path.format(**pattern)
    stdout("Data files pattern {}", filepath_pattern)

    # File pattern glob
    filepaths_matching = sorted(glob(filepath_pattern))
    if len(filepaths_matching) > 0:
        stdout("Found {} matching files", len(filepaths_matching))
    else:
        print("No files matching pattern; exiting.")
        exit()

    # Build up inventory
    header = obspy.read(filepaths_matching[0], headonly=True)[0].stats
    db_entrynames = [item for item in header]
    db = pd.DataFrame(columns=db_entrynames)

    # Extract headers from every files
    index = 0
    for filepath in tqdm(filepaths_matching, desc="Making inventory"):

        # Fix Windows filepath (temporary solution)
        if  "\\" in filepath:
            filepath=filepath.replace("\\", "/")

        # Read headers
        stream = obspy.read(filepath, headonly=True)
        parsed = parse(parsable_path, filepath)
        # print(parsable_path)
        # print(filepath)

        # Extract stats from every traces
        for trace in stream:
            for entry in db_entrynames:
                db.loc[index, entry] = trace.stats[entry]
            db.loc[index, "tag"] = parsed["tag"]
            db.loc[index, "path"] = filepath
            index += 1

    return db


def read(filename_inventory):
    """Read inventory pickle file.
    
    Arguments
    ---------
    filename: str
        The filename of the inventory.

    Returns
    -------
    pandas.DataFrame
        The tags and corresponding metadata to read.
    """
    # Read pickle file
    db = pd.read_pickle(filename_inventory)

    # Drop columns
    db = db.drop(db._format.unique()[0].lower(), axis=1)
    db = db.drop("_format", axis=1)

    # Convert to pandas timestamps
    db.starttime = pd.to_datetime([t.datetime for t in db.starttime])
    db.endtime = pd.to_datetime([t.datetime for t in db.endtime])

    # Infer types
    db = db.infer_objects()

    # Duration
    db["duration"] = db.endtime - db.starttime
    db["duration_hours"] = db.duration.dt.total_seconds() / 3600

    return db
