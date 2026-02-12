import pytest
from projet_sudoku.solver import Sudoku
from projet_sudoku.generateur import GenerateurSudoku


def test_sudoku_chargement_exemple():
    s = Sudoku('src/projet_sudoku/exemple.txt')
    assert s.grille[0][8] == 2
    assert s.grille[1][8] == 3
    assert s.grille[8][0] == 4


def test_sudoku_resoudre():
    s = Sudoku('src/projet_sudoku/exemple.txt')
    solved = s.resoudre()
    assert solved is True
    assert all(all(1 <= val <= 9 for val in row) for row in s.grille)


def test_sudoku_unique_solution():
    s = Sudoku('src/projet_sudoku/exemple.txt')
    assert s.unique_solution() is True


def test_generateur_sudoku():
    g = GenerateurSudoku()
    grille = g.generer(nb_cases_a_retirer=20)
    assert sum(cell == 0 for row in grille for cell in row) == 20
    s = Sudoku(grille)
    assert s.unique_solution() is True


def test_coups_jouables():
    s = Sudoku('src/projet_sudoku/exemple.txt')
    coups = s.coups_jouables(0, 0)
    assert isinstance(coups, list)
    assert all(1 <= n <= 9 for n in coups)
