#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 14:12:48 2020

@author: m4this
"""

class Individu():
    
    def __init__(self, a, b, epsilon = 10 ** -9):
        self.a = a
        self.b = b
        self.epsilon = epsilon
       
    def __repr__(self):
        return f'Individu({self.a}, {self.b})'
    
    def __le__(self, other):
        # <=
        return self.distance_carre() < other.distance_carre() or self.__eq__(other)
    
    def __lt__(self,other):
        # <
        return self.distance_carre() < other.distance_carre()
    
    def __eq__(self, other):
        # ==
        return abs(self.distance_carre() - other.distance_carre()) <= self.epsilon
    
    def distance_carre(self):
        return self.a ** 2 + self.b ** 2
    
def mini(ind, liste):
    
    m = liste[0]
    l_mini = []
    
    for element in liste:
        if element < m:
            l_mini = []
            m = element
        elif element == m:
            l_mini.append(element)
    
    return l_mini
