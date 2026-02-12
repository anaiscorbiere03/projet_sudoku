from projet_sudoku.solver import Sudoku

def test_bloc():
    s = Sudoku('src/projet_sudoku/exemple.txt')
    assert s.bloc(0, 0) == 0
    assert s.bloc(4, 4) == 4
    assert s.bloc(8, 8) == 8

def test_indices():
    s = Sudoku('src/projet_sudoku/exemple.txt')
    assert s.indices(0, 0) == (0, 0)
    assert s.indices(4, 5) == (4, 5)


def test_next_coup():
    s = Sudoku('src/projet_sudoku/exemple.txt')
    case, liste = s.next_coup()
    assert isinstance(case, tuple)
    assert isinstance(liste, list)
