
# Importation du module random pour le mélange et la sélection aléatoire
import random
from projet_sudoku.solver import Sudoku  # Import du solveur pour vérifier l'unicité de la solution


# Classe permettant de générer des grilles de Sudoku valides et uniques
class GenerateurSudoku:
    """
    Classe permettant de générer des grilles de Sudoku valides et uniques.
    """
    def __init__(self):
        """
        Initialise une nouvelle instance avec une grille vide (9x9 remplie de zéros).
        """
        self.grille = [[0 for _ in range(9)] for _ in range(9)]

    def remplir_grille(self):
        """
        Remplit complètement la grille avec une solution valide.
        Utilise une approche récursive et aléatoire pour garantir la diversité des grilles.
        """
        def remplir_case(i, j):
            # Si on a atteint la fin de la grille, c'est terminé
            if i == 9:
                return True
            # Passage à la case suivante
            ni, nj = (i, j+1) if j < 8 else (i+1, 0)
            nums = list(range(1, 10))
            random.shuffle(nums)  # Mélange les chiffres
            for num in nums:
                if self.est_valide(i, j, num):
                    self.grille[i][j] = num
                    if remplir_case(ni, nj):
                        return True
                    self.grille[i][j] = 0  # Backtracking
            return False
        remplir_case(0, 0)

    def est_valide(self, i, j, val):
        """
        Vérifie si l'insertion de 'val' en position (i, j) respecte les règles du Sudoku.
        Args:
            i (int): Indice de ligne.
            j (int): Indice de colonne.
            val (int): Valeur à tester.
        Returns:
            bool: True si la valeur peut être placée, False sinon.
        """
        # Vérification de la ligne et de la colonne
        for k in range(9):
            if self.grille[i][k] == val or self.grille[k][j] == val:
                return False
        # Vérification du bloc 3x3
        bi, bj = 3 * (i // 3), 3 * (j // 3)
        for x in range(bi, bi+3):
            for y in range(bj, bj+3):
                if self.grille[x][y] == val:
                    return False
        return True

    def retirer_cases(self, nb_cases):
        """
        Retire nb_cases de la grille tout en gardant une unique solution.
        Pour chaque case retirée, on vérifie que la grille reste à solution unique.
        Args:
            nb_cases (int): Nombre de cases à retirer.
        """
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)  # Mélange les positions pour retirer au hasard
        count = 0
        for i, j in positions:
            if count >= nb_cases:
                break
            sauvegarde = self.grille[i][j]  # Sauvegarde la valeur avant suppression
            self.grille[i][j] = 0
            sudoku = Sudoku.from_grille(self.grille)
            # Vérifie que la grille a toujours une solution unique
            if not sudoku.unique_solution():
                self.grille[i][j] = sauvegarde  # Restaure si ce n'est pas le cas
            else:
                count += 1

    def generer(self, nb_cases_a_retirer=40):
        """
        Génère une nouvelle grille de Sudoku avec un nombre donné de cases retirées.
        Args:
            nb_cases_a_retirer (int): Nombre de cases à retirer pour créer la grille à résoudre.
        Returns:
            list[list[int]]: Grille de Sudoku générée.
        """
        self.remplir_grille()
        self.retirer_cases(nb_cases_a_retirer)
        return self.grille

    def sauvegarder(self, chemin):
        """
        Sauvegarde la grille actuelle dans un fichier texte.
        Chaque ligne du fichier correspond à une ligne de la grille.
        Args:
            chemin (str): Chemin du fichier où sauvegarder la grille.
        """
        with open(chemin, 'w') as f:
            for ligne in self.grille:
                f.write(''.join(str(x) for x in ligne) + '\n')

