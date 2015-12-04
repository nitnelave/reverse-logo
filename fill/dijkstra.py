#! /usr/bin/env python

from fill.tools import add_dir, dirs, PriorityQueue
import numpy as np

def dijkstra(start, is_allowed, seen, dimensions):
    dist = dimensions[0] * dimensions[1] * np.ones((dimensions[0], dimensions[1]), dtype=float)
    dist[start] = 0
    dseen = np.zeros((dimensions[0], dimensions[1]), dtype=bool)
    heap = PriorityQueue()
    heap.update(start, 0)
    while heap:
        _, p = heap.pop()
        for d in dirs:
            dis = dist[p]
            newp = add_dir(p, d, dimensions)
            npts = []
            k = 0
            while newp and not dseen[newp] and is_allowed(newp):
                k += 1
                npts.append((newp, dis + 0.001 * k))
                newp = add_dir(newp, d, dimensions)
            for (p_, d_) in npts:
                dist[p_] = min(dist[p_], d_)
                heap.update(p_, dist[p_])
        dseen[p] = True
        if not seen[p]:
            res = [p]
            c = 0
            while p != start:
                c += 1
                x, ps = min([(dist[_p], _p) for _p in [add_dir(p, d, dimensions) for d in dirs]], key=lambda x: x[0])
                p = ps
                res.append(ps)
                seen[p] = True
            res.reverse()
            return res
    return None

