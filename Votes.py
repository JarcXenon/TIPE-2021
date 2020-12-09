import random as rd
import matplotlib.pyplot as plt
from individu import Individu, mini, disque
import numpy as np
from copy import deepcopy

"""
Création de population
"""

def crée_population(populations):
    """
    Crée une population
    populations contient la liste des populations (a moyen, b moyen, p moyen, sigma, total, nom)
    """
    population = []
    for pop in populations:
        mua, mub, mup, sigma, k, nom = pop
        for i in range(k):
            a = rd.gauss(mu=mua, sigma=sigma)
            b = rd.gauss(mu=mub, sigma=sigma)
            p = rd.gauss(mu=mup, sigma=sigma)
            individu = Individu(a, b, p=p, nom = nom)
            population.append(individu)
    return population

def crée_partis(listeab):
    """
    Crée la liste des partis
    listeab contient la liste des partis (a, b, nom)
    """
    partis = []
    for k in listeab:
        a, b, nom = k
        parti = Individu(a, b, nom = nom)
        partis.append(parti)
    return partis

"""
Visualisation
"""

"""
Version précédente, on ne s'en sert plus

def plot(population, partis):
    list_a = []
    list_b = []
    list_a2 = []
    list_b2 = []
    for individu in population:
        list_a.append(individu.a)
        list_b.append(individu.b)
    for parti in partis:
        list_a2.append(parti.a)
        list_b2.append(parti.b)
    plt.clf()
    plt.scatter(list_a, list_b, alpha = 0.1)
    plt.scatter(list_a2, list_b2)
    plt.show()
    return None
"""

def heatmap(population, partis):
    list_a = []
    list_b = []
    list_a2 = []
    list_b2 = []
    for individu in population:
        list_a.append(individu.a)
        list_b.append(individu.b)
    for parti in partis:
        list_a2.append(parti.a)
        list_b2.append(parti.b)
    #https://stackoverflow.com/questions/36957149/density-map-heatmaps-in-matplotlib
    Z, xedges, yedges = np.histogram2d(list_a, list_b)
    plt.clf()
    plt.pcolormesh(xedges, yedges, Z.T)
    plt.scatter(list_a2, list_b2, color='r')
    plt.show()
    return None
    
"""
Résultats
"""

def test_election(votes, n_partis=0, n_population=0):
    "Teste un éléction avec le vote donné en argument"
    if n_partis == 0:
        partis = crée_partis([(0.25, 0.25, 'sud ouest'), 
                              (0.25, 0.75, 'nord ouest'), 
                              (0.5, 0.5, 'centre'), (0.75, 0.25, 'sud est'), 
                              (0.75, 0.75, 'nord est')])
    if n_population == 1:
        population = crée_population([(0.5, 0.25, 0.2, 0.15, 25000, "sud"), 
                                      (0.5, 0.75, 0.2, 0.15, 25000, "nord"), 
                                      (0.25, 0.5, 0.2, 0.15, 25000, "ouest"), 
                                      (0.75, 0.5, 0.2, 0.15, 25000, "est")])
    if n_population == 0:
        population = crée_population([(0.25, 0.25, 0.2, 0.15, 25000, "sud ouest"), 
                                      (0.25, 0.75, 0.2, 0.15, 25000, "nord ouest"), 
                                      (0.75, 0.25, 0.2, 0.15, 25000, "sud est"), 
                                      (0.75, 0.75, 0.2, 0.15, 25000, "nord est")])
    heatmap(population, partis)
    resultats = []
    for vote in votes:
        resultats.append(vote(partis, population))
    return resultats

def test_elections(n_partis=0, n_population=0):
    return test_election([main_alternatif, main_approbation, main_condorcet, main_uninominal], n_partis, n_population)

"""
Condorcet
"""

def scrutin_condorcet(partis):
    "crée le scrutins (les duels)"
    scrutin = []
    n = len(partis)
    for i in range(n):
        for j in range(i+1, n):
            #On fait en sorte que chaque parti rencontre tous les autres une fois
            scrutin.append((partis[i], partis[j]))
    return scrutin

def cree_bulletin_condorcet(individu, scrutin):
    "fait voter un individu (crée son bulletin de vote)"
    bulletin= []
    for duel in scrutin:
        #Pour chaque duel
        val1, val2 = duel
        vainqueur = mini(individu, [val1, val2])
        bulletin.append(vainqueur)
    return bulletin

def duel_condorcet(bulletins, scrutin, partis):
    "Réalise le vote"
    score = [0 for k in partis]
    for bulletin in bulletins:
        for vainqueur in bulletin:
            #Pour chaque duel, on ajoute 1 au compte de victoires du vainqueur
            score[partis.index(vainqueur)] += 1
    score_vainqueur = max(score)
    vainqueur = []
    for i in range(len(partis)):
        if score[i] == score_vainqueur:
            vainqueur.append(partis[i])
    return vainqueur, score

