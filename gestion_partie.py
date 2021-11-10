# la classe gestion_partie s'occupe de la gestion du jeu quand le mot est choisi
erreurs_max = 8


class Partie:
    """
    Classe qui gère la partie de pendu à partir d'un mot donné
    et du nombre d'erreurs qui normalement vaut 8.
    @ attributs:
        _mot_a_trouver (str) déclaré dans l'initiateur
        _lettres_proposees (set) set de char initialisé aux lettres de début et de fin de __mot_a_trouver
        _nb_erreurs (int) initialisé à 8 par défaut
        _gagne (bool)initialisé à False
        _perdu (bool)initialisé à False
    @ méthodes:
        __init__(mot_mystère: str, nb_erreurs=erreurs_max: int)
        reset_mot_a_trouver(self, mot_propose) relance le jeu et réinitialise les attributs
        get_gagne()->bool       renvoie _gagne
        get_perdu()->bool       renvoie _perdu
        get_propose()->set(str) renvoie _lettres_proposees
        mot_affiche()->str      renvoie le str à afficher au fil de la partie
        __ajoute_erreur__()     modifie _nb_erreurs (et _perdu selon les cas)
        propose_lettre(str)     modifie _lettres_proposees (et applique __ajoute_erreur__ ou modifie _gagne)
        propose_mot(str)        compare _mot_a_trouver (et applique __ajoute_erreur__ ou modifie _gagne)
    """
    def __init__(self, mot_mystere=None, nb_erreurs=erreurs_max):
        self._mot_a_trouver = mot_mystere
        if mot_mystere is not None:
            self._lettres_proposees = {mot_mystere[0], mot_mystere[-1]}
        else:
            self._lettres_proposees = set()
        self._nb_erreurs = nb_erreurs
        self._gagne = False
        self._perdu = False

    @property
    def __repr__(self):
        return f"Jeu de pendu:\n\nnbr d'erreurs: {8-self._nb_erreurs}\nmot à trouver: {self.mot_affiche()}"

    def reset_mot_a_trouver(self, mot_propose):
        self._mot_a_trouver = mot_propose
        self._lettres_proposees = set()
        self._nb_erreurs = erreurs_max
        self._gagne = False
        self._perdu = False

    def get_gagne(self):
        return self._gagne

    def get_perdu(self):
        return self._perdu

    def get_proposees(self):
        return self._lettres_proposees

    def get_erreurs(self):
        return self._nb_erreurs

    def mot_affiche(self):
        if len(self._mot_a_trouver) <= 2:
            return self._mot_a_trouver
        ln = len(self._mot_a_trouver)
        affiche = ln*"-"
        for i in range(ln):
            if self._mot_a_trouver[i] in self._lettres_proposees:
                affiche = affiche[:i] + self._mot_a_trouver[i] + affiche[i+1:]
        return affiche

    def __ajoute_erreur__(self):
        self._nb_erreurs -= 1
        if self._nb_erreurs == 0:
            self._perdu = True

    def propose_lettre(self, lettre):
        self._lettres_proposees.add(lettre)
        if lettre not in self._mot_a_trouver:
            self.__ajoute_erreur__()
        if self.mot_affiche() == self._mot_a_trouver:
            self._gagne = True

    def propose_mot(self, mot):
        if mot == self.mot_affiche():
            self._gagne = True
        else:
            self.__ajoute_erreur__()
