import pygame
from level_data import chess_board

screen_width, screen_height = 1920, 1200
board_size = 800

tile_size = board_size/len(chess_board)

highlight_color = pygame.color.Color(140, 174, 197)
background_color = pygame.color.Color(99, 83, 116)
brown_color = pygame.color.Color(160,82,45)
kill_color = pygame.color.Color(209, 91, 68)