def main_condorcet(partis, population):
    "Réalise un vote de Condorcet, renvoie juste le vainnqueur"
    scrutin = scrutin_condorcet(partis)
    bulletins = [cree_bulletin_condorcet(individu, scrutin) for individu in population]
    vainqueur, score = duel_condorcet(bulletins, scrutin, partis)
    nom_partis = [parti.nom for parti in partis]
    plt.clf()
    plt.bar(nom_partis, score)
    plt.show()
    return vainqueur

"""
Uninominal
"""

def cree_bulletins_uninominal(individu, partis):
    "Fait voter un individu (crée un bulletin de vote uninominal)"
    return mini(individu, partis)

def vote_uninominal(bulletins, partis):
    "Dépouille les bulletins"
    score = [0 for k in partis]
    for vote in bulletins:
        score[partis.index(vote)] += 1
    "Trouve le vainqueur"
    score_vainqueur = max(score)
    vainqueur = partis[score.index(score_vainqueur)]
    return (vainqueur, score)

def main_uninominal(partis, population):
    "Réalise le vote uninominal et renvoit le vainqueur"
    bulletins = [cree_bulletins_uninominal(individu, partis) for individu in population]
    vainqueur, score = vote_uninominal(bulletins, partis)
    nom_partis = [parti.nom for parti in partis]
    plt.clf()
    plt.bar(nom_partis, score)
    plt.show()
    return vainqueur

"""
Alternatif
"""
def cree_bulletins_alternatif(individu, partis):
    """Fait voter un individu (crée un bulletin de vote alternatif),
    sous forme de la liste des candidats, dans l'ordre de préférence"""
    liste_choix = deepcopy(partis)
    bulletin = []
    while len(liste_choix) > 0:
        choix = mini(individu, liste_choix)
        liste_choix.remove(choix)
        bulletin.append(choix)
    return bulletin

def min_alternatif(résultats, sortis):
    "Renvoie l'indice du plus petit élément de résultat qui n'est pas dans sortis"
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

def privation(l1, l2):
    "Renvoie l1 privée de l2"
    l = deepcopy(l1)
    for x in l2:
        try:
            l.remove(x)
        except:
            pass
    return l

def vote_alternatif(bulletins, partis):
    l = len(bulletins)
    votes = [[] for k in partis]
    tout = []
    sortis = []
    for vote in bulletins:
        premier_choix = vote[0]
        votes[partis.index(premier_choix)].append(vote)
    résultats = [len(votes[k]) for k in range(len(votes))]
    tout.append(deepcopy(résultats))
    v_premier = max(résultats)
    while 2 * v_premier < l:
        v_dernier = min(privation(résultats, [0 for k in résultats]))
        i_dernier = résultats.index(v_dernier)
        dernier = partis[i_dernier]
        sortis.append(dernier)
        résultats[i_dernier] = 0
        for vote in votes[i_dernier]:
            i = 0
            n = len(vote)
            flag = True
            while i < n and flag:
                if not vote[i] in sortis:
                    premier_choix = vote[i]
                    flag = False
                i += 1
            résultats[partis.index(premier_choix)] += 1
            votes[partis.index(premier_choix)].append(vote)
        tout.append(deepcopy(résultats))
        v_premier = max(résultats)
        print(résultats)
    return résultats.index(max(résultats)), tout

def main_alternatif(partis, population):
    "Réalise le vote alternatif et renvoit le vainqueur"
    bulletins = [cree_bulletins_alternatif(individu, partis) for individu in population]
    vainqueur, résultats = vote_alternatif(bulletins, partis)
    nom_partis = [parti.nom for parti in partis] + ["ordre"]
    n = len(résultats)
    y = max(résultats[-1])
    for j in range(n):
        k = résultats[n-j-1]
        plt.bar(nom_partis, k + [(y*(n-j))/n])
    plt.show()
    return vainqueur

"""
Approbation
"""

def cree_bulletin_approbation(individu, partis):
    """Fait voter un individu (crée un bulletin de vote alternatif),
    sous forme d'une liste de bolléens, dans l'ordre des partis"""
    approuvés = disque(individu, partis)
    bulletin = [parti in approuvés for parti in partis]
    print(individu.nom, bulletin)
    return bulletin

def vote_approbation(bulletins, partis):
    score = [0 for k in partis]
    n = len(partis)
    for vote in bulletins:
        i = 0
        while i < n:
            if vote[i]:
                score[i] += 1
            i += 1
    return partis[score.index(max(score))], score


def main_approbation(partis, population):
    "Réalise le vote par approbation et renvoit le vainqueur"
    bulletins = [cree_bulletin_approbation(individu, partis) for individu in population]
    vainqueur, résultats = vote_approbation(bulletins, partis)
    nom_partis = [parti.nom for parti in partis]
    plt.clf()
    plt.bar(nom_partis, résultats)
    plt.show()
    return vainqueur