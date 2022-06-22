import pygame, sys
from level import Level
from settings import screen_width, screen_height, background_color

# pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
level = Level(screen)
pygame.display.set_caption("Chess")
global choose_piece
choose_piece = False

while True:
    event = pygame.event.poll()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()
            if choose_piece:
                level.move_piece(mouse_pos)
                choose_piece = False
            else:
                choose_piece = level.choose_piece(mouse_pos)

                
            
            
    screen.fill(background_color)
    
    level.run()

    pygame.display.update()
    clock.tick(60)

# if u take piece, don't move and press on other piece it will not take this new piece it will just remove last piece from self.chosen_piece, fix this
# fix top, left, right , bottom moves, diagonally works right i think - after checking i think this is problem with check_moves method - FIXED
# fix choose_pice method, top,right,bottom,left not working well, for now i didn't see any bugs with diagonal movement - FIXED
# When black piece is highlighted, highlight it with light red color, make a barier, ex. queen can't beat rock if it stands after the pawn - DONE
#  So next thing to do is to make king real, so he cant move when there is check etc. I think it would be ok to check possible moves of black pieces but not blit them on screen,
#  thanks to this highlight_pos of king must be diffrent from black_poss_moves 
