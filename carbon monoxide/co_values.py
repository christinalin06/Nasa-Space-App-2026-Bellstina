import sys
import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.spatial import cKDtree

CO_colorbar = "CO_colowebar_plain.png"


def load_colorbar(co_colorbar=CO_colorbar):
    """Find gradient in colorbar PNG and return its color (left (low CO) to right (High CO))"""
    rgb = np.array(Image.open(co_colorbar).convert("RGB")).astype(int)

    # identify colorbar in image
    not_white = (rgb != 255).any(axis=2)

    rows, cols = np.where(not_white)
    top, bottom = rows.min(), rows.max()
    left, right = cols.min(), cols.max()

    # account for white tick marks in colorbar
    pixels_per_row = not_white[top : bottom + 1].sum(axis=1)
    full_width = pixels_per_row.max()
