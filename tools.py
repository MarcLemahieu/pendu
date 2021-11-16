## Ce fichier implémente tous les éléments de jeu qui dépendent de la librairie Tkinter
## et qui s'insèreront dans la fenètre principale.

import tkinter as tk
import choix_nom as cn
import tkinter.simpledialog
import gestion_partie as gp

## déclaration des constantes des éléments graphiques
bkgd = "#127622"                                        # couleur du fond
fontcolor = "#e6e905"                                   # couleur de dessin
fontcolor2 = "#ff5505"                                  # couleur de police de fin de jeu
police = ('Chilanka', 20, 'bold')                       # police d'écriture
cles_touches = ["AZERTYUIOP", "QSDFGHJKLM", "WXCVBN"]   # organisation des touches pour le clavier


class Trace(tk.Canvas):
    """trace un canvas avec le pendu en fonction du nombre d'erreurs atteint
    @ attributs:
    _e : int  permet de modifier la taille du cavas
    @ methodes:
    update_canvas(partie: gp.Partie) met à jour le canvas en fonction de partie._nb_erreurs
    """
    def __init__(self,master, etape):
        super().__init__(master)
        self._e = 45
        e = self._e
        self.config(height=12*e, width=9*e, bg=bkgd, bd=0)
        for i in range(9-etape):
            self.__etapes_traces__()[i](e)

    def update_canvas(self, partie: gp.Partie):
        etape = partie.get_erreurs()
        lst_construct = self.__etapes_traces__()[0:9-etape]
        self.delete("all")
        if partie.get_gagne():
            self.__trace_victoire__(self._e)
        else:
            for f in lst_construct:
                f(self._e)

    def __etapes_traces__(self):
        couleur = fontcolor
        larg = 6
        f0 = lambda e: self.create_line(e, 10*e, 8*e, 10*e, width=larg, fill=couleur, capstyle='round')
        f1 = lambda e: self.create_line(3*e, 10*e, 3*e, 2*e, width=larg, fill=couleur, capstyle='round')
        f2 = lambda e: self.create_line(3*e, 2*e, int(6.3*e), 2*e, width=larg, fill=couleur, capstyle='round')
        f3 = lambda e: self.create_line(3*e, 4*e, 5*e, 2*e, width=larg, fill=couleur, capstyle='round')
        f4 = lambda e: self.create_line(6*e, 2*e, 6*e, 4*e, width=larg, fill=couleur, capstyle='round')
        f5 = lambda e: self.create_oval(int(5.5*e), 4*e, int(6.5*e), 5*e, width=larg, outline=couleur)
        f6 = lambda e: self.create_line(6*e, 5*e, 6*e, int(6.5*e), width=larg, fill=couleur, capstyle='round')
        f7 = lambda e: self.create_line(5*e, int(5.5*e), 7*e, int(5.5*e), width=larg, fill=couleur, capstyle='round')
        f8 = lambda e: self.__trace_defaite__(e)
        return f0, f1, f2, f3, f4, f5, f6, f7, f8

    def __trace_victoire__(self, e):
        p = (police[0], police[1]*2, police[2])
        self.create_text(int(4.5*e), 8*e, text="Vous avez\ngagné!!!", fill=fontcolor2, font=p, justify='center')

    def __trace_defaite__(self, e):
        larg = 6
        p = (police[0], police[1]*2, police[2])
        self.create_line(5*e, int(8.5*e), 6*e,
                         int(6.5*e),7*e,int(8.5*e), width=larg, fill=fontcolor, capstyle='round')
        self.create_text(int(4.5*e), 8*e, text="Vous avez\nperdu", fill=fontcolor2, font=p, justify='center')


