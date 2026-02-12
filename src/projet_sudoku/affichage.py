
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_BACKSPACE, K_DELETE
from projet_sudoku.solver import Sudoku
from typing import List, Optional

TAILLE = 540
MARGE_X = 20
CASE = (TAILLE - 2*MARGE_X) // 9
FONT_SIZE = 40
COULEUR_BG = (255, 255, 255)
COULEUR_LIGNE = (0, 0, 0)
COULEUR_LIGNE_BLOC = (20, 20, 20)
COULEUR_FIXE = (255, 230, 240)
COULEUR_MODIFIABLE = (255, 255, 255)
COULEUR_TEXTE = (0, 0, 0)
COULEUR_VALID = (0, 200, 0)
COULEUR_ERREUR = (200, 0, 0)
COULEUR_SELECTION = (180, 210, 255,60)

def afficher_sudoku_pygame(grille: List[List[int]]) -> None:
    pygame.init()
    screen = pygame.display.set_mode((TAILLE, TAILLE + 120))
    pygame.display.set_caption("Sudoku")
    font = pygame.font.SysFont(None, FONT_SIZE)
    timer_font = pygame.font.SysFont(None, 28)

    # Cases modifiables (0) ou fixes (non 0)
    modifiables = [[cell == 0 for cell in row] for row in grille]
    user_grille = [row[:] for row in grille]
    selected = None
    finished = False
    start_ticks = pygame.time.get_ticks()
    # Calculer la solution complète au lancement
    sudoku_solver = Sudoku([row[:] for row in grille])
    sudoku_solver.resoudre()
    solution = sudoku_solver.grille
    nb_indices = 0
    indices_matrix = [[False for _ in range(9)] for _ in range(9)]

    def draw_grid(final_time: Optional[str] = None, erreurs: Optional[List[List[bool]]] = None) -> None:
        screen.fill(COULEUR_BG)
        # Timer
        if final_time is None:
            elapsed = (pygame.time.get_ticks() - start_ticks) // 1000
            minutes = elapsed // 60
            seconds = elapsed % 60
            timer_text = timer_font.render(f"Temps : {minutes:02d}:{seconds:02d}", True, (50, 50, 50))
            screen.blit(timer_text, (TAILLE//2 - 60, 10))
        # Décaler la grille vers le bas pour le timer
        offset_y = 40
        offset_x = MARGE_X
        COULEUR_INDICE = (30, 60, 180)
        for i in range(9):
            for j in range(9):
                rect = pygame.Rect(offset_x + j*CASE, offset_y + i*CASE, CASE, CASE)
                color = COULEUR_FIXE if not modifiables[i][j] else COULEUR_MODIFIABLE
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (180,180,180), rect, 1)  # fine border for each cell
                if user_grille[i][j] != 0:
                    # Si erreurs, afficher en rouge les chiffres incorrects
                    if erreurs and erreurs[i][j]:
                        txt = font.render(str(user_grille[i][j]), True, COULEUR_ERREUR)
                    elif indices_matrix[i][j]:
                        txt = font.render(str(user_grille[i][j]), True, COULEUR_INDICE)
                    else:
                        txt = font.render(str(user_grille[i][j]), True, COULEUR_TEXTE)
                    screen.blit(txt, (offset_x + j*CASE+CASE//3, offset_y + i*CASE+CASE//6))
        # Colorier la ligne et la colonne sélectionnées APRÈS le dessin des cases
        if selected:
            sel_i, sel_j = selected
            # Surface temporaire avec alpha, taille de la grille uniquement
            highlight = pygame.Surface((9*CASE, 9*CASE), pygame.SRCALPHA)
            # Ligne
            for j in range(9):
                rect = pygame.Rect(j*CASE, sel_i*CASE, CASE, CASE)
                pygame.draw.rect(highlight, COULEUR_SELECTION, rect)
            # Colonne
            for i in range(9):
                if i != sel_i:
                    rect = pygame.Rect(sel_j*CASE, i*CASE, CASE, CASE)
                    pygame.draw.rect(highlight, COULEUR_SELECTION, rect)
            screen.blit(highlight, (offset_x, offset_y))
            # Bordure de la case sélectionnée
            pygame.draw.rect(screen, (100, 100, 255), (offset_x + sel_j*CASE, offset_y + sel_i*CASE, CASE, CASE), 3)
        if finished:
            pygame.draw.rect(screen, COULEUR_VALID, (offset_x, offset_y, 9*CASE, 9*CASE), 8)

        # DESSIN DES LIGNES (fines puis épaisses) JUSTE AVANT L'AFFICHAGE
        # D'abord toutes les lignes fines
        for i in range(10):
            pygame.draw.line(screen, COULEUR_LIGNE, (offset_x, offset_y + i*CASE), (offset_x + 9*CASE, offset_y + i*CASE), 2)
            pygame.draw.line(screen, COULEUR_LIGNE, (offset_x + i*CASE, offset_y), (offset_x + i*CASE, offset_y + 9*CASE), 2)

        # Puis toutes les lignes épaisses pour les blocs 3x3
        for i in [0, 3, 6, 9]:
            pygame.draw.line(screen, COULEUR_LIGNE_BLOC, (offset_x, offset_y + i*CASE), (offset_x + 9*CASE, offset_y + i*CASE), 6)
            pygame.draw.line(screen, COULEUR_LIGNE_BLOC, (offset_x + i*CASE, offset_y), (offset_x + i*CASE, offset_y + 9*CASE), 6)

        # Bouton Valider centré et grisé si la grille n'est pas remplie
        bouton_width, bouton_height = 180, 50
        bouton_x = (TAILLE - bouton_width) // 2
        bouton_y = offset_y + 9*CASE + 25
        bouton_rect = pygame.Rect(bouton_x, bouton_y, bouton_width, bouton_height)
        # Grisé si la grille n'est pas remplie
        grille_remplie = all(all(cell != 0 for cell in row) for row in user_grille)
        couleur_bouton = (0, 120, 200) if grille_remplie else (180, 180, 180)
        pygame.draw.rect(screen, couleur_bouton, bouton_rect, border_radius=10)
        bouton_text = font.render("Valider", True, (255,255,255) if grille_remplie else (100,100,100))
        text_rect = bouton_text.get_rect(center=bouton_rect.center)
        screen.blit(bouton_text, text_rect)
            # Affichage du texte d'indice sous le bouton
        indice_font = pygame.font.SysFont(None, 28)
        indice_text = indice_font.render('Indice : appuyer sur "h" pour dévoiler une case', True, (50, 50, 50))
        indice_rect = indice_text.get_rect(center=(TAILLE//2, bouton_y + bouton_height + 25))
        screen.blit(indice_text, indice_rect)

        # Si le sudoku est fini et correct, afficher le temps final au centre et le nombre d'indices
        if final_time is not None:
            big_font = pygame.font.SysFont(None, 44)
            small_font = pygame.font.SysFont(None, 28)
            center_x = offset_x + (9*CASE)//2
            center_y = offset_y + (9*CASE)//2
            bravo_text = big_font.render("Bravo !", True, (0, 100, 0))
            chrono_text = big_font.render(f"Temps : {final_time}", True, (0, 100, 0))
            indices_text = small_font.render(f"Indices utilisés : {nb_indices}", True, (0, 100, 0))
            screen.blit(bravo_text, bravo_text.get_rect(center=(center_x, center_y - 35)))
            screen.blit(chrono_text, chrono_text.get_rect(center=(center_x, center_y)))
            screen.blit(indices_text, indices_text.get_rect(center=(center_x, center_y + 35)))

        pygame.display.flip()

    def check_valid() -> bool:
        for i in range(9):
            for j in range(9):
                if user_grille[i][j] != solution[i][j]:
                    return False
        return True

    running = True
    final_time_str = None
    erreurs = None
    while running:
        draw_grid(final_time=final_time_str, erreurs=erreurs)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                offset_y = 40
                # Clic sur la grille
                if not finished and offset_y <= y < offset_y + 9*CASE and MARGE_X <= x < MARGE_X + 9*CASE:
                    i, j = (y - offset_y) // CASE, (x - MARGE_X) // CASE
                    if 0 <= i < 9 and 0 <= j < 9 and modifiables[i][j]:
                        selected = (i, j)
                # Clic sur le bouton Valider
                bouton_width, bouton_height = 180, 50
                bouton_x = (TAILLE - bouton_width) // 2
                bouton_y = offset_y + 9*CASE + 25
                bouton_rect = pygame.Rect(bouton_x, bouton_y, bouton_width, bouton_height)
                grille_remplie = all(all(cell != 0 for cell in row) for row in user_grille)
                if bouton_rect.collidepoint(x, y) and not finished and grille_remplie:
                    # Vérifier la grille
                    if check_valid():
                        finished = True
                        elapsed = (pygame.time.get_ticks() - start_ticks) // 1000
                        minutes = elapsed // 60
                        seconds = elapsed % 60
                        final_time_str = f"{minutes:02d}:{seconds:02d}"
                        erreurs = None
                    else:
                        # Marquer les erreurs
                        erreurs = [[user_grille[i][j] != 0 and user_grille[i][j] != solution[i][j] for j in range(9)] for i in range(9)]
            elif event.type == KEYDOWN and selected and not finished:
                if event.key in [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9]:
                    val = event.key - K_0
                    i, j = selected
                    user_grille[i][j] = val
                elif event.key in [K_BACKSPACE, K_DELETE, K_0]:
                    i, j = selected
                    user_grille[i][j] = 0
                # Fonctionnalité indice : touche 'h'
                elif event.key == pygame.K_h:
                    i, j = selected
                    if modifiables[i][j]:
                        user_grille[i][j] = solution[i][j]
                        if not indices_matrix[i][j]:
                            indices_matrix[i][j] = True
                            nb_indices += 1
        if finished:
            draw_grid(final_time=final_time_str)
            pygame.time.wait(2500)
            running = False
    pygame.quit()
