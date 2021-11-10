# pendu
version fenetrée du jeu de pendu en python

### detail des fichiers et de leur rôle:

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
