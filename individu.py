#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 14:12:48 2020

@author: m4this
"""
from random import choice

class Individu():
    """
    a, b : position de l'individu sur l'échéquier politique
    p : distance à laquelle un parti doit être pour que l'individu l'approuve
    """
    def __init__(self, a, b, p,  epsilon = 10 ** -9):
        self.a = a
        self.b = b
        self.p = p
        self.epsilon = epsilon
       
    def __repr__(self):
        return f'Individu({self.a}, {self.b}, {self.p})'
    
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



def minis(ind, liste):
    
    m = liste[0]
    l_mini = []
    
    for element in liste:
        if element < m:
            l_mini = []
            m = element
        elif element == m:
            l_mini.append(element)
    
    return l_mini

def mini(ind, liste):
    l = minis(ind, liste)
    return choice(l)
    

def disque(ind, liste):
    p_c = ind.p ** 2
    return [element for element in liste if element.distance_carre() <= p_c]
