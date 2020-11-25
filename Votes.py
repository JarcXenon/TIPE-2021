import random as rd
import matplotlib.pyplot as plt
from individu import Individu, mini, disque

"""
Création de population
"""

def crée_population(populations):
    """
    Crée une population
    populations contient la liste des populations (a moyen, b moyen, p, sigma, total, nom)
    """
    population = []
    for pop in populations:
        mua, mub, p, sigma, k, nom = pop
        for i in range(k):
            a = rd.gauss(mu=mua, sigma=sigma)
            b = rd.gauss(mu=mub, sigma=sigma)
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
    "Réalise un vote de Condorcet, renvoie juste le ou les vainnqueurs"
    scrutin = scrutin_condorcet(partis)
    bulletins = [cree_bulletin_condorcet(individu, scrutin) for individu in population]
    vainqueur, score = duel_condorcet(bulletins, scrutin, partis)
    nom_partis = [parti.nom for parti in partis]
    plt.clf()
    plt.bar(nom_partis, score)
    plt.show()
    return vainqueur

def condorcet(n=0):
    "A déja partis et population de préremplis"
    if n == 0:
        partis = crée_partis([(0.25, 0.25, 'sud ouest'), 
                              (0.25, 0.75, 'nord ouest'), 
                              (0.5, 0.5, 'centre'), (0.75, 0.25, 'sud est'), 
                              (0.75, 0.75, 'nord est')])
        population = crée_population([(0.5, 0.25, 0.25, 0.15, 25000, "sud"), 
                                      (0.5, 0.75, 0.25, 0.15, 25000, "nord"), 
                                      (0.25, 0.5, 0.25, 0.15, 25000, "ouest"), 
                                      (0.75, 0.5, 0.25, 0.15, 25000, "est")])
    plot(population, partis)
    return main_condorcet(partis, population)