# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 15:29:33 2022

@author: Michael
"""

class recur:
    def __init__(self):
        self.n = None
    
    def add(self,n):
        if n <= 0:
            return 0
        else: 
            return n + self.add(n-1)
        
    def prod(self,n):
        if n <= 0:
            return 1
        else: 
            return n*self.prod(n-1)
    
    
test = recur()
test.add(5)
test.prod(5)


def add_recur(n):
    if n<= 0:
        return 0
    else:
        return n + add_recur(n-1)

add_recur(5)

def add_iter(n):
    tmp = 0
    for i in range(0,n):
        tmp+=i
    return(tmp)

add_iter(5)
    