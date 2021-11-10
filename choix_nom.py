"""Module qui gère le choix des mots,
    -choisir_mot choisit un mot aléatoire
    parmi les mots de la langue française
    -verif_mot s'assure qu'un mot est bien
    un nom commun de la langue française"""

import pandas as pd
from random import randint

banque_de_noms = pd.read_csv("venv/include/dicoNC.csv", usecols=['nom'], sep='\t', skiprows=58)


def choisir_mot(longueur_min=6, longueur_max=10):
    nb_mots = banque_de_noms.nom.count()
    mot = ''
    while (len(mot) <= longueur_min) or (len(mot) >= longueur_max) or (mot.find('-') != -1):
        numero = randint(0, nb_mots-1)
        mot = banque_de_noms.loc[numero].nom
    return ote_accent(mot).upper()


def ote_accent(mot):
    a = ['a', 'à', 'â', 'ä']
    e = ['e', 'é', 'è', 'ê', 'ë']
    i = ['i', 'î', 'ï']
    o = ['o', 'ô', 'ö']
    u = ['u', 'ù', 'û', 'ü']
    c = ['c', 'ç']
    voyelles = [a, c, e, i, o, u]
    for voyelle in voyelles:
        for i in range(1, len(voyelle)):
            mot = mot.replace(voyelle[i], voyelle[0])
    return mot


def verif_mot(mot_propose):
    retour = False
    n = banque_de_noms.nom.count()
    i = 0
    while not retour and i < n:
        retour = mot_propose.upper() == ote_accent(banque_de_noms.loc[i].nom).upper()
        i += 1
    return retour
