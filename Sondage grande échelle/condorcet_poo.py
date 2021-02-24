# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 15:01:23 2020

@author: maelys
"""

import matplotlib.pyplot as plt

class Data():
    
    def __init__(self, file=None, tableau=None, choix=None):
        self.file = file
        if file:
            with open(file, "r") as f:
                
                lines = []
                line = f.readline().strip('\n')
                lines += line.split(';')
                line = f.readline().strip('\n')
                while not line[0].isnumeric():
                    line = line.split(';')
                    lines[-1] += '\n' + line[0]
                    line = line[1:]
                    lines += line
                    line = f.readline().strip('\n')
                self.choix = lines[:-1]
                
                lines = [line]
                lines += f.readlines()
                self.votes = []
                
                for line in lines:
                    vote = line.split(',')
                    self.votes.append([int(n) for n in vote])
        if tableau:
            self.votes = tableau
        if choix:
            self.choix = choix
        
    def __repr__(self):
        return f'Data({self.file}, {self.choix})'
    
    def condorcet(self, afficher = False):
        score = [0 for _ in self.choix]
        
        n = len(self.choix)
        for i in range(n):
            for j in range(i+1, n):
                li =0
                lj =0
                for vote in self.votes:
                    if vote[i]<vote[j]:
                        li += 1
                    else:
                        lj += 1
                if li < lj:
                    score[j] += 1
                else:
                    score[i] += 1           
        if afficher:
            plt.clf()
            plt.bar(self.choix, score, color = 'b')
        
        score_vainc = max(score)
        print("Vainqueur(s) :")
        for i in range (n):
            if score[i] == score_vainc:
                print(self.choix[i])
        if score_vainc == n:
            print("C'est un vainqueur de Condorcet")
        else :
            print("Il n'y a pas de vainqueur de Condorcet")


"""
a = Data(file = "vote classement.csv")
a.condorcet(afficher = True)
"""

b = Data(file = 'condorcet.csv')
b.condorcet(afficher = True)