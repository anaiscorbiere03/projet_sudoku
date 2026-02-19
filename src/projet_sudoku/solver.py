
class Sudoku:
    @classmethod
    def from_grille(cls, grille):
        """
        Crée une instance de Sudoku à partir d'une grille existante (liste de listes).
        Args:
            grille (list): Grille de Sudoku sous forme de liste de listes d'entiers.
        Returns:
            Sudoku: Nouvelle instance initialisée avec la grille donnée.
        """
        return cls(grille)
    
    def __init__(self, nom_fichier=None):
        """
        Initialise une instance de Sudoku à partir d'un nom de fichier (str) ou d'une grille (list).
        Args:
            nom_fichier (str ou list): Chemin du fichier texte ou grille sous forme de liste de listes.
        Raises:
            ValueError: Si l'argument n'est ni une chaîne ni une liste.
        """
        self.grille = [[0]*9 for _ in range(9)]
        if isinstance(nom_fichier, str):
            self.charger(nom_fichier)
        elif isinstance(nom_fichier, list):
            # Copie profonde de la grille
            self.grille = [row[:] for row in nom_fichier]
        else:
            raise ValueError("Sudoku doit être initialisé avec un nom de fichier (str) ou une grille (list)")



    def charger(self, nom_fichier):
        """
        Charge la grille de Sudoku à partir d'un fichier texte.
        Args:
            nom_fichier (str): Chemin du fichier texte contenant la grille.
        """
        with open(nom_fichier, 'r') as f:
            for i, ligne in enumerate(f):
                valeurs = ligne.strip()
                for j, val in enumerate(valeurs):
                    self.grille[i][j] = int(val)

    def bloc(self, i, j):
        """
        Retourne le numéro du bloc 3x3 contenant la cellule (i, j).
        Args:
            i (int): Indice de ligne.
            j (int): Indice de colonne.
        Returns:
            int: Numéro du bloc (0 à 8).
        """
        return (i // 3) * 3 + (j // 3)

    def indices(self, b, r):
        """
        Retourne les indices (i, j) de la cellule de rang r dans le bloc b.
        Args:
            b (int): Numéro du bloc (0 à 8).
            r (int): Rang de la cellule dans le bloc (0 à 8).
        Returns:
            tuple: Indices (i, j) de la cellule.
        """
        return (3*(b//3) + r//3, 3*(b%3) + r%3)
    
    def coups_jouables(self, i, j):
        """
        Retourne la liste des valeurs possibles (coups jouables) pour la cellule (i, j).
        Args:
            i (int): Indice de ligne.
            j (int): Indice de colonne.
        Returns:
            list: Liste des entiers jouables (1 à 9) pour la cellule.
        """
        tab=[True]*10
        b=self.bloc(i,j)
        for k in range(9):
            if k!=j and self.grille[i][k]!=0:
                 tab[self.grille[i][k]]=False
            if k!=i and self.grille[k][j]!=0:
                 tab[self.grille[k][j]]=False
            x,y=self.indices(b,k)
            if (x,y)!= (i,j) and self.grille[x][y]!=0:
                tab[self.grille[x][y]]=False
        return [n for n in range(1,10) if tab[n]]
    
    def next_coup(self):
        """
        Cherche la prochaine case vide avec le moins de coups jouables (pour l'optimisation du backtracking).
        Returns:
            tuple: (case, liste) où case est un tuple (i, j) et liste la liste des valeurs possibles.
        """
        case=(-1,-1)
        liste=[i for i in range(9)]
        for i in range(9):
            for j in range(9):
                if self.grille[i][j]==0:
                    jouables=self.coups_jouables(i,j)
                    if case==(-1,-1) or len(jouables)<len(liste):
                        case=(i,j)
                        liste=jouables
        return case,liste


    def resoudre(self):
        """
        Résout la grille de Sudoku en utilisant une approche de backtracking récursif.
        Returns:
            bool: True si la grille est résolue, False sinon.
        """
        case, liste = self.next_coup()
        if case == (-1, -1):
            return True  # Grille résolue
        i, j = case
        for val in liste:
            self.grille[i][j] = val
            if self.resoudre():
                return True
            self.grille[i][j] = 0  # Backtrack
        return False  # Aucune solution trouvée
    
    def unique_solution(self):
        """
        Vérifie si la grille de Sudoku a une solution unique.
        Returns:
            bool: True si la grille a une unique solution, False sinon.
        """
        def compter_solutions():
            """
            Compte le nombre de solutions possibles pour la grille actuelle (utilisé en interne).
            Returns:
                int: Nombre de solutions trouvées (s'arrête à 2).
            """
            case, liste = self.next_coup()
            if case == (-1, -1):
                return 1  # Une solution trouvée
            i, j = case
            total = 0
            for val in liste:
                self.grille[i][j] = val
                total += compter_solutions()
                self.grille[i][j] = 0  # Backtrack

                if total > 1:
                    return total  # On arrête dès qu'on a trouvé 2 solutions
            return total

        return compter_solutions() == 1



