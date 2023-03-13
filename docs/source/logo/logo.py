"""Logo for scatseisnet.

This script generates a logo for scatseisnet. The logo is a scatter plot of a
wavelet. The wavelet is a Gaussian windowed sine wave. The scatter plot is
colored by time and the size of the scatter points is proportional to the
amplitude of the wavelet. The wavelet is squeezed in the x-direction to
simulate a seismic trace. 

The logo is saved as a PNG file and SVG file.

Author: Leonard Seydoux
Date: 2023-03-01
Copyright (C) 2023 Leonard Seydoux
"""

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

import scatseisnet as ssn


FILEPATH_SAVE_LOGO = "logo_scatseisnet"
TEXT = "scat seis net"
FONT = "Ubuntu Mono"
N_POINTS = 900
FREQUENCY = 1.7
WIDTH = 0.8
THICKNESS = 600
COLORBLEND = "#FFD43B", "#FFD43B", "0.2", "#4B8BBE", "#4B8BBE"


def main():

    # Create figure
    fig = plt.figure(figsize=(2, 2))

    # Create axes
    ax = fig.add_axes([0, 0, 1, 1])

    # Time vector
    time = 1.5 * np.linspace(-1, 1, N_POINTS)

    # Wavelet design
    wavelet = 0.8 * ssn.wavelet.complex_morlet(
        time, center=FREQUENCY, width=WIDTH
    )

    # Thickness and color
    thickness = THICKNESS * np.abs(wavelet)
    cmap = mcolors.LinearSegmentedColormap.from_list("", COLORBLEND, N=1000)

    # Plot
    ax.scatter(time, wavelet.imag, c=time, s=thickness, cmap=cmap, linewidths=0)

    # Manage axes limits and style
    ax.set_ylim(-1.5, 1.5)
    ax.set_axis_off()

    # Save figure
    save_kw = dict(bbox_inches="tight", pad_inches=0, transparent=True, dpi=300)
    fig.savefig(FILEPATH_SAVE_LOGO + "_notext.png", **save_kw)
    fig.savefig(FILEPATH_SAVE_LOGO + "_notext.svg", **save_kw)

    # Manage axes limits and style
    ax.set_ylim(-1.4, 1.2)

    # Text
    text_kwargs = dict(ha="center", va="top", size=25, name=FONT, weight="bold")
    ax.text(0, -1.1, TEXT, color="0.4", **text_kwargs)

    # Plot a colored dot for each space
    indices = [i for i, x in enumerate(TEXT) if x == " "]
    for i, index in enumerate(indices):
        dot = list(" ") * len(TEXT)
        dot[index] = "·"
        dot = "".join(dot)
        ax.text(0, -1.1, dot, color=cmap(i / 3 + 0.33), **text_kwargs)

    # Save figure
    save_kw = dict(bbox_inches="tight", pad_inches=0, transparent=True, dpi=300)
    fig.savefig(FILEPATH_SAVE_LOGO + ".png", **save_kw)
    fig.savefig(FILEPATH_SAVE_LOGO + ".svg", **save_kw)


if __name__ == "__main__":
    main()
