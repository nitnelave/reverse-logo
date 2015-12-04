#! /usr/bin/env python

from tologo.functions import *
from tologo.repeat import *
from tologo.obfuscate import *
from fill.tools import pt_diff
import numpy as np
import math

def get_instructions(pts):
    instr = []
    angle = 0
    for i in range(len(pts) - 1):
        if pts[i+1] == pts[i]:
            continue
        dp = pt_diff(pts[i+1], pts[i])
        na = round(np.arctan2(dp[0], dp[1]) * 2 / math.pi) * 90
        da = na - angle
        if da > 180:
            da -= 360
        elif da <= -180:
            da += 360
        angle = na
        dist = abs(sum(dp))
        instr.append('{} {:.0f}\nforward {:.0f}'.format('left' if da > 0 else 'right', abs(da), dist))
    return instr

def get_compressed_instructions(pts, repeat_thr=6):
    instr = get_instructions(pts)
    decl, fun = scan_functions(instr)
    instr = get_functions(instr, fun)
    ngrams = {}
    for i in range(2, 6):
        d, ngrams = get_ngrams(instr, i, ngrams)
        while d != '':
            decl += d
            instr = replace_ngrams(instr, i, ngrams)
            d, ngrams = get_ngrams(instr, i, ngrams)
    s = '\n'.join(instr)
    instr = s.split('\n')
    for n in range(repeat_thr + 1, 0, -1):
        instr = get_repeat(instr, n)
    instr = get_repeat(instr, 1)
    s = '\n'.join(instr)
    s = s.replace('\n]', ' ]')
    text = 'right 90\n' + decl + s + '\n'
    text = obfuscate(decl, text)
    return (decl, text)
