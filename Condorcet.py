import random as rd
import matplotlib.pyplot as plt

#variables globales
partis_pos = [0, 1/6, 2/6, 3/6, 4/6, 5/6, 1] #positions des partis sur l'échelle politique
partis = ["extreme gauche", "gauche", "centre gauche", "centre", "centre droit", "droite", "extreme droite"] #liste des partis

pop1 = [rd.gauss(mu=5/6, sigma=0.15) for k in range(100000)]
pop0 = [rd.gauss(mu=1/6, sigma=0.15) for k in range(100000)]
pop = pop0 + pop1 #population de travail

pop_parti=[0 for k in range(7)] 

#Fonction globale
def trouve_parti(individu, liste_partis):
    ##Trouve un parti adapté à un individu
    if individu < liste_partis[0]:
        #Si l'individu est plus à gauche que le parti le plus à gauche, on renvoie le parti le plus à gauche.
        return 0
    if individu > liste_partis[-1]:
        #Si l'individu est plus à droite que le parti le plus à droite, on renvoie le parti le plus à droite.
        return len(liste_partis)-1
    for position in range(len(liste_partis)):
        #On fait défiler les partis de gauche à droite
        parti = liste_partis[position]
        if individu > parti:
            #On vérifie que l'individu est bien à droite du parti, sinon son cas aurait dû être traîté dans les boucles précédentes
            suivant = liste_partis[position+1]
            if individu < suivant:
                #Si l'individu est bien entre le parti étudié et le suivant,
                if individu < (parti + suivant)/2:
                    #Si l'individu est plus proche du parti étudié que du suivant, on renvoit la position de ce parti
                    return position
                else:
                    #Sinon on renvoit la position de l'autre
                    return position+1

"""
Condorcet
"""

def scrutins():
    ##crée le scrutins (les duels)
    scrutin = []
    for i in range(len(partis)) :
        for j in range((i+1), len(partis)) :
            #On fait en sorte que chaque parti rencontre tous les autres
            scrutin.append((i,j))
    return scrutin

def cree_bulletins(individu, scrutin):
    #fait voter un individu (crée son bulletin de vote)
    bulletin = []
    for duel in scrutin:
        #Pour chaque duel,
        val1, val2 = duel
        lvalduel = [partis_pos[val1], partis_pos[val2]]
        vainc = trouve_parti(individu, lvalduel)
        #On cherche le parti le plus proche de l'individu (renvoit 0 si c'est celui de gauche et 1 si c'est celui de droite
        bulletin.append(vainc == 0)
        #On ajoute le résultat du duel au bulletin
    return bulletin


def duel_condorcet(bulletins, scrutin):
    #Dépouille les bulletins
    score = [0 for k in partis]
    for bulletin in bulletins:
        #Pour chaque bulletin,
        for nduel in range(len(bulletin)):
            duel = bulletin[nduel]
            duel1, duel2 = scrutin[nduel]
            if duel :
                score[duel1] += 1
            else :
                score[duel2] += 1
    #Trouve le ou les vainqueurs
    score_vainqueur = max(score)
    vainqueur =[]
    for i in range (len(partis)):
        if score[i] == score_vainqueur:
            vainqueur.append(partis[i])
    return (vainqueur, score)

def main_condorcet():
    #Réalise un vote de Condorcet, renvoie juste le ou les vainnqueurs
    scrutin = scrutins()
    bulletins = [cree_bulletins(individu, scrutin) for individu in pop]
    vainqueur, score = duel_condorcet(bulletins, scrutin)
    return vainqueur

def main_condorcet_graph():
    #Réalise un vote de Condorcet, renvoie le ou les vainqueurs et un graph des résultats du vote
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
    #Fait voter un individu (crée un bulletin de vote uninominal)
    return trouve_parti(individu, partis_pos)

def vote_uninominal(bulletins):
    #Dépouille les bulletins
    score = [0 for k in partis]
    for vote in bulletins:
        score[vote] += 1
    #Trouve le vainqueur
    score_vainqueur = max(score)
    vainqueur = []
    for i in range(len(partis)):
        if score[i] == score_vainqueur:
            vainqueur.append(partis[i])
    return (vainqueur, score)

def main_uninominal():
    #Réalise le vote uninominal et renvoit le ou les vainqueurs
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
    #Fait voter un individu (crée un bulletin de vote alternatif)
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
    #Renvoie l'indice du plus petit élément de résultat qui n'est pas dans sortis
    i = 0
    n = len(résultats)
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
