#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 13:33:10 2020

@author: m4this
"""

import matplotlib.pyplot as plt



def median(liste):
    return sorted(liste)[len(liste) // 2]

class Data(): 
    
    def __init__(self, file):
        self.file = file
        self.appreciations = ["Pas vu", "Nul", "Mauvais", "Moyen", "Assez bien", "Bien", "Excellent"]
        
        with open(file, "r") as f:
            
            self.partis = f.readline().strip('\n').split(',')[1:]
            lines = f.readlines()
            
            self.noms = []
            self.votes = []
            
            for line in lines:
                nom, *vote = line.split(',')
                self.noms.append(nom)
                self.votes.append([int(n) for n in vote])
        
    def __repr__(self):
        return f'Data({self.file}, {self.partis})'
    
    def jugement_majoritaire(self, compte_pas_vu = True, afficher = False):
        l = [[] for _ in self.partis]
        
        for vote in self.votes:
            for i, element in enumerate(vote):
                if compte_pas_vu or element != 1:
                    l[i].append(element)
        
        
        # if afficher:
        #     plt.clf()
        #     color = [k * (16**6 - 1) / len(self.appreciations) for k in range()]
        
        return [median(liste) for liste in l]
        


if __name__ == '__main__':
    d = Data("vote film (majoritaire).csv")
    l1 = d.jugement_majoritaire(compte_pas_vu=False)
    l2 = d.jugement_majoritaire(compte_pas_vu=True)