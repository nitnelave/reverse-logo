#! /usr/bin/env python

from collections import Counter

FORBIDDEN_NGRAMS = ['left', 'right', 'forward']

def scan_functions(l):
    functions = [('r', 'right 90', Counter()),
                 ('l', 'left 90', Counter()),
                 ('u', 'left 180', Counter())]
    for i in l:
        for st, ft, dic in functions:
            if i.startswith(ft):
                f = int(i[len(ft) + 9:])
                dic[f] += 1
                break
    s = ""
    for st, ft, dic in functions:
        for k, v in dic.items():
            if v > 3:
                s += "to {}{}\n{}\nforward {} end\n".format(st, k, ft, k)
    return (s, functions)

def get_functions(instr, functions):
    res = []
    for i in instr:
        added = False
        for st, ft, dic in functions:
            if i.startswith(ft):
                f = int(i[len(ft) + 9:])
                if dic[f] > 3:
                    res.append('{}{}'.format(st, f))
                    added = True
                    break
        if not added:
            res.append(i)
    return res

def get_ngrams(instr, n, ngrams):
    i = 0
    ngrams[n] = Counter()
    while i < len(instr) - n:
        l = ','.join(instr[i:i+n])
        c = 1
        for f in FORBIDDEN_NGRAMS:
            if f in l:
                c = 0
                break
        ngrams[n][l] += c
        i += 1
    decl = ''
    for l, k in ngrams[n].items():
        if k * (n - 1) > n + 1:
            decl += 'to {}\n{} end\n'.format(l.replace(',', ''), l.replace(',', '\n'))
    return (decl, ngrams)

def replace_ngrams(instr, n, ngrams):
    i = 0
    res = []
    while i < len(instr) - n:
        l = ','.join(instr[i:i+n])
        k = ngrams[n][l]
        if k*(n-1) > n+1:
            res.append(l.replace(',', ''))
            i += n
        else:
            res.append(instr[i])
            i += 1
    res.extend(instr[-n+1:])
    return res


