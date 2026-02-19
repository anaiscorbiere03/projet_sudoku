

# Importation des modules nécessaires
import copy
import argparse
from projet_sudoku.generateur import GenerateurSudoku  # Générateur de grilles de Sudoku
from projet_sudoku.solver import Sudoku  # Solveur de Sudoku
from projet_sudoku.affichage import afficher_sudoku_pygame  # Affichage graphique avec pygame


# Fonction utilitaire pour afficher une grille de Sudoku dans la console
def afficher_grille(grille):
    """
    Affiche une grille de Sudoku dans la console de façon lisible.
    Les zéros sont remplacés par des points et la grille est découpée en blocs 3x3.
    Args:
        grille (list[list[int]]): Grille de Sudoku à afficher.
    """
    for i, ligne in enumerate(grille):
        # Affiche une ligne de séparation tous les 3 blocs
        if i % 3 == 0 and i != 0:
            print("-------+--------+-------")
        # Remplace les zéros par des points pour les cases vides
        ligne_affiche = " ".join(str(x) if x != 0 else "." for x in ligne)
        # Découpe la ligne en 3 blocs pour l'affichage
        blocs = [ligne_affiche[0:6], ligne_affiche[6:12], ligne_affiche[12:]]
        print(" | ".join(blocs))
    print()


# Fonction principale du programme
def main():
    """
    Point d'entrée principal du programme.
    Gère les arguments de la ligne de commande pour lancer soit le jeu graphique, soit l'affichage console.
    Génère une grille de Sudoku, l'affiche et propose la résolution automatique si demandé.
    """
    # Création du parser d'arguments pour la ligne de commande
    parser = argparse.ArgumentParser(
        description="Sudoku - Générateur et jeu graphique",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--jeu', action='store_true', help='Lancer le jeu graphique')  # Option pour lancer le mode graphique
    parser.add_argument('-v', action='count', default=0, help='Activer le mode verbose (niveau 1, -vv pour niveau 2, etc)')  # Option pour le niveau de verbosité
    args = parser.parse_args()

    import logging
    # Association du niveau de verbosité à un niveau de logging
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
    generateur = GenerateurSudoku()  # Création d'une instance du générateur
    grille = generateur.generer(nb_cases_a_retirer=40)  # Génération d'une grille avec 40 cases retirées
    logging.debug("Grille générée")
    if args.jeu:
        logging.info("Lancement du jeu graphique")
        afficher_sudoku_pygame(grille)  # Affichage de la grille dans une fenêtre graphique
    else:
        print("Grille générée :\n")
        afficher_grille(grille)  # Affichage de la grille dans la console
        grille_a_resoudre = copy.deepcopy(grille)  # Copie de la grille pour la résolution
        sudoku = Sudoku(grille_a_resoudre)  # Création d'une instance du solveur
        logging.debug("Résolution de la grille")
        if sudoku.resoudre():
            print("Solution :\n")
            afficher_grille(sudoku.grille)  # Affichage de la solution
            logging.info("Grille résolue avec succès")
        else:
            print("Aucune solution trouvée.")
            logging.warning("Échec de la résolution de la grille")
