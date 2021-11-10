import tkinter as tk
import choix_nom as cn
import tkinter.simpledialog
import gestion_partie as gp

bkgd = "#127622"
fontcolor = "#e6e905"
fontcolor2 = "#ff5505"
police = ('Chilanka', 15, 'bold')


class Trace(tk.Canvas):
    """trace un canvas avec le pendu en fonction du nombre d'erreurs atteint"""
    def __init__(self,master, etape):
        super().__init__(master)
        self._e=39
        e = self._e
        self.config(height=12*e, width=9*e, bg=bkgd, bd=0)
        for i in range(9-etape):
            self.__etapes_traces__()[i](e)

    def __etapes_traces__(self):
        couleur = fontcolor
        larg = 6
        f0 = lambda e :self.create_line(e, 10*e, 8*e, 10*e, width=larg, fill=couleur, capstyle='round')
        f1 = lambda e :self.create_line(3*e, 10*e, 3*e, 2*e, width=larg, fill=couleur, capstyle='round')
        f2 = lambda e :self.create_line(3*e, 2*e, int(6.3*e), 2*e, width=larg, fill=couleur, capstyle='round')
        f3 = lambda e :self.create_line(3*e, 4*e, 5*e, 2*e, width=larg, fill=couleur, capstyle='round')
        f4 = lambda e :self.create_line(6*e, 2*e, 6*e, 4*e, width=larg, fill=couleur, capstyle='round')
        f5 = lambda e :self.create_oval(int(5.5*e), 4*e, int(6.5*e), 5*e, width=larg, outline=couleur)
        f6 = lambda e :self.create_line(6*e, 5*e, 6*e, int(6.5*e), width=larg, fill=couleur, capstyle='round')
        f7 = lambda e :self.create_line(5*e, int(5.5*e), 7*e, int(5.5*e), width=larg, fill=couleur, capstyle='round')
        f8 = lambda e :self.dernier_trace(e)
        return f0, f1, f2, f3, f4, f5, f6, f7, f8

    def dernier_trace(self, e):
        larg = 6
        couleur = fontcolor
        p = (police[0],police[1]*2,police[2])
        self.create_line(5*e,int(8.5*e), 6*e, \
                                        int(6.5*e),7*e,int(8.5*e), width=larg, fill=couleur, capstyle='round')
        self.create_text(int(4.5*e), 8*e, text="Vous avez\nperdu", fill=fontcolor2, font=p, justify='center')

    def update_canvas(self, partie: gp.Partie):
        etape= partie.get_erreurs()
        lst_construct = self.__etapes_traces__()
        self.delete("all")
        for f in lst_construct:
            f(self._e)


class Furoncle(tk.Button):
    """implémente les touches des lettres de l'alphabet pour le pendu"""
    def __init__(self, master, lettre):
        super().__init__(master)
        self.config(text=lettre, bg=bkgd, fg=fontcolor, font=police, borderwidth=0)
        self._valeur = lettre

    def command_bouton(self,partie: gp.Partie, cnv: Trace):
        self.config(state=tk.DISABLED)
        partie.propose_lettre(self._valeur)
        cnv.update_canvas(partie)



class Clavier(tk.Frame):
    """implémente un clavier et permet de récupérer la liste
    des boutons qui le composent"""
    def __init__(self, master):
        cles_touches = ["AZERTYUIOP","QSDFGHJKLM","WXCVBN"]
        super().__init__(master)
        self.config(bg=bkgd)
        self._subframes=list()
        self._touches = list()
        for ligne in range(len(cles_touches)):
            f=tk.Frame(self)
            self._subframes.append(f)
            for car in cles_touches[ligne]:
                touche = Furoncle(f,car)
                touche.grid(column = cles_touches[ligne].find(car), row = 0)
                self._touches.append(touche)
            f.grid(column=0, row=ligne)

    def get_buttons(self):
        """renvoie la liste des boutons du clavier"""
        return self._touches


class MenuPendu(tk.Menu):
    """pour créer un menu qui permettra de choisir des mots au hasard
    ou en les saisissant à condition qu'ils soient dans le dico (forçage possible)"""
    def __init__(self,fenetre):
        super().__init__(fenetre)
        self.__mot_mystere = None # stockera le mot mystère
        self.menu_partie = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Partie", menu= self.menu_partie)
        self.menu_partie.add_command(label="Choisir nom", command=self.choix_user)
        self.menu_partie.add_command(label="Nom aléatoire", command= self.choix_alea)
        self.menu_partie.add_separator()
        self.menu_partie.add_command(label="Quitter", command=quit)
        fenetre.config(menu=self)

    def choix_alea(self):
        """choisit un mot aléatoirement dans les noms commun du dico csv.
        puis désactive les deux menus de choix"""
        self.menu_partie.entryconfigure(0, state=tk.DISABLED)
        self.menu_partie.entryconfigure(1, state=tk.DISABLED)
        self.__mot_mystere = cn.choisir_mot()
        print(self.__mot_mystere)

    def get_mot_mystere(self):
        return self.__mot_mystere

    def choix_user(self):
        """ouvre une boite de dialogue pour proposer un mot et le vérifie
        puis déactive les deux menus de choix"""
        while True:
            mot = tkinter.simpledialog.askstring(title="entre un nom", prompt="", initialvalue= "votre proposition", show="#")
            if not cn.verif_mot(mot):
                if tk.messagebox.askyesno(title="ATTENTION",message="mot absent du dico\nle conserver?"):
                    self.__mot_mystere = mot
                    break
            else:
                self.__mot_mystere = mot
                break
        self.menu_partie.entryconfigure(0, state=tk.DISABLED)
        self.menu_partie.entryconfigure(1, state=tk.DISABLED)

    def enable_menus(self):
        """permet en fin de partie de réactiver les menu"""
        self.menu_partie.entryconfigure(0, state=tk.ACTIVE)
        self.menu_partie.entryconfigure(1, state=tk.ACTIVE)


class Entree(tk.Entry):
    def __init__(self, master):
        super().__init__(master)
        self.config(bg = bkgd, fg = fontcolor,font = police, selectborderwidth=5, state=tk.DISABLED)



class A_trouver(tk.Label):
    def __init__(self,master, txt=""):
        super().__init__(master)
        p=(police[0],police[1]+5,police[2])
        self.config(bg=bkgd, fg=fontcolor, font=p, borderwidth=0)
        self.config(text=txt)

    def update(self,partie:gp.Partie):
        self.config(text=partie.mot_affiche())

def main():
    fen = tk.Tk()
    # fen.geometry("400x300")
    fen.title("un pendu sinon rien")
    fen.tk.call('wm', 'iconphoto', fen._w, tk.PhotoImage(file='venv/include/iconeNSI.png'))
    #fen.iconbitmap("venv/iconeNSI.ico")
    fen.config(bg = bkgd)
    packounet = A_trouver(fen, "")
    packounet.grid(column=0, row=0)
    firstpack = Entree(fen)
    firstpack.grid(column=0, row=2)
    sous_pack = tk.Button(fen)
    sous_pack.config(text="A", command=lambda :sous_pack.config(state=tk.DISABLED))
    sous_pack.grid(column=0, row=4)
    fr = tk.Frame(fen)
    fr.grid(column=0, row=6)
    cnv = Trace(fen,0)
    cnv.grid(column=1, row=0, rowspan=7)
    print(cnv['height'])
    menu_b = MenuPendu(fen)
    fen.config(menu=menu_b)
    fen.mainloop()

if __name__ == "__main__":
    main()
