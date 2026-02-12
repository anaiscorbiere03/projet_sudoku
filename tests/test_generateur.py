
from projet_sudoku.generateur import GenerateurSudoku

def test_remplir_grille():
    g = GenerateurSudoku()
    g.remplir_grille()
    # Vérifie que la grille est remplie sans 0
    assert all(all(1 <= val <= 9 for val in row) for row in g.grille)


def test_est_valide():
    g = GenerateurSudoku()
    g.remplir_grille()
    # Teste qu'une valeur déjà présente n'est pas valide
    val = g.grille[0][0]
    assert not g.est_valide(0, 1, val)


def test_retirer_cases():
    g = GenerateurSudoku()
    g.remplir_grille()
    g.retirer_cases(10)
    nb_zeros = sum(cell == 0 for row in g.grille for cell in row)
    assert nb_zeros == 10
