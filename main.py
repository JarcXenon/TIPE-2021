"""
Main page des votes
"""

import random as rd

partis_pos = [0, 1/6, 2/6, 3/6, 4/6, 5/6, 1] #positions des partis sur l'échelle politique
partis = ["extreme gauche", "gauche", "centre gauche", "centre", "centre droit", "droite", "extreme droite"] #liste des différents partis

#création d'une population
pop1 = [rd.gauss(mu=1/6, sigma=0.15) for k in range(100000)]
pop0 = [rd.gauss(mu=3/6, sigma=0.15) for k in range(100000)]
pop = pop0 + pop1

def trouve_parti(individu, liste_partis):
    #trouve un parti adapté à un individu
    if individu < liste_partis[0]:
        return 0
    if individu > liste_partis[-1]:
        return len(liste_partis)-1
    for pos in range(len(liste_partis)):
        valbasse = liste_partis[pos]
        if individu > valbasse:
            valhaute = liste_partis[pos+1]
            if individu < valhaute:
                if individu < (valbasse+valhaute)/2:
                    return pos
                else:
                    return pos+1