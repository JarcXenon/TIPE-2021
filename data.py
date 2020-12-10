#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 13:33:10 2020

@author: m4this
"""

import numpy as np
import matplotlib.pyplot as plt

default_appreciations = ["Pas vu", "Nul", "Mauvais", "Moyen", "Assez bien", "Bien", "Excellent"]


class Data(): 
    
    def __init__(self, file,
                 appreciations = default_appreciations):
        """
        

        Parameters
        ----------
        file : string
            nom du fichier dans lequel se trouve les données à récupérer
        appreciations : string list
            tableau des appréciations possibles
        
        

        Returns
        -------
        None.

        """
        self.file = file
        self.appreciations = appreciations
        
        with open(file, "r") as f:
            
            self.choix = f.readline().strip('\n').split(',')[1:] #Tableau des choix possibles
            lines = f.readlines()
            
            self.noms = [] #Tableau des noms des participants
            self.votes = [] #Tableau des tableaux représentant les votes de chaque personne
            
            for line in lines:
                nom, *vote = line.split(',')
                self.noms.append(nom)
                self.votes.append([int(n) for n in vote])
        
    def __repr__(self):
        return f'Data({self.file}, {self.choix})'
    
    def jugement_majoritaire(self, 
                             compte_pas_vu = True, 
                             afficher = False, 
                             taux_de_départage = 0.75):
        """
        

        Parameters
        ----------
        compte_pas_vu : bool, optional
            indique si les votes indiquant la non connaissance d'un choix est comptée. 
            Vaut par défaut True.
        afficher : bool, optional
            si vrai, affiche le graphe du vote au jugement majoritaire. 
            Vaut par défaut False.
        taux_de_départage : float, optional
            Valeur entre 0 et 1 indique le taux pour départager les choix en cas d'égalité. 
            Vaut par défaut 0.75.

        Returns
        -------
        vainqueur : string 
            choix vainqueur par jugement majoritaire.
            

        """
        liste_des_votes = [[] for _ in self.choix]
        
        for vote in self.votes:
            for i, element in enumerate(vote):
                if compte_pas_vu or element != 1:
                    liste_des_votes[i].append(element)
        
        
            
        medians = [quantile(liste, p = 0.5) for liste in liste_des_votes]
        max_median = max(medians)
        n = medians.count(max_median)
        if n == 1:
            vainqueur = self.choix[medians.index(max_median)]
            besoin_départage = False
        else:
            pas = - 0.01 if taux_de_départage > 0.5 else 0.01
            besoin_départage = True
            
            while n != 1:
                quantiles = [quantile(liste, p = taux_de_départage) for liste in liste_des_votes]
                max_quantile = max(quantiles)
                n = quantiles.count(max_quantile)
                taux_de_départage += pas
            
            vainqueur = self.choix[quantiles.index(max_quantile)]
            
            


        if afficher:
            start = 1 if compte_pas_vu else 2 
            fig, ax = self.graphe_majo(liste_des_votes, start)
            nb_votant = len(liste_des_votes[0])
            ax.vlines(nb_votant/2, -0.2, 9.2, color = "blue" )
            if besoin_départage:
                ax.vlines(nb_votant * taux_de_départage, -0.2, 9.2, color = "purple")
            
            plt.show()
        
        
        return vainqueur
    
    
    
    
    def graphe_majo(self, results, start):
        """
        

        Parameters
        ----------
        results : TYPE
            DESCRIPTION.
        start : TYPE
            DESCRIPTION.

        Returns
        -------
        fig : TYPE
            DESCRIPTION.
        ax : TYPE
            DESCRIPTION.

        """
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
    
def quantile(liste, p = 0.5):
    """
    

    Parameters
    ----------
    liste : list
    p : float, optional
        Taux de partitions. Vaut par défaut 0.5.

    Returns
    -------
    int
        quantile de la liste de taux p. 

    """
    assert 0 < p < 1, 'Le taux de partition doit être entre 0 et 1'
    return sorted(liste)[int(len(liste) * p)]






if __name__ == '__main__':
    d = Data("vote film (majoritaire).csv")
    vainqueur = d.jugement_majoritaire(
        compte_pas_vu = True,
        afficher=True,
        taux_de_départage=0.1)
    
    print(vainqueur)
