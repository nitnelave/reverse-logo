
# coding: utf-8

from PIL import Image
import numpy as np

from fill import fill
from tologo import instructions


def get_binary_image(f, thresh=None, invert=False):
    im = Image.open(f)
    bin_im = im.convert('L')
    px = bin_im.load()
    black = 255 if invert else 0
    white = 255 - black
    if not invert:
        thresh = 185 if invert else 70

    for p in np.ndindex(bin_im.size):
        bin_im.putpixel(p, black if px[p] <= thresh else white)

    return bin_im

def image_to_logo(imgfile, outputfile=None, invert=False, verbose=2):
    im = get_binary_image(imgfile, invert)
    points = fill.fill(im)
    if verbose >= 2:
        print(len(points), "points to cover")
    _, program = instructions.get_compressed_instructions(points)
    if verbose >= 2:
        print("Completed in", program.count('\n'), "lines")
    if outputfile:
        with open(outputfile, 'w') as f:
            f.write(program)
    return program

