import random
from projet_sudoku.solver import Sudoku

class GenerateurSudoku:
    def __init__(self):
        self.grille = [[0 for _ in range(9)] for _ in range(9)]

    def remplir_grille(self):
        """Remplit complètement la grille avec une solution valide."""
        def remplir_case(i, j):
            if i == 9:
                return True
            ni, nj = (i, j+1) if j < 8 else (i+1, 0)
            nums = list(range(1, 10))
            random.shuffle(nums)
            for num in nums:
                if self.est_valide(i, j, num):
                    self.grille[i][j] = num
                    if remplir_case(ni, nj):
                        return True
                    self.grille[i][j] = 0
            return False
        remplir_case(0, 0)

    def est_valide(self, i, j, val):
        for k in range(9):
            if self.grille[i][k] == val or self.grille[k][j] == val:
                return False
        bi, bj = 3 * (i // 3), 3 * (j // 3)
        for x in range(bi, bi+3):
            for y in range(bj, bj+3):
                if self.grille[x][y] == val:
                    return False
        return True

    def retirer_cases(self, nb_cases):
        """Retire nb_cases de la grille tout en gardant une unique solution."""
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)
        count = 0
        for i, j in positions:
            if count >= nb_cases:
                break
            sauvegarde = self.grille[i][j]
            self.grille[i][j] = 0
            sudoku = Sudoku.from_grille(self.grille)
            if not sudoku.unique_solution():
                self.grille[i][j] = sauvegarde
            else:
                count += 1

    def generer(self, nb_cases_a_retirer=40):
        self.remplir_grille()
        self.retirer_cases(nb_cases_a_retirer)
        return self.grille

    def sauvegarder(self, chemin):
        with open(chemin, 'w') as f:
            for ligne in self.grille:
                f.write(''.join(str(x) for x in ligne) + '\n')