class Furoncle(tk.Button):
    """implémente les touches des lettres de l'alphabet pour le pendu
    @ attributs:
    self._valeur: str ATTENTION, réduit à un unique caractère
    @ methodes:
    command_bouton(partie: gp.Partie, cnv: Trace,
                clavier: Clavier, affiche: A_trouver, entree: Entree, menu: MenuPendu) implémente la réponse
                au clic pendant le déroulé de la partie
    """
    def __init__(self, master, lettre:str):
        super().__init__(master)
        self.config(text=lettre, bg=bkgd, fg=fontcolor, font=police, borderwidth=0)
        self._valeur = lettre


    def command_bouton(self, partie: gp.Partie, cnv: Trace, clavier, affiche, entree, menu):
        self.config(state=tk.DISABLED)
        partie.propose_lettre(self._valeur) # on ajoute la lettre aux lettres proposées
        cnv.update_canvas(partie)           # on actualise le canvas
        affiche.update_affichage(partie)    # on actualise l'afichage du mot
        if partie.get_gagne() or partie.get_perdu():    # si on gagne la partie
            entree.config(state=tk.DISABLED)    # on désactive l'entrée clavier
            for bouton in clavier.get_buttons(): # on désactive tous les boutons du clavier
                bouton.config(state=tk.DISABLED)
            menu.enable_menus()             # on réactive les menus
            if partie.get_perdu():
                affiche.config(text=menu.get_mot_mystere()) # on affiche le mot non trouvé


class Clavier(tk.Frame):
    """implémente un clavier et permet de récupérer la liste
    des boutons qui le composent (la répartition des touches est donnée par la constante globale cles_touches
    @ attributs:
    _subframes: tk.Frame qui contient les frames qui formeront les lignes de boutons du clavier
    _touches : qui est la liste de tout les boutons du clavier.
    @ methodes:
    get_buttons() qui renvoie l'attribut _touches
    """
    def __init__(self, master):
        super().__init__(master)
        self.config(bg=bkgd)
        self._subframes=list()
        self._touches = list()
        for ligne in range(len(cles_touches)):
            f = tk.Frame(self)
            self._subframes.append(f)
            for car in cles_touches[ligne]:
                touche = Furoncle(f, car)
                touche.grid(column = cles_touches[ligne].find(car), row = 0)
                self._touches.append(touche)
            f.grid(row=ligne)

    def get_buttons(self):
        """renvoie la liste des boutons du clavier"""
        return self._touches


class MenuPendu(tk.Menu):
    """pour créer un menu qui permettra de choisir des mots au hasard
    ou en les saisissant à condition qu'ils soient dans le dico (forçage possible)
    @ attributs:
    __mot_mystere: str qui va héberger le mot à trouver au moment du choix par une des deux commandes
            'Choisir nom' et 'Nom aléatoire'
    @ methodes:
    get_mot_mystere() -> str qui renvoie __mot_mystère utile à l'affichage de fin de jeu dans
                                les commandes de button et de Entry.
    enable_menu() qui réactive les menus en fin de partie dans les commandes de button et de Entry

    __lancement_partie__(partie, trace, atrouver, clavier, entree)
    __choix_alea__(partie, trace, atrouver, clavier, entree)
    __choix_user__(partie, trace, atrouver, clavier, entree)
                        sont les trois commandes qui sont activées dans le menu à l'initalisation du jeu
    """
    def __init__(self,fenetre, partie, trace, atrouver, clavier, entree):
        """
        crée les menus et gère les interactions de lancement entre les objets de l'application
        fenetre: tk.Tk
        partie: gp.Partie
        trace: Trace
        atrouver: A_trouver
        clavier: Clavier
        entree: Entree
        """
        super().__init__(fenetre)
        self.__mot_mystere = None # stockera le mot mystère
        self.menu_partie = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Partie", menu= self.menu_partie)
        self.menu_partie.add_command(label="Choisir nom", command=lambda  : self.__choix_user__(partie, trace, atrouver, clavier, entree))
        self.menu_partie.add_command(label="Nom aléatoire", command=lambda  : self.__choix_alea__(partie, trace, atrouver, clavier, entree))
        self.menu_partie.add_separator()
        self.menu_partie.add_command(label="Quitter", command=quit)
        fenetre.config(menu=self)

    def get_mot_mystere(self):
        return self.__mot_mystere

    def enable_menus(self):
        """permet en fin de partie de réactiver les menu"""
        self.menu_partie.entryconfigure(0, state=tk.ACTIVE)
        self.menu_partie.entryconfigure(1, state=tk.ACTIVE)

    def __choix_alea__(self, partie, trace, atrouver, clavier, entree):
        """choisit un mot aléatoirement dans les noms commun du dico csv.
        puis désactive les deux menus de choix"""
        self.__mot_mystere = cn.choisir_mot()
        # print(self.__mot_mystere)
        self.__lancement_partie__(partie, trace, atrouver, clavier, entree)

    def __choix_user__(self, partie, trace, atrouver, clavier, entree):
        """ouvre une boite de dialogue pour proposer un mot et le vérifie
        puis déactive les deux menus de choix"""
        while True:
            mot = tkinter.simpledialog.askstring(title="entre un nom", prompt="", initialvalue= "votre proposition", show="#")
            if not cn.verif_mot(mot):
                if tk.messagebox.askyesno(title="ATTENTION",message="mot absent du dico\nle conserver?"):
                    self.__mot_mystere = cn.ote_accent(mot).upper()
                    self.__lancement_partie__(partie, trace, atrouver, clavier, entree)
                    break
            else:
                self.__mot_mystere = cn.ote_accent(mot).upper()
                self.__lancement_partie__(partie, trace, atrouver, clavier, entree)
                break

    def __lancement_partie__(self, partie, trace, atrouver, clavier, entree):
        """
        active les écouteurs des widgets du jeu en même temps qu'elle initialise partie
        partie: gp.Partie,
        trace: Trace,
        atrouver: A_trouver,
        clavier: Clavier,
        entree: Entree
        """
        partie.reset_partie(self.__mot_mystere) #on initialise la partie avec le mot choisi.
        atrouver.update_affichage(partie)# on actualise l'affichage avec partie
        trace.update_canvas(partie)# on actualise le canvas
        for bouton in clavier.get_buttons():# on active tous les boutons du clavier
            bouton.config(state=tk.NORMAL)
            bouton.bind("<Button-1>", lambda evt, but=bouton : but.command_bouton(partie, trace, clavier, atrouver, entree, self))
        entree.config(state=tk.NORMAL) #on active la barre de saisie
        entree.bind("<Return>", lambda evt: entree.retour_entree(partie, clavier, trace, atrouver, self))
        self.menu_partie.entryconfigure(0, state=tk.DISABLED)#on désactive les menus
        self.menu_partie.entryconfigure(1, state=tk.DISABLED)


