# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 17:20:56 2022

@author: lenovo
"""
def get_kernel(a):
    return {0:[[1/a**2 for k in range(a)] for k in range(a)],

1:[[0, 0, 0],
 [0, 1, 0],
 [0, 0, 0]],

2:[[0, 1, 0],
 [1, -4, 1],
 [0, 1, 0]],

3:[[0, -1, 0],
 [-1, 5, -1],
 [0, -1, 0]],

4:[[-2*a, -1*a, 0],
 [-1*a, 1, 1*a],
 [0, 1*a, 2*a]]}


