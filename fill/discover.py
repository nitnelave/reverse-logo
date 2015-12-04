#! /usr/bin/env python

from fill.tools import add_dir

def discover(p, seen, dim):
    res = []
    seen[p] = True
    dir = 0
    last_dir = 3
    while dir != last_dir:
        p_p = add_dir(p, dir, dim)
        p_s = add_dir(p, (dir + 1), dim)
        while (p_p and not seen[p_p]) or (p_s and not seen[p_s]):
            last_dir = dir
            p = p_p if (p_p and not seen[p_p]) else p_s
            res.append(p)
            seen[p] = True
            p_p = add_dir(p, dir, dim)
            p_s = add_dir(p, (dir + 1), dim)
        dir = (dir + 1) % 4
    return res
