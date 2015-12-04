#! /usr/bin/env python

dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def pt_diff(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])

def add_dir(p, d, dim):
    if isinstance(d, int):
        d = dirs[d % 4]
    p_ = (p[0] + d[0], p[1] + d[1])
    if p_[0] < 0 or p_[0] >= dim[0] or p_[1] < 0 or p_[1] >= dim[1]:
        return None
    return p_

class PriorityQueue:

    def __init__(self):
        self.heap = []
        self.map = {}

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.update_map(i)
        self.update_map(j)

    def __bool__(self):
        return len(self.heap) != 0

    def update_map(self, i):
        self.map[self.heap[i][1]] = i

    def pop(self):
        res = self.heap[0]
        del self.map[res[1]]
        if len(self.heap) == 1:
            self.heap = []
            self.map = {}
            return res
        self.heap = [self.heap[-1]] + self.heap[1:-1]
        self.update_map(0)
        ind = 0
        while 2 * ind + 1 < len(self.heap):
            if (len(self.heap) > 2 * ind + 2
                and self.heap[2 * ind + 2][0] < self.heap[ind][0]
                and self.heap[2 * ind + 2][0] < self.heap[2 * ind + 1][0]):
                nind = 2 * ind + 2
            elif self.heap[2 * ind + 1][0] < self.heap[ind][0]:
                nind = 2 * ind + 1
            else:
                break
            self.swap(ind, nind)
            ind = nind
        return res


    def update(self, key, value):
        if key not in self.map:
            self.heap.append((value, key))
            self.map[key] = len(self.heap) - 1
        ind = self.map[key]
        self.heap[ind] = (value, key)
        while ind:
            nind = (ind - 1) // 2
            if self.heap[nind][0] > self.heap[ind][0]:
                self.swap(ind, nind)
                ind = nind
            else:
                break
