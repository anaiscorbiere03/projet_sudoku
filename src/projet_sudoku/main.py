import copy
from projet_sudoku.generateur import GenerateurSudoku
from projet_sudoku.solver import Sudoku

def afficher_grille(grille):
    for i, ligne in enumerate(grille):
        if i % 3 == 0 and i != 0:
            print("-------+--------+-------")
        ligne_affiche = " ".join(str(x) if x != 0 else "." for x in ligne)
        blocs = [ligne_affiche[0:6], ligne_affiche[6:12], ligne_affiche[12:]]
        print(" | ".join(blocs))
    print()

def main() -> None:
    # Générer une grille
    generateur = GenerateurSudoku()
    grille = generateur.generer(nb_cases_a_retirer=40)
    print("Grille générée :\n")
    afficher_grille(grille)

    # Résoudre la grille
    # On crée une copie profonde pour ne pas modifier la grille générée
    grille_a_resoudre = copy.deepcopy(grille)
    sudoku = Sudoku(grille_a_resoudre)
    if sudoku.resoudre():
        print("Solution :\n")
        afficher_grille(sudoku.grille)
    else:
        print("Aucune solution trouvée.")
