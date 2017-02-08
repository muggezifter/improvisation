#! /usr/bin/env python

ar = [1,2,3]

def makefun(y):
    return lambda x: x+y

print(map(makefun(20),ar))