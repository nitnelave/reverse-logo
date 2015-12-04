#! /usr/bin/env python

import re
import itertools

def gen_fun_name():
    #name_list = [chr(i) for i in itertools.chain(range(97, 123),range(65, 91))]
    name_list = [chr(i) for i in range(97, 123)]
    for i in itertools.count(): #Infinite loop
        for l in itertools.product(name_list, repeat=(i+1)):
            s = ''.join(l)
            yield 'z' + s


def obfuscate(decl, text):
    i = 0
    g = gen_fun_name()
    for d in decl.split('\n'):
        if not d.startswith("to "):
            continue
        dname = d[3:]
        ob_name = next(g)
        text = re.sub('^' + dname + '( |\n)', ob_name + '\\1', text, flags=re.MULTILINE)
        text = re.sub('^to ' + dname + '\n', 'to ' + ob_name + '\n', text, flags=re.MULTILINE)
    return text
