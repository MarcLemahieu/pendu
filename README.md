![logo NSI](venv/include/iconeNSI.png)

# pendu
version fenetrée du jeu de pendu en python

## detail des fichiers et de leur rôle:

- **main** contient la classe FenetrePendu qui gère le déroulé d'une partie et l'interaction entre les objets qui la constitue
- **tools** implémente les classes
  - **Trace(_Canvas_)** qui trace le pendu au fil de la partie
  - **Furoncle(_Button_)** qui gère les boutons du clavier
  - **Clavier(_Frame_)** qui organise les Furoncles dans un Frame
  - **MenuPendu(_Menu_)** qui organise le menu pour lancer une partie ou quitter
  - **Entree(_Entry_)** qui surclasse le champde saisie pour l'entrée d'un mot complet(lettre seule possible)
  - **A_trouver(_Label_)** qui affiche les lettres découvertes du mot
- **gestion_partie** qui contient la classe Partie qui s'occupe de l'état du jeu et qui sera la classe à laisser développer par les élèves
- **choix_nom** qui contient deux fonctions essentielles au jeu:
  - **_choisir_mot_** qui prend un nom commun dans le dictionnaire de la langue française (issu du CNAM au format csv)
  - **_verif_mot_** qui s'assure qu'un nom appartient à ce dictionnaire

## reste à faire

**TODO** on pourra proposer une modification de *choix_nom* en utilisant la library **csv** plutôt que **pandas** qui alourdit inutilement (modification proposable aux élèves) 

## Idées d'améliorations possibles:

- On pourra rajouter un popup lorsque le mot est trouver pour renvoyer la définition du mot sur un dictionnaire en ligne (je pense à [https://www.cnrtl.fr](https://www.cnrtl.fr))  
  la bibliothèque [webbrowser](https://docs.python.org/3/library/webbrowser.html) pourra à ce titre être utile.
  
- De même dans la barre de menu on peut ajouter un menu pour choisir la police. L'appli va chercher les polices existantes sur l'OS et permet d'en sélectionner une.
