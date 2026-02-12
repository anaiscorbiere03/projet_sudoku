
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
    parser = argparse.ArgumentParser(
        description="Sudoku - Générateur et jeu graphique",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--jeu', action='store_true', help='Lancer le jeu graphique')
    parser.add_argument('-v', action='count', default=0, help='Activer le mode verbose (niveau 1, -vv pour niveau 2, etc)')
    args = parser.parse_args()

    import logging
    # Map -v levels to logging levels
    if args.v >= 3:
        log_level = logging.DEBUG
    elif args.v == 2:
        log_level = logging.INFO
    elif args.v == 1:
        log_level = logging.WARNING
    else:
        log_level = logging.ERROR
    logging.basicConfig(level=log_level, format='[%(levelname)s] %(message)s')

    logging.info("Démarrage du générateur de Sudoku")
    generateur = GenerateurSudoku()
    grille = generateur.generer(nb_cases_a_retirer=40)
    logging.debug("Grille générée")
    if args.jeu:
        logging.info("Lancement du jeu graphique")
        afficher_sudoku_pygame(grille)
    else:
        print("Grille générée :\n")
        afficher_grille(grille)
        grille_a_resoudre = copy.deepcopy(grille)
        sudoku = Sudoku(grille_a_resoudre)
        logging.debug("Résolution de la grille")
        if sudoku.resoudre():
            print("Solution :\n")
            afficher_grille(sudoku.grille)
            logging.info("Grille résolue avec succès")
        else:
            print("Aucune solution trouvée.")
            logging.warning("Échec de la résolution de la grille")
