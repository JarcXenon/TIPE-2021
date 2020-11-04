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
        
def vote_alternatif(bulletins):
    n = len(partis)
    resultats = []
    score = [0 for k in partis]
    sortis = []
    maxi = max(score)
    tot = len(bulletins)
    while n > 0 and (maxi/tot) < 0.5:
        #FINIR A PARTIR D'ICI
        for vote in bulletins:
            k = vote.index(1)
            i = 1
            while i < n-1 and not k in sortis:
                k = vote.index(1+i)
                i += 1
            score[k] += 1
        mini = min(score)
        sortis.append(score.index(mini))
        n -= 1
        resultats.append(score)
    return score, resultats, sortis, n
        


def main_alternatif():
    bulletins = [cree_bulletins_alternatif(individu) for individu in pop]
    """
    vainqueur, resultats = vote_alternatif(bulletins)
    
    plt.clf()
    plt.bar(partis, score)
    plt.show()
    plt.clf()
    pop_parti = [0 for k in range(len(partis))]
    for ind in pop:
        pop_parti[trouve_parti(ind, partis_pos)] += 1
    plt.bar(partis, pop_parti)
    plt.show()
    return vainqueur, resultats
    """
    return vote_alternatif(bulletins)