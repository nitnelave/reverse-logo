#! /usr/bin/env python

def get_repeat(instr, n):
    res = []
    end = len(instr) - n
    i = 0
    while i < end - 1:
        j = i
        while j < end - 1:
            j += n
            good = True
            for k in range(n):
                if instr[j + k] != instr[i + k]:
                    good = False
                    break
            if not good:
                break
        l = (j - i) // n
        if l == 1 or (l == 2 and n == 1):
            res.append(instr[i])
        else:
            res.append('repeat {} [\n{}\n]'.format(l, '\n'.join(instr[i:i + n])))
            i = j - 1
        i += 1
    res.extend(instr[i:])
    return res
