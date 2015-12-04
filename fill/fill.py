#! /usr/bin/env python

from fill.tools import add_dir, pt_diff
import numpy as np
from fill.dijkstra import dijkstra
from fill.discover import discover
import functools


def find_center(bin_im):
    px = bin_im.load()
    width, height = bin_im.size
    center = (width /2, height /2 + 9)
    c = center
    try:
        while px[c] != 255:
            c = add_dir(c, (0, 1), bin_im.size)
    except:
        c = center
        while px[c] != 255:
            c = add_dir(c, (0, -1), bin_im.size)
    return c

def log(*args, level=0):
    if level >= 0:
        print(*args)

def no_consecutive(pts):
    res = [pts[0]]
    for i in range(len(pts) - 1):
        if pts[i+1][0] != pts[i][0] or pts[i+1][1] != pts[i][1]:
            res.append(pts[i+1])
    return res

def simplify(pts):
    res = [pts[0]]
    for i in range(len(pts) - 2):
        if pt_diff(pts[i+1], pts[i]) != pt_diff(pts[i+2], pts[i+1]):
            res.append(pts[i + 1])
    return res

def fill(bin_im, verbose=2):
    points = [find_center(bin_im)]
    seen = np.zeros(bin_im.size, dtype=bool)
    px = bin_im.load()
    for p_ in np.ndindex(bin_im.size):
        seen[p_] = not px[p_]

    maxpx = len(seen) * len(seen[0])
    totalPix = maxpx - seen.sum()
    c = 0
    while True:
        c += 1
        if not c % 100:
            s = 100 * (1 - (maxpx - seen.sum()) / totalPix)
            log("{:.0f}%".format(s), level=verbose - 2)
        pts = discover(points[-1], seen, bin_im.size)
        points.extend(pts)
        p = points[-1]
        def is_allowed(p):
            return px[p]
        pts = dijkstra(p, is_allowed, seen, bin_im.size)
        if pts is None:
            break
        else:
            points.extend(pts)

    if seen.sum() != maxpx:
        log("More than one SCC, could not reach everything. Pixels left:", maxpx - seen.sum(), level=verbose - 1)
    return simplify(no_consecutive(points))