class Entree(tk.Entry):
    """classe qui autorise les saisies clavier pour jouer un mot ou une lettre.
    @ attributs:

    @ methodes:
    retour_entree(partie: gp.Partie, clavier: Clavier, dessin: Trace, affiche: A_trouver, menu: MenuPendu)
                    qui gère la commande de l'objet à la saisie du retour chariot
    """
    def __init__(self, master):
        super().__init__(master)
        self.config(bg=bkgd, fg=fontcolor, font=police, width=22, selectborderwidth=5, state=tk.DISABLED)


    def retour_entree(self,partie, clavier, dessin, affiche, menu):
        """methode qui permet la gestion de la saisie du retour chariot"""
        proposition = cn.ote_accent(self.get()).upper()
        if len(proposition) > 1: # si on saisit plus d'un caractère
            partie.propose_mot(proposition) #on ne met pas à jour l'affichage ce serait redondant.
        elif len(proposition) == 1: #si on ne saisit qu'un caractère
            partie.propose_lettre(proposition)
            affiche.update_affichage(partie)
        dessin.update_canvas(partie)
        self.delete(0, len(self.get()))
        if partie.get_perdu() or partie.get_gagne():
            affiche.config(text=menu.get_mot_mystere())
            menu.enable_menus()
            for bouton in clavier.get_buttons():
                bouton.config(state=tk.DISABLED)
            self.config(state=tk.DISABLED)


class A_trouver(tk.Label):
    """ la classe A_trouver surclasse Label pour l'affichage du mot caché en découvrant à chaque phase du jeu
    sa mise à jour.
    @ attributs:

    @ methodes:
    update_affichage(partie: gp.Partie) qui met à jour l'affichage avec partie.mot_affiche()
    """
    def __init__(self,master, txt=""):
        super().__init__(master)
        p = (police[0],police[1]+5,police[2])
        self.config(bg=bkgd, fg=fontcolor, font=p, borderwidth=0)
        self.config(text=txt)

    def update_affichage(self, partie: gp.Partie):
        self.config(text=partie.mot_affiche())
