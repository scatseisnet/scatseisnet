"""Animated logo for scatseisnet.

This script generates an animated logo for scatseisnet. The logo is a scatter
plot of a wavelet. The wavelet is a Gaussian windowed sine wave with animated
phase. The scatter plot is colored by time and the size of the scatter points is
proportional to the amplitude of the wavelet. The wavelet is squeezed in the
x-direction to simulate a seismic trace.

The animated logo is saved as a GIF file.

Author: Leonard Seydoux Date: 2023-03-01 Copyright (C) 2023 Leonard Seydoux
"""

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io

import scatseisnet as ssn


FILEPATH_SAVE_LOGO = "logo_scatseisnet_anim.gif"
TEXT = "scat seis net"
FONT = "Ubuntu Mono"
N_POINTS = 2000
FREQUENCY = 1.7
WIDTH = 0.8
THICKNESS = 600
COLORBLEND = "#FFD43B", "#FFD43B", "0.2", "#4B8BBE", "#4B8BBE"
N_FRAMES = 240  # Number of frames in the animation
FPS = 30  # Frames per second


def create_frame(phase):
    """Create a single frame with the given phase."""

    # Always start with a fresh figure and axes
    plt.close("all")  # Close all previous figures to free memory
    fig = plt.figure(figsize=(2, 1.8), facecolor="none")
    ax = fig.add_axes([0, 0, 1, 1], facecolor="none")  # type: ignore

    # Time vector
    time = 1.5 * np.linspace(-1, 1, N_POINTS)

    # Wavelet design with animated phase inside the oscillatory term
    wavelet = (
        0.8
        * np.exp(1j * (2 * np.pi * FREQUENCY * time + phase))
        * ssn.wavelet.gaussian_window(time, WIDTH)
    )

    # Thickness and color
    thickness = THICKNESS * np.abs(wavelet)
    # Interpolate custom colors for a smooth gradient
    cmap = mcolors.LinearSegmentedColormap.from_list("custom", COLORBLEND)

    # Normalize time for smooth color mapping
    time_norm = (time - time.min()) / (time.max() - time.min())
    ax.scatter(
        time, wavelet.imag, c=time_norm, s=thickness, cmap=cmap, linewidths=0
    )

    # Manage axes limits and style
    ax.set_xlim(time.min() * 1.1, time.max() * 1.1)
    ax.set_ylim(-1.2, 1.2)
    ax.set_axis_off()

    # Convert figure to image
    buf = io.BytesIO()
    fig.savefig(
        buf,
        format="png",
        bbox_inches="tight",
        pad_inches=0,
        transparent=True,
        dpi=300,
    )
    buf.seek(0)
    frame_img = Image.open(buf).convert("RGBA")
    blank_img = Image.new("RGBA", frame_img.size, (255, 255, 255, 0))
    blank_img.paste(frame_img, (0, 0), frame_img)

    # Clean up
    buf.close()
    plt.close(fig)

    return blank_img


def main():
    """Generate animated logo."""

    print(f"Generating {N_FRAMES} frames...")

    # Generate frames with phases from 0 to 2*pi
    phases = np.linspace(0, 2 * np.pi, N_FRAMES, endpoint=False)
    frames = []

    for i, phase in enumerate(phases):
        print(f"Frame {i+1}/{N_FRAMES} (phase={phase:.2f})", end="\r")
        frame = create_frame(phase)
        frames.append(frame)

    frames[0].save(
        "logo_scatseisnet_anim.png",
        save_all=True,
        append_images=frames[1:],
        duration=2000 / FPS,
        loop=0,
        format="PNG",
    )


if __name__ == "__main__":
    main()
