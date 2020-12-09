#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 13:33:10 2020

@author: m4this
"""

import numpy as np
import matplotlib.pyplot as plt



def median(liste):
    return sorted(liste)[len(liste) // 2]


def quantile(liste, p = 0.5):
    return sorted(liste)[int(len(liste) * p)]

class Data(): 
    
    def __init__(self, file):
        self.file = file
        self.appreciations = ["Pas vu", "Nul", "Mauvais", "Moyen", "Assez bien", "Bien", "Excellent"]
        
        with open(file, "r") as f:
            
            self.choix = f.readline().strip('\n').split(',')[1:]
            lines = f.readlines()
            
            self.noms = []
            self.votes = []
            
            for line in lines:
                nom, *vote = line.split(',')
                self.noms.append(nom)
                self.votes.append([int(n) for n in vote])
        
    def __repr__(self):
        return f'Data({self.file}, {self.choix})'
    
    def jugement_majoritaire(self, compte_pas_vu = True, afficher = False, départage = 0.75):
        
        l = [[] for _ in self.choix]
        
        for vote in self.votes:
            for i, element in enumerate(vote):
                if compte_pas_vu or element != 1:
                    l[i].append(element)
        
        
        if afficher:
            start = 1 if compte_pas_vu else 2 
            fig, ax = self.graphe_majo(l, start)
            nb_votant = len(l[0])
            ax.vlines(nb_votant/2, -0.2, 9.2, color = "blue" )
            
            plt.show()
            
        medians = [median(liste) for liste in l]
        max_median = max(medians)
        n = medians.count(max_median)
        if n == 1:
            vainqueur = self.choix[ median.index(max_median) ]
            return vainqueur
        else:
            raise ValueError("Egalité")
        
    def graphe_majo(self, results, start):
        data = np.array(
            [[element.count(i) for i in range(start, len(self.appreciations) + 1)]
             for element in results])
        labels = self.choix
        category_names = self.appreciations[start - 1:]

    
        data_cum = data.cumsum(axis=1)
        category_colors = plt.get_cmap('RdYlGn')(
            np.linspace(0.15, 0.85, data.shape[1]))
    
        fig, ax = plt.subplots(figsize=(9.2, 5))
        ax.invert_yaxis()
        ax.xaxis.set_visible(False)
        ax.set_xlim(0, np.sum(data, axis=1).max())
    
        for i, (colname, color) in enumerate(zip(category_names, category_colors)):
            widths = data[:, i]
            starts = data_cum[:, i] - widths
            ax.barh(labels, widths, left=starts, height=0.5,
                    label=colname, color=color)
            
            
            
            # xcenters = starts + widths / 2
    
            # r, g, b, _ = color
            # text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
            # for y, (x, c) in enumerate(zip(xcenters, widths)):
            #     ax.text(x, y, str(int(c)), ha='center', va='center',
            #             color=text_color)
        
        ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
                  loc='lower left', fontsize='small')
    
        return fig, ax
    






if __name__ == '__main__':
    d = Data("vote film (majoritaire).csv")
    l1 = d.jugement_majoritaire(compte_pas_vu = True, afficher=True)
    # l2 = d.jugement_majoritaire(compte_pas_vu=True)
    
    # d.jugement_majoritaire(afficher=True)
    # plt.show()