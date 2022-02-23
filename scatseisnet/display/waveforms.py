# coding: utf-8
"""Display features.

Author: Leonard Seydoux
Date: June, 2021
Email: leonard.seydoux@univ-grenoble-alpes.fr
"""

import numpy as np
import obspy

from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from scipy.spatial.distance import euclidean

# from scipy.stats import median_abs_deviation as mad

from .. import inventory


plt.rcParams["figure.constrained_layout.use"] = True
COLORS = "#226fc7", "#22c78b", "#c75c22"


def match_tag(timestamp, times):
    try:
        return np.where((np.fix(timestamp) - times) == 0)[0][0]
    except:
        return np.argmin(np.abs(np.fix(timestamp) - times))


def show_waveforms(
    segment,
    file_features,
    file_prediction,
    file_inventory,
    file_figure,
    n_samples=None,
    reader=None,
    factor=0.8,
):

    # Features
    with np.load(file_features) as data:
        feature_times = data["times"]
        feature_values = data["features"]

    # Predictions
    with np.load(file_prediction) as data:
        predictions = data["predictions"]

    # Get start times of inventory
    database = inventory.read(file_inventory)
    # tags = list(database.keys())
    # inventory.read(file_inventory)
    # _, paths, starts, *_ = inventory.read(file_inventory)
    # starts = [mdates.datestr2num(t) for t in starts]
    # starts = get_all_subkeys(database, "date_start") #does not work
    starts = [database["starttime"]]
    starts = mdates.date2num(starts)
    # paths = get_all_subkeys(database, "path") #does not work
    paths = [database["path"]]
    # end = get_all_subkeys(database, "date_end")
    # zeros = get_all_subkeys(database, "n_zeros")
    # sampling_rate = get_all_subkeys(database, "sampling_rate")
    # npts = get_all_subkeys(database, "n_pts")
    # start = mdates.date2num(start)
    # end = mdates.date2num(end)

    # Calculate centroids
    classes = np.unique(predictions)

    for cluster in classes:

        # Extract clusters
        within_cluster = predictions == cluster
        cluster_samples = feature_values[within_cluster]
        cluster_times = feature_times[within_cluster]

        # Centroid
        centroid = np.mean(cluster_samples, axis=0)
        distances = list()
        for sample in cluster_samples:
            distances.append(euclidean(sample, centroid))
        distances = np.array(distances)

        # Extract best waveforms timestamps
        distances_argsort = np.argsort(distances)
        sorted_times = cluster_times[distances_argsort][:n_samples]
        # sorted_times = cluster_times[:n_samples]

        # Create figure
        fig, axes = plt.subplots(
            nrows=1,
            ncols=2,
            figsize=(6, 6),
            sharey=True,
            gridspec_kw={"width_ratios": (2, 1)},
        )

        y_ticklabels = list()
        for event_id, timestamp in enumerate(sorted_times):

            # Match time
            print(timestamp)
            tag_id = match_tag(timestamp, starts)
            start = obspy.UTCDateTime(mdates.num2date(timestamp))
            end = obspy.UTCDateTime(
                mdates.num2date(timestamp + segment / 3600 / 24)
            )
            # stream = reader(paths[tag_id], trim=(start, end)) #ERROR trim option not accepted
            stream = reader(paths[tag_id])
            n_channels = len(stream)
            if n_channels == 0:
                continue

            y_ticklabels.append(
                mdates.num2date(timestamp).strftime("%y/%m/%d %H:%M:%S")
            )

            # Show
            plot_style = dict()
            # components_max = np.mean([mad(trace.data) for trace in stream])
            components_max = np.max([np.max(trace.data) for trace in stream])
            for trace_id, trace in enumerate(stream):

                # Extract data
                trace_times = trace.times()
                trace_data = trace.data
                # trace_data = trace_data / components_max / 20
                trace_data = trace_data / components_max
                trace_data += factor * trace_id + n_channels * event_id

                # Assign channel color and label
                plot_style["color"] = COLORS[trace_id]
                if event_id == 0:
                    plot_style["label"] = trace.stats.channel

                # Plot
                axes[0].plot(trace_times, trace_data, **plot_style)

            axes[0].plot(
                [0, 0],
                [
                    event_id * n_channels,
                    event_id * n_channels + factor * (n_channels - 1),
                ],
                "0.3",
                clip_on=False,
            )

            axes[0].plot(
                2 * [trace_times.max()],
                [
                    event_id * n_channels,
                    event_id * n_channels + factor * (n_channels - 1),
                ],
                "0.3",
                clip_on=False,
            )

        # Skip if no waveforms detected
        if not y_ticklabels:
            continue

        # Yticks
        y_ticks = np.arange(0, n_channels * len(y_ticklabels), n_channels)
        y_ticks = y_ticks + factor

        # Distances
        axes[1].barh(
            y_ticks,
            distances[distances_argsort][:n_samples],
            height=1.5,
            color="0.8",
        )
        axes[1].axvline(np.mean(distances))
        # axes[1].plot(distances[distances_argsort][:n_samples], y_ticks, "o")
        axes[1].set_xlabel("Euclidean distance (latent space)")
        axes[1].spines["top"].set_visible(False)
        axes[1].spines["right"].set_visible(False)

        # Labels
        axes[0].legend(loc="upper center", ncol=3)
        axes[0].set_xlim(0, trace_times.max())
        axes[0].set_xlabel("Time (seconds)")
        axes[0].set_yticks(y_ticks)
        axes[0].set_ylim(-1, n_channels * n_samples + 1)
        axes[0].set_yticklabels(y_ticklabels, size="small")
        axes[0].grid(clip_on=False)
        axes[0].set_title(f"Cluster {cluster}", loc="left")
        axes[0].spines["top"].set_visible(False)
        axes[0].spines["right"].set_visible(False)
        axes[0].spines["left"].set_visible(False)
        axes[0].tick_params(axis="y", length=0, which="both")

        # # Latent inset
        # inset = fig.add_axes([0.8, 0.8, 0.2, 0.2])
        # inset.plot(feature_values[:, 0], feature_values[:, 1], ".", c="0.6")
        # inset.plot(
        #     cluster_samples[:, 0], cluster_samples[:, 1], ".", c="k",
        # )
        # inset.plot(
        #     cluster_samples[distances_argsort, 0][:n_samples],
        #     cluster_samples[distances_argsort, 1][:n_samples],
        #     ".",
        #     c="C1",
        # )

        fig.savefig(file_figure.replace("*", f"{cluster:02d}"))
        plt.close()


def get_all_subkeys(dictionnary, subkey):
    """Get all sub entries of a dictionnary with given subkey."""
    subvalues = [dictionnary[key][subkey] for key in dictionnary.keys()]
    return subvalues
