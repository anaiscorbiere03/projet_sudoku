import sys
import copy
import argparse
from projet_sudoku.generateur import GenerateurSudoku
from projet_sudoku.solver import Sudoku
from projet_sudoku.affichage import afficher_sudoku_pygame

def afficher_grille(grille):
    for i, ligne in enumerate(grille):
        if i % 3 == 0 and i != 0:
            print("-------+--------+-------")
        ligne_affiche = " ".join(str(x) if x != 0 else "." for x in ligne)
        blocs = [ligne_affiche[0:6], ligne_affiche[6:12], ligne_affiche[12:]]
        print(" | ".join(blocs))
    print()

def main():
    parser = argparse.ArgumentParser(description="Sudoku - Générateur et jeu graphique")
    parser.add_argument('--jeu', action='store_true', help='Lancer le jeu graphique')
    # Ajoutez ici d'autres arguments à l'avenir
    args = parser.parse_args()

    generateur = GenerateurSudoku()
    grille = generateur.generer(nb_cases_a_retirer=40)
    if args.jeu:
        afficher_sudoku_pygame(grille)
    else:
        print("Grille générée :\n")
        afficher_grille(grille)
        grille_a_resoudre = copy.deepcopy(grille)
        sudoku = Sudoku(grille_a_resoudre)
        if sudoku.resoudre():
            print("Solution :\n")
            afficher_grille(sudoku.grille)
        else:
            print("Aucune solution trouvée.")
