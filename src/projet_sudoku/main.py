import os
from projet_sudoku.solver import Sudoku

def main() -> None:
    chemin = os.path.join(os.path.dirname(__file__), "exemple.txt")
    sudoku = Sudoku(chemin)
    if sudoku.resoudre():
        print("Grille résolue :\n")
        for i, ligne in enumerate(sudoku.grille):
            if i % 3 == 0 and i != 0:
                print("-------+--------+-------")
            ligne_affiche = " ".join(str(x) if x != 0 else "." for x in ligne)
            blocs = [ligne_affiche[0:6], ligne_affiche[6:12], ligne_affiche[12:]]
            print(" | ".join(blocs))
        print()
    else:
        print("Aucune solution trouvée.")
