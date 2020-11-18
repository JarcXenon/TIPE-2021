import random as rd
import matplotlib.pyplot as plt

partis_pos = [0, 1/6, 2/6, 3/6, 4/6, 5/6, 1] #positions des partis sur l'échelle politique
partis = ["extreme gauche", "gauche", "centre gauche", "centre", "centre droit", "droite", "extreme droite"]

pop1 = [rd.gauss(mu=5/6, sigma=0.15) for k in range(100000)]
pop0 = [rd.gauss(mu=1/6, sigma=0.15) for k in range(100000)]
pop = pop0 + pop1

pop_parti=[0 for k in range(7)]

def scrutins():
    #creer le scrutins (les duels)
    scrutin = []
    for i in range(len(partis)) :
        for j in range((i+1), len(partis)) :
            scrutin.append((i,j))
    return scrutin

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

def cree_bulletins(individu, scrutin):
    bulletin = []
    for duel in scrutin:
        val1, val2 = duel
        lvalduel = [partis_pos[val1], partis_pos[val2]]
        vainc = trouve_parti(individu, lvalduel)
        bulletin.append(vainc == 0)
    return bulletin


def duel_condorcet(bulletins, scrutin):
     #on dépouille les bulletins
    score = [0 for k in partis]
    for bulletin in bulletins:
        for nduel in range(len(bulletin)):
            duel = bulletin[nduel]
            duel1, duel2 = scrutin[nduel]
            if duel :
                score[duel1] += 1
            else :
                score[duel2] += 1
    #On trouve le ou les vainqueurs
    score_vainqueur = max(score)
    vainqueur =[]
    for i in range (len(partis)):
        if score[i] == score_vainqueur:
            vainqueur.append(partis[i])
    return (vainqueur, score)

def main_condorcet():
    scrutin = scrutins()
    bulletins = [cree_bulletins(individu, scrutin) for individu in pop]
    vainqueur, score = duel_condorcet(bulletins, scrutin)
    return vainqueur

def main_condorcet_graph():
    scrutin = scrutins()
    bulletins = [cree_bulletins(individu, scrutin) for individu in pop]
    vainqueur, score = duel_condorcet(bulletins, scrutin)
    plt.clf()
    plt.bar(partis, score)
    plt.show()
    plt.clf()
    pop_parti = [0 for k in range(len(partis))]
    for ind in pop:
        pop_parti[trouve_parti(ind, partis_pos)] += 1
    plt.bar(partis, pop_parti)
    plt.show()
    return vainqueur

"""
Uninominal
"""

def cree_bulletins_uninominal(individu):
    return trouve_parti(individu, partis_pos)

def vote_uninominal(bulletins):
    score = [0 for k in partis]
    for vote in bulletins:
        score[vote] += 1
    #On trouve le vainqueur
    score_vainqueur = max(score)
    vainqueur = []
    for i in range(len(partis)):
        if score[i] == score_vainqueur:
            vainqueur.append(partis[i])
    return (vainqueur, score)

def main_uninominal():
    bulletins = [cree_bulletins_uninominal(individu) for individu in pop]
    vainqueur, score = vote_uninominal(bulletins)
    plt.clf()
    plt.bar(partis, score)
    plt.show()
    plt.clf()
    pop_parti = [0 for k in range(len(partis))]
    for ind in pop:
        pop_parti[trouve_parti(ind, partis_pos)] += 1
    plt.bar(partis, pop_parti)
    plt.show()
    return vainqueur

"""
Alternatif
"""
def cree_bulletins_alternatif(individu):
    liste_choix = partis_pos.copy()
    n = len(liste_choix)
    bulletin = [0 for k in liste_choix]
    for k in range(n):
        liste_choix[k] = abs(liste_choix[k] - individu)
    for i in range(n):
        maxi = liste_choix[0]
        val_maxi = 0
        for k in range(1,n):
            if liste_choix[k] > maxi:
                maxi = liste_choix[k]
                val_maxi = k
        liste_choix[val_maxi] = -1
        bulletin[val_maxi] = n-i
    return bulletin
        

def min_alternatif(résultats, sortis):
    i = 0
    n = len(résultats)
    #print(résultats, sortis)
    while i < n and i in sortis:
        i += 1
    imax = résultats[i]
    k = i
    while k < n:
        if imax > résultats[k] and not k in sortis:
            i = k
            imax = résultats[k]
        k += 1
    return i
    

def vote_alternatif(bulletins):
    l = len(bulletins)
    votes = [[] for k in partis]
    tout = []
    sortis = []
    for vote in bulletins:
        k = vote.index(1)
        votes[k].append(vote)
    résultats = [len(votes[k]) for k in range(len(votes))]
    tout.append(résultats.copy())
    premier = max(résultats)
    while 2 * premier < l:
        dernier = min_alternatif(résultats, sortis)
        sortis.append(dernier)
        résultats[dernier] = 0
        for vote in votes[dernier]:
            k = min_alternatif(vote, sortis)
            votes[k].append(vote)
            résultats[k] += 1
        tout.append(résultats.copy())
        premier = max(résultats)
    return résultats.index(max(résultats)), tout
    

def main_alternatif():
    bulletins = [cree_bulletins_alternatif(individu) for individu in pop]
    vainqueur, résultats = vote_alternatif(bulletins)
    n = len(résultats)
    y = max(résultats[-1])
    for j in range(n):
        k = résultats[n-j-1]
        plt.bar(partis + ["ordre"], k + [(y*(n-j))/n])
        plt.show()
    return vainqueur