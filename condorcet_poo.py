# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 15:01:23 2020

@author: maelys
"""

import matplotlib.pyplot as plt

class Data():
    
    def __init__(self, file):
        self.file = file
        
        with open(file, "r") as f:
            
            self.partis = f.readline().strip('\n').split(',')[1:]
            lines = f.readlines()
            
            self.votes = []
            
            for line in lines:
                vote = line.split(',')
                self.votes.append([int(n) for n in vote])
        
    def __repr__(self):
        return f'Data({self.file}, {self.partis})'
    
    def condorcet(self, afficher = False):
        score = [0 for _ in self.partis]
        
        n = len(self.partis)
        for i in range(n):
            for j in range((i+1), n):
                for vote in self.votes:
                    li =0
                    lj =0
                    if vote[i]<vote[j]:
                        lj += 1
                    else:
                        li += 1
                if li < lj:
                    score[j] += 1
                else:
                    score[i] += 1           
        if afficher:
            plt.clf()
            plt.plot(self.partis, score, color = 'b')
        
        score_vainqueur = max(score)
        vainc = []
        for i in range (n):
            if score[i] == score_vainqueur:
                vainc.append(self.partis[i])
        return vainc