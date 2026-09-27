"""Module qui gère le choix des mots,
    -choisir_mot choisit un mot aléatoire
    parmi les mots de la langue française
    -verif_mot s'assure qu'un mot est bien
    un nom commun de la langue française"""

from random import choice

def ote_accent(mot):
    a = ['a', 'à', 'â', 'ä']
    e = ['e', 'é', 'è', 'ê', 'ë']
    i = ['i', 'î', 'ï']
    o = ['o', 'ô', 'ö']
    u = ['u', 'ù', 'û', 'ü']
    c = ['c', 'ç']
    apos = ['-', "'"]
    voyelles = [a, c, e, i, o, u, apos]
    for voyelle in voyelles:
        for i in range(1, len(voyelle)):
            mot = mot.replace(voyelle[i], voyelle[0])
    return mot

# construction de la liste de mots
with open("include/dicoNC.csv", "r") as donnees_brutes:
    for num_ln in range(59):
        perdu = donnees_brutes.readline()
    banque_de_noms = [line.split('\t')[1][:-1] for line in donnees_brutes.readlines()]
    dictionnaire = tuple([ote_accent(mot).upper() for mot in banque_de_noms])

def choisir_mot(longueur_min=6, longueur_max=10):
    mot = ''
    while (len(mot) <= longueur_min) or (len(mot) >= longueur_max) or (mot.find('-') != -1):
        mot = choice(dictionnaire)
    return mot

def verif_mot(mot_propose):
    return mot_propose.upper() in dictionnaire    
