import tkinter as tk
import tools as tls
import gestion_partie as gp

class FenetrePendu:
    """classe principale du jeu de pendu qui se contente d'organiser les différents objets du jeu dans la fenêtre"""
    def __init__(self):
        # 1) Création de la gestion de partie
        self.__partie = gp.Partie(mot_mystere=None)

        # 2) Création de la fenètre principale
        self.__fenetre = tk.Tk()
        self.__fenetre.config(bg=tls.bkgd)
        self.__fenetre.title("un pendu sinon rien")
        self.__fenetre.tk.call('wm', 'iconphoto', self.__fenetre._w,
                               tk.PhotoImage(file='venv/include/iconeNSI.png'))

        # 3) Création et placement du Canvas de dessin de pendu
        self.__dessin = tls.Trace(self.__fenetre, 8)
        self.__dessin.grid(column=1, row=0, rowspan=6)

        # 4) Création et placement du label d'affichage
        self.__affiche = tls.A_trouver(self.__fenetre, "P---U")
        self.__affiche.grid(column=0, row=1)

        # 5) Création et placement du clavier de boutons
        self.__clavier = tls.Clavier(self.__fenetre)
        self.__clavier.grid( column=0, row=5)

        # 6) Création et placement du champ de saisie
        self.__entre_mot = tls.Entree(self.__fenetre)
        self.__entre_mot.grid(column=0, row=3)

        # 7) Création du menu partie
        self.__menu = tls.MenuPendu(self.__fenetre, self.__partie, self.__dessin, self.__affiche, self.__clavier, self.__entre_mot)

        self.__fenetre.mainloop()


def main():
    FenetrePendu()


if __name__ == "__main__":
    main()
