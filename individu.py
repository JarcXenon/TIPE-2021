#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 14:12:48 2020

@author: m4this
"""
from random import choice

class Individu():
    """
    Objet désignant un individu ou un parti
    """

    def __init__(self, a, b, p = 0, nom = '', epsilon = 10 ** -9):
        """
        

        Parameters
        ----------
        a : float
            abscisse de l'individu/parti sur l'échéquier politique.
        b : float
            ordonnée de l'individu/parti sur l'échéquier politique.
        p : float, optional
            distance à laquelle un parti doit être pour que l'individu l'approuve. Vaut par défaut 0
        nom : string, optional
            nom du parti ou du groupe. Vaut par défaut ''
        epsilon : float, optional
            écart pour les comparaison. Vaut par défaut 10 ** -9.

        Returns
        -------
        None.

        """
        self.a = a
        self.b = b
        self.p = p
        self.epsilon = epsilon
        self.nom = nom
       
    def __repr__(self):
        return f'Individu({self.a}, {self.b}, {self.p}, {self.nom})'
    
    def __le__(self, other):
        # <=
        return self.distance_carre() < other.distance_carre() or self.__eq__(other)
    
    def __lt__(self,other):
        # <
        return self.distance_carre() < other.distance_carre()
    
    def __eq__(self, other):
        # ==
        return self.distance_caree(other) <= self.epsilon
    
    def distance_caree(self, other = None):
        return self.a ** 2 + self.b ** 2 if not other else (self.a - other.a)**2 + (self.b - other.b)**2 


def minis(ind, liste_partis):
    """
    

    Parameters
    ----------
    ind : Individu
        désigne un individu
    liste_partis : Individu list
        tableau des partis.

    Returns
    -------
    l_mini : Invidu list
        tableau des partis les plus proches de l'individu ind

    """
    
    plus_proche_parti = liste_partis[0]
    l_mini = [plus_proche_parti]
    
    for element in liste_partis:
        if ind.distance_caree(element) < ind.distance_caree(plus_proche_parti):
            plus_proche_parti = element
            l_mini = [plus_proche_parti]
        elif element == plus_proche_parti:
            l_mini.append(element)
    return l_mini

def mini(ind, liste_partis):
    """
    

    Parameters
    ----------
    ind : Individu
        désigne un individu
    liste_partis : Individu list
        tableau des partis.

    Returns
    -------
    Individu
        Un des partis les plus proches de l'individu ind.

    """
    l = minis(ind, liste_partis)
    return choice(l)

def disque(ind, liste_partis):
    """
    

    Parameters
    ----------
    ind : Individu
        désigne un individu
    liste_partis : Individu list
        tableau des partis.

    Returns
    -------
    tableau de tous les partis que l'individu approuve

    """
    p_c = ind.p ** 2
    return [parti for parti in liste_partis if ind.distance_caree(parti) <= p_c]
