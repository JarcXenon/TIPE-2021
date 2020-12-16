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

    Parameters
    ----------
    populations : list tuple (float, float, float, float, float, string)
        Liste des différentes populations-type.
        Le tuple contient les arguments pour créer un groupe de la
        population-type
        (a moyen, b moyen, p moyen, écart-type, total, nom)
    Returns
    -------
    population : list Individu
        Liste de toute la population-type.

    """
    population = []
    for arguments in populations:
        mua, mub, mup, sigma, k, nom = arguments
        for i in range(k):
            a = rd.gauss(mu=mua, sigma=sigma)
            b = rd.gauss(mu=mub, sigma=sigma)
            p = rd.gauss(mu=mup, sigma=sigma)
            individu = Individu(a, b, p=p, nom = nom)
            population.append(individu)
    return population

def crée_partis(liste_partis):
    """

    Parameters
    ----------
    listeab : list tuple (float, float, string)
        Le tuple contient les arguments pour créer un parti.
        (a, b, nom)

    Returns
    -------
    partis : list Individu
        Liste des partis

    """
    partis = []
    for arguments in liste_partis:
        a, b, nom = arguments
        parti = Individu(a, b, nom = nom)
        partis.append(parti)
    return partis

"""
Visualisation
"""

def heatmap(population, partis):
    """
    
    Parameters
    ----------
    population : list Individu
        Liste de toute la population-type.
    partis : list Individu
        Liste de tout les partis.

    Returns
    -------
    None.
    Crée une heatmap de la population ainsi que des points correspondant
    aux partis.

    """
    
    list_a = []
    list_b = []
    list_a2 = []
    list_b2 = []
    #On crée les listes de points qui correspondent aux partis et population
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
    """

    Parameters
    ----------
    votes : list funcction
        liste des votes que l'on veut tester.
    n_partis : int, optional
        numéro de la répartition de partis que l'on veut tester.
        Vaut 0 par défaut.
    n_population : int, optional
        numéro de la population-type que l'on veut tester.
        Vaut 0 par défaut.

    Returns
    -------
    resultats : list Individu
        Renvoie le tableau des candidats élus par chaque vote.

    """
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
    """

    Parameters
    ----------
    n_partis : int, optional
        numéro de la répartition de partis que l'on veut tester.
        Vaut 0 par défaut.
    n_population : int, optional
        numéro de la population-type que l'on veut tester.
        Vaut 0 par défaut.

    Returns
    -------
    resultats : list Individu
        Renvoie le tableau des candidats élus par chaque vote.

    """
    return test_election([main_alternatif, main_approbation, main_condorcet,
                          main_uninominal], n_partis, n_population)

"""
Condorcet
"""

def scrutin_condorcet(partis):
    """
    
    Parameters
    ----------
    partis : list Individu
        Tableau des partis candidats.

    Returns
    -------
    scrutin : list tuple (Individu, Individu)
        Tableau des duels du scrutin de condorcet

    """
    scrutin = []
    n = len(partis)
    for i in range(n):
        for j in range(i+1, n):
            #On fait en sorte que chaque parti rencontre tous les autres une fois
            scrutin.append((partis[i], partis[j]))
    return scrutin

def cree_bulletin_condorcet(individu, scrutin):
    """

    Parameters
    ----------
    individu : Individu
        L'individu que l'on fait voter.
    scrutin : list tuple (Individu, Individu)
        Tableau des duels du scrutin de condorcet.

    Returns
    -------
    bulletin : list Individu
        Renvoie un tableau qui contient, pour chaque duel du scrutin,
        le candidat préféré du duel.

    """
    bulletin= []
    for duel in scrutin:
        #Pour chaque duel
        val1, val2 = duel
        vainqueur = mini(individu, [val1, val2])
        bulletin.append(vainqueur)
    return bulletin

def duel_condorcet(bulletins, scrutin, partis):
    """

    Parameters
    ----------
    bulletins : list list Individu
        Tableau des bulletins de la population
        (Sous la forme du tableau qui contient le gagnant de chaque duel)
    scrutin : scrutin : list tuple (Individu, Individu)
        Tableau des duels du scrutin de condorcet.
    partis : list Individu
        Tableau des partis candidats.

    Returns
    -------
    vainqueur : Individu
        Parti vainqueur
        Ici, celui qui a gagné le plus de duels
    score : list int
        Tableau du nombre de duels gagnés pour chaque parti

    """
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
    """

    Parameters
    ----------
    partis : list Individu
        Tableau des partis candidats.
    population : list Individu
        Tableau des individus que l'on fait voter.

    Returns
    -------
    vainqueur : Individu
        Parti vainqueur
        Ici, celui qui a gagné le plus de duels.
    Réalise un graphe du nombre de duels gagnés par chaque condidat
    """
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
    """

    Parameters
    ----------
    individu : Individu
        L'individu que l'on fait voter.
    partis : list Individu
        Tableau des partis candidats.
        
    Returns
    -------
    Individu
        Renvoie le candidat préféré de l'individu parmis les candidats.

    """
    return mini(individu, partis)

def vote_uninominal(bulletins, partis):
    """

    Parameters
    ----------
    bulletins : list list Individu
        Tableau des bulletins de la population
    partis : list Individu
        Tableau des partis candidats.

    Returns
    -------
    vainqueur : Individu
        Parti vainqueur
    score : list int
        Tableau du nombre de votes pour chaque parti

    """
    score = [0 for k in partis]
    for vote in bulletins:
        score[partis.index(vote)] += 1
    score_vainqueur = max(score)
    vainqueur = partis[score.index(score_vainqueur)]
    return (vainqueur, score)

def main_uninominal(partis, population):
    """
    

    Parameters
    ----------
    partis : list Individu
        Tableau des partis candidats.
    population : list Individu
        Tableau des individus que l'on fait voter.

    Returns
    -------
    vainqueur : Individu
        Parti vainqueur
        Ici, le premier choix du plus d'élécteurs
    Réalise un graphe du nombre de votes reçus par chaque condidat

    """
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
    """

    Parameters
    ----------
    individu : Individu
        L'individu que l'on fait voter.
    partis : list Individu
        Tableau des partis candidats.

    Returns
    -------
    bulletin : list Individu
        Renvoie un tableau qui contient les candidats
        dans l'ordre de préférence de l'individu.
    """
    liste_choix = deepcopy(partis)
    bulletin = []
    while len(liste_choix) > 0:
        choix = mini(individu, liste_choix)
        liste_choix.remove(choix)
        bulletin.append(choix)
    return bulletin

def privation(l1, l2):
    """

    Parameters
    ----------
    l1 : list
        contient une liste dont on veut retirer des éléments.
    l2 : list
        contient la liste des éléments que l'on veut retirer.

    Returns
    -------
    l : list
        l1 privée de l2.

    """
    l = deepcopy(l1)
    for x in l2:
        try:
            l.remove(x)
        except:
            pass
    return l

def vote_alternatif(bulletins, partis):
    """
    

    Parameters
    ----------
    bulletins : list list Individu
        Tableau des bulletins de la population
    partis : list Individu
        Tableau des partis candidats.

    Returns
    -------
    vainqueur : Individu
        Parti vainqueur
    tout : list list int
        Tableau du nombre de vote pour chaque parti
        à chaque éléction successive.

    """
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
        vainqueur = partis[résultats.index(max(résultats))]
    return vainqueur, tout

def main_alternatif(partis, population):
    """
    

    Parameters
    ----------
    partis : list Individu
        Tableau des partis candidats.
    population : list Individu
        Tableau des individus que l'on fait voter.

    Returns
    -------
    vainqueur : Individu
        Parti vainqueur
        Ici, le premier candidat à passer 50% des voix à une election
    Réalise un graphe du nombre de votes reçus par chaque condidat
    à chaque éléction

    """
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
    """
    
    Parameters
    ----------
    individu : Individu
        L'individu que l'on fait voter.
    partis : list Individu
        Tableau des partis candidats.

    Returns
    -------
    bulletin : list bool
        Tableau de bolléens correspondant à si l'indivdu approuve
        de chaque parti, dans l'ordre des partis.

    """
    approuvés = disque(individu, partis)
    bulletin = [parti in approuvés for parti in partis]
    return bulletin

def vote_approbation(bulletins, partis):
    """

    Parameters
    ----------
    bulletins : list list Individu
        Tableau des bulletins de la population
    partis : list Individu
        Tableau des partis candidats.

    Returns
    -------
    vainqueur : Individu
        Parti vainqueur
    score : list int
        Tableau du nombre d'individus qui approvent chaque parti

    """
    score = [0 for k in partis]
    n = len(partis)
    for vote in bulletins:
        i = 0
        while i < n:
            if vote[i]:
                score[i] += 1
            i += 1
        vainqueur = partis[score.index(max(score))]
    return vainqueur, score


def main_approbation(partis, population):
    """

    Parameters
    ----------
    partis : list Individu
        Tableau des partis candidats.
    population : list Individu
        Tableau des individus que l'on fait voter.

    Returns
    -------
    vainqueur : Individu
        Parti vainqueur
        Ici, le candidat approuvé par le plus d'individus
    Réalise un graphe du nombre de votes reçus par chaque condidat

    """
    bulletins = [cree_bulletin_approbation(individu, partis) for individu in population]
    vainqueur, résultats = vote_approbation(bulletins, partis)
    nom_partis = [parti.nom for parti in partis]
    plt.clf()
    plt.bar(nom_partis, résultats)
    plt.show()
    return vainqueur