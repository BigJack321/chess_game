import pygame
from settings import *
from sprites import Piece, Highlight
from level_data import *
from player import Player


class Level(pygame.sprite.Sprite):
    def __init__(self,display_surface):
        super().__init__()
        self.display_surface = display_surface
        self.offset_y = int(((self.display_surface.get_size()[1] - board_size)/2))
        self.offset_x = int(((self.display_surface.get_size()[0] - board_size)/2))
        self.topleft_board_tile_pos = (self.offset_x,self.offset_y)
        self.bottomleft_board_tile_pos = (self.offset_x,int(tile_size*len(chess_board) + self.offset_y - tile_size))
        self.topright_board_tile_pos = (int(tile_size * len(chess_board[0]) + self.offset_x - tile_size), self.offset_y)
        self.bottomright_board_tile_pos = (int(tile_size * len(chess_board[0]) + self.offset_x - tile_size),int(tile_size*len(chess_board) + self.offset_y - tile_size))



        # player
        self.player = Player()
        self.player_group = pygame.sprite.GroupSingle()
        self.player_group.add(self.player)

        # pawns 
        self.b_pawns_group = self.create_piece('p', b_pawns)
        self.w_pawns_group = self.create_piece('P', w_pawns)

        # rocks 
        self.b_rocks_group = self.create_piece('r', b_rocks)
        self.w_rocks_group = self.create_piece('R', w_rocks)

        # knights - s
        self.b_knights_group = self.create_piece('s', b_knights)
        self.w_knights_group = self.create_piece('S', w_knights)

        # bishops
        self.b_bishops_group = self.create_piece('b', b_bishops)
        self.w_bishops_group = self.create_piece('B', w_bishops)

        # queens
        self.b_queen_group = self.create_piece('q', b_queen)
        self.w_queen_group = self.create_piece('Q', w_queen)

        # kings
        self.b_king_group = self.create_piece('k', b_king)
        self.w_king_group = self.create_piece('K', w_king)
        

        # creating all_w_sprites_group
        all_w_sprites_list = [self.w_pawns_group,self.w_rocks_group,self.w_knights_group,self.w_bishops_group,self.w_queen_group,self.w_king_group]
        all_b_sprites_list = [self.b_pawns_group,self.b_rocks_group,self.b_knights_group,self.b_bishops_group,self.b_queen_group,self.b_king_group]
        all_sprites_list = [self.w_pawns_group,self.w_rocks_group,self.w_knights_group,self.w_bishops_group,self.w_queen_group,self.w_king_group,
                            self.b_pawns_group,self.b_rocks_group,self.b_knights_group,self.b_bishops_group,self.b_queen_group,self.b_king_group]
        self.all_w_sprites_group = pygame.sprite.Group()
        self.all_b_sprites_group = pygame.sprite.Group()
        self.all_pieces_sprites_group = pygame.sprite.Group()
        for sprite_group in all_w_sprites_list:
            self.all_w_sprites_group.add(sprite_group)
        for sprite_group in all_b_sprites_list:
            self.all_b_sprites_group.add(sprite_group)
        for sprite_group in all_sprites_list:
            self.all_pieces_sprites_group.add(sprite_group)

        self.collided_sprite = []

        # Highlight
        self.highlight_sprite_group = pygame.sprite.Group()

        # creating dictionary with pos of tile ex. 'a2':(560,800)
        self.a8_h1_list =            ['a8','b8','c8','d8','e8','f8','g8','h8',
                                      'a7','b7','c7','d7','e7','f7','g7','h7',
                                      'a6','b6','c6','d6','e6','f6','g6','h6',
                                      'a5','b5','c5','d5','e5','f5','g5','h5',
                                      'a4','b4','c4','d4','e4','f4','g4','h4',
                                      'a3','b3','c3','d3','e3','f3','g3','h3',
                                      'a2','b2','c2','d2','e2','f2','g2','h2',
                                      'a1','b1','c1','d1','e1','f1','g1','h1',]
        self.tiles_pos_dictionary = self.create_tile_pos_dictionary()

    # basic display

    def create_tile_pos_dictionary(self):
        pos_list = []
        for row_index, row in enumerate(chess_board):
            for col_index, col in enumerate(row):
                y = tile_size * row_index + self.offset_y
                x = tile_size * col_index + self.offset_x
                pos = (x,y)
                pos_list.append(pos)
        return dict(zip(self.a8_h1_list,pos_list))


    def create_chess_board(self,board):
        for row_index, row in enumerate(board):
            for col_index, col in enumerate(row):
                y = tile_size * row_index + self.offset_y
                x = tile_size * col_index + self.offset_x
                if col == 'X':
                    surface = pygame.Surface((tile_size,tile_size))
                    surface.fill('white')
                    self.display_surface.blit(surface,(x,y))
                    
                if col == ' ':
                    surface = pygame.Surface((tile_size,tile_size))
                    surface.fill(brown_color)
                    self.display_surface.blit(surface,(x,y))
    
    def create_chess_board_wrap(self,board_wrap):
        for row_index, row in enumerate(board_wrap):
            for col_index, col in enumerate(row):
                y = tile_size * row_index + self.offset_y - tile_size
                x = tile_size * col_index + self.offset_x - tile_size
                if col == '_':
                    surface = pygame.Surface((tile_size,tile_size))
                    surface.fill('grey')
                    self.display_surface.blit(surface,(x,y))
                if col == '|':
                    surface = pygame.Surface((tile_size,tile_size))
                    surface.fill('grey')
                    self.display_surface.blit(surface,(x,y))
                       

    def create_piece(self,type, layout):
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                
                if value != ' ':

                    y = tile_size * row_index + self.offset_y
                    x = tile_size * col_index + self.offset_x

                    # whites
                    if type == 'P': sprite = Piece(tile_size, x, y, '../graphics/pieces/white/w_pawn.png')
                    if type == 'R': sprite = Piece(tile_size, x, y, '../graphics/pieces/white/w_rock.png')
                    if type == 'S': sprite = Piece(tile_size, x, y, '../graphics/pieces/white/w_knight.png')
                    if type == 'B': sprite = Piece(tile_size, x, y, '../graphics/pieces/white/w_bishop.png')
                    if type == 'Q': sprite = Piece(tile_size, x, y, '../graphics/pieces/white/w_queen.png')
                    if type == 'K': sprite = Piece(tile_size, x, y, '../graphics/pieces/white/w_king.png')
                    
                    # blacks
                    if type == 'p': sprite = Piece(tile_size, x, y, '../graphics/pieces/black/b_pawn.png')
                    if type == 'r': sprite = Piece(tile_size, x, y, '../graphics/pieces/black/b_rock.png')
                    if type == 's': sprite = Piece(tile_size, x, y, '../graphics/pieces/black/b_knight.png')
                    if type == 'b': sprite = Piece(tile_size, x, y, '../graphics/pieces/black/b_bishop.png')
                    if type == 'q': sprite = Piece(tile_size, x, y, '../graphics/pieces/black/b_queen.png')
                    if type == 'k': sprite = Piece(tile_size, x, y, '../graphics/pieces/black/b_king.png')

                    sprite_group.add(sprite)

        return sprite_group
        

    def choose_piece(self,mouse_pos):
        self.collided_sprite = [s for s in self.all_w_sprites_group if s.rect.collidepoint(mouse_pos[0],mouse_pos[1])]
        if bool(self.collided_sprite):
            #self.highlight_sprite_group.empty()
            """x = self.collided_sprite[0].rect.topleft[0]
            y = self.collided_sprite[0].rect.topleft[1]
            self.highlight(tile_size,tile_size*2,x,y-tile_size*2,highlight_color)"""
            pos_to_highlight = []
            possible_kill_pos = []
            pos_to_kill = []
            


            delete_after_pos_top = (0,0)
            delete_after_pos_right = (screen_width,screen_height)
            delete_before_pos_bottom = (screen_width,screen_height)
            delete_after_pos_left = (0,0)
            delete_after_pos_tl_diagonally = (0,0)
            delete_after_pos_tr_diagonally = (0,0)
            delete_after_pos_br_diagonally = (screen_width,screen_height)
            delete_after_pos_bl_diagonally = (0,screen_height)


            sprite_pos = self.collided_sprite[0].rect.topleft


            tiles_on_right = int((self.topright_board_tile_pos[0] - sprite_pos[0])/tile_size)
            tiles_on_left = int((sprite_pos[0] - self.topleft_board_tile_pos[0])/tile_size)
            tiles_on_top = int((sprite_pos[1] - self.topleft_board_tile_pos[1])/tile_size)
            tiles_on_bottom = int((self.bottomright_board_tile_pos[1] - sprite_pos[1])/tile_size)


            possible_moves = self.check_possible_moves(sprite_pos)
            
            if self.type == 'king':
                enemy_possible_checks = self.check_opposite_moves(self.all_b_sprites_group)

            if True:
                if self.type == 'rock' or self.type == 'queen':
                    # right
                    if possible_moves.count('right') == 1:
                        for sprite in self.all_pieces_sprites_group.sprites():
                            if sprite.rect.topleft[1] == sprite_pos[1]:
                                if (sprite.rect.topleft[0]<delete_after_pos_right[0]) and (sprite.rect.topleft[0] > sprite_pos[0]):
                                    delete_after_pos_right = sprite.rect.topleft
                        for pos in self.tiles_pos_dictionary.values():
                            if (pos[0] < delete_after_pos_right[0]) and (pos[1] == sprite_pos[1]) and (pos[0] > sprite_pos[0]):
                                pos_to_highlight.append(pos)
                        possible_kill_pos.append(delete_after_pos_right)
                    else:
                        for sprite in self.all_b_sprites_group.sprites():
                            if sprite.rect.topleft == (sprite_pos[0]+tile_size,sprite_pos[1]) and self.all_b_sprites_group.sprites().count(sprite) != self.b_king_group.sprites().count(sprite):
                                pos_to_kill.append(sprite.rect.topleft)
                    
                    # top
                    if possible_moves.count('top') == 1:
                        for sprite in self.all_pieces_sprites_group.sprites():
                            if sprite.rect.topleft[0] == sprite_pos[0]:
                                if sprite.rect.topleft[1]>delete_after_pos_top[1] and sprite.rect.topleft[1] < sprite_pos[1]:
                                    delete_after_pos_top = sprite.rect.topleft
                        for pos in self.tiles_pos_dictionary.values():
                            if (pos[1] > delete_after_pos_top[1]) and (pos[0] == sprite_pos[0]) and (sprite_pos[1] >  pos[1]):
                                pos_to_highlight.append(pos)
                        possible_kill_pos.append(delete_after_pos_top)
                    else:
                        for sprite in self.all_b_sprites_group.sprites():
                            if sprite.rect.topleft == (sprite_pos[0],sprite_pos[1]-tile_size) and self.all_b_sprites_group.sprites().count(sprite) != self.b_king_group.sprites().count(sprite):
                                pos_to_kill.append(sprite.rect.topleft)

                    # bottom
                    if possible_moves.count('bottom') == 1:
                        for sprite in self.all_pieces_sprites_group.sprites():
                            if sprite.rect.topleft[0] == sprite_pos[0]:
                                if (sprite.rect.topleft[1]<delete_before_pos_bottom[1]) and (sprite.rect.topleft[1] > sprite_pos[1]):
                                    delete_before_pos_bottom = sprite.rect.topleft
                        for pos in self.tiles_pos_dictionary.values():
                            if (pos[1] < delete_before_pos_bottom[1]) and (pos[0] == sprite_pos[0]) and (pos[1] > sprite_pos[1]):

                                pos_to_highlight.append(pos)
                        possible_kill_pos.append(delete_before_pos_bottom)
                    else:
                        for sprite in self.all_b_sprites_group.sprites():
                            if sprite.rect.topleft == (sprite_pos[0],sprite_pos[1]+tile_size) and self.all_b_sprites_group.sprites().count(sprite) != self.b_king_group.sprites().count(sprite):
                                pos_to_kill.append(sprite.rect.topleft)

                    # left 
                    if possible_moves.count('left') == 1:
                        for sprite in self.all_pieces_sprites_group.sprites():
                            if sprite.rect.topleft[1] == sprite_pos[1]:
                                if (sprite.rect.topleft[0]>delete_after_pos_left[0]) and (sprite.rect.topleft[0] < sprite_pos[0]):
                                    delete_after_pos_left = sprite.rect.topleft
                        for pos in self.tiles_pos_dictionary.values():
                            if (pos[0] > delete_after_pos_left[0]) and (pos[1] == sprite_pos[1]) and (pos[0] < sprite_pos[0]):
                                pos_to_highlight.append(pos)  
                        possible_kill_pos.append(delete_after_pos_left)
                    else:
                        for sprite in self.all_b_sprites_group.sprites():
                            if sprite.rect.topleft == (sprite_pos[0]-tile_size,sprite_pos[1]) and self.all_b_sprites_group.sprites().count(sprite) != self.b_king_group.sprites().count(sprite):
                                pos_to_kill.append(sprite.rect.topleft)

                if self.type == 'bishop' or self.type == 'queen':
                    # top_left_diagonally
                    if possible_moves.count('top_left_diagonally') == 1:
                        for sprite in self.all_pieces_sprites_group.sprites():
                            for i in range(1,tiles_on_left+1):
                                if (sprite.rect.topleft[0]+i*tile_size == sprite_pos[0] and sprite.rect.topleft[1]+i*tile_size == sprite_pos[1]) and (sprite.rect.topleft[0] > delete_after_pos_tl_diagonally[0] and sprite.rect.topleft[1]>delete_after_pos_tl_diagonally[1]):
                                    delete_after_pos_tl_diagonally = sprite.rect.topleft
                    
                        
                        for pos in self.tiles_pos_dictionary.values():
                            for i in range(1,tiles_on_left+1):
                                if (pos[1] > delete_after_pos_tl_diagonally[1]) and (pos[0] + i*tile_size == sprite_pos[0] and pos[1]+i*tile_size == sprite_pos[1]):
                                    pos_to_highlight.append(pos)
                        possible_kill_pos.append(delete_after_pos_tl_diagonally)
                    else:
                        for sprite in self.all_b_sprites_group.sprites():
                            if sprite.rect.topleft == (sprite_pos[0]-tile_size,sprite_pos[1]-tile_size) and self.all_b_sprites_group.sprites().count(sprite) != self.b_king_group.sprites().count(sprite):
                                pos_to_kill.append(sprite.rect.topleft)

                    # top_right_diagonally
                    if possible_moves.count('top_right_diagonally') == 1:
                        for sprite in self.all_pieces_sprites_group.sprites():
                            for i in range(1,tiles_on_right+1):
                                if (sprite.rect.topleft[0]-i*tile_size == sprite_pos[0] and sprite.rect.topleft[1]+i*tile_size == sprite_pos[1]) and (sprite.rect.topleft[0] > delete_after_pos_tr_diagonally[0] and sprite.rect.topleft[1]>delete_after_pos_tr_diagonally[1]):
                                    delete_after_pos_tr_diagonally = sprite.rect.topleft

                        for pos in self.tiles_pos_dictionary.values():
                            for i in range(1,tiles_on_right+1):
                                if (pos[1] > delete_after_pos_tr_diagonally[1] and (pos[0]-i*tile_size == sprite_pos[0] and pos[1]+i*tile_size == sprite_pos[1])):
                                    pos_to_highlight.append(pos)
                        possible_kill_pos.append(delete_after_pos_tr_diagonally)
                    else:
                        for sprite in self.all_b_sprites_group.sprites():
                            if sprite.rect.topleft == (sprite_pos[0]+tile_size,sprite_pos[1]-tile_size) and self.all_b_sprites_group.sprites().count(sprite) != self.b_king_group.sprites().count(sprite):
                                pos_to_kill.append(sprite.rect.topleft)

                    # bottom_right_diagonally
                    if possible_moves.count('bottom_right_diagonally') == 1:
                        for sprite in self.all_pieces_sprites_group.sprites():
                            for i in range(1,tiles_on_right+1):
                                if (sprite.rect.topleft[0]-i*tile_size == sprite_pos[0] and sprite.rect.topleft[1]-i*tile_size == sprite_pos[1]) and (sprite.rect.topleft[0] < delete_after_pos_br_diagonally[0] and sprite.rect.topleft[1]<delete_after_pos_br_diagonally[1]):
                                    delete_after_pos_br_diagonally = sprite.rect.topleft

                        for pos in self.tiles_pos_dictionary.values():
                            for i in range(1,tiles_on_right+1):
                                if (pos[1] < delete_after_pos_br_diagonally[1] and (pos[0]-i*tile_size == sprite_pos[0] and pos[1]-i*tile_size == sprite_pos[1])):
                                    pos_to_highlight.append(pos)
                        possible_kill_pos.append(delete_after_pos_br_diagonally)
                    else:
                        for sprite in self.all_b_sprites_group.sprites():
                            if sprite.rect.topleft == (sprite_pos[0]+tile_size,sprite_pos[1]+tile_size) and self.all_b_sprites_group.sprites().count(sprite) != self.b_king_group.sprites().count(sprite):
                                pos_to_kill.append(sprite.rect.topleft)

                    # bottom_left_diagonally
                    if possible_moves.count('bottom_left_diagonally') == 1:
                        for sprite in self.all_pieces_sprites_group.sprites():
                            for i in range(1,tiles_on_left+1):
                                if (sprite.rect.topleft[0]+i*tile_size == sprite_pos[0] and sprite.rect.topleft[1]-i*tile_size == sprite_pos[1]) and (sprite.rect.topleft[0] > delete_after_pos_bl_diagonally[0] and sprite.rect.topleft[1]<delete_after_pos_bl_diagonally[1]):
                                    delete_after_pos_bl_diagonally = sprite.rect.topleft

                        for pos in self.tiles_pos_dictionary.values():
                            for i in range(1,tiles_on_left+1):
                                if (pos[1] < delete_after_pos_bl_diagonally[1] and (pos[0]+i*tile_size == sprite_pos[0] and pos[1]-i*tile_size == sprite_pos[1])):
                                    pos_to_highlight.append(pos)
                        possible_kill_pos.append(delete_after_pos_bl_diagonally)
                    else:
                        for sprite in self.all_b_sprites_group.sprites():
                            if sprite.rect.topleft == (sprite_pos[0]-tile_size,sprite_pos[1]+tile_size) and self.all_b_sprites_group.sprites().count(sprite) != self.b_king_group.sprites().count(sprite):
                                pos_to_kill.append(sprite.rect.topleft)

                if self.type == 'king':
                    if possible_moves.count('top') == 1 and enemy_possible_checks.count((sprite_pos[0],sprite_pos[1]-tile_size)) == 0: pos_to_highlight.append((sprite_pos[0],sprite_pos[1]-tile_size))
                    if possible_moves.count('right') == 1 and enemy_possible_checks.count((sprite_pos[0]+tile_size,sprite_pos[1])) == 0: pos_to_highlight.append((sprite_pos[0]+tile_size,sprite_pos[1]))
                    if possible_moves.count('bottom') == 1 and enemy_possible_checks.count((sprite_pos[0],sprite_pos[1]+tile_size)) == 0: pos_to_highlight.append((sprite_pos[0],sprite_pos[1]+tile_size))
                    if possible_moves.count('left') == 1 and enemy_possible_checks.count((sprite_pos[0]-tile_size,sprite_pos[1])) == 0: pos_to_highlight.append((sprite_pos[0]-tile_size,sprite_pos[1]))
                    if possible_moves.count('top_left_diagonally') == 1 and enemy_possible_checks.count((sprite_pos[0]-tile_size,sprite_pos[1]-tile_size)) == 0: pos_to_highlight.append((sprite_pos[0]-tile_size,sprite_pos[1]-tile_size))
                    if possible_moves.count('top_right_diagonally') == 1 and enemy_possible_checks.count((sprite_pos[0]+tile_size,sprite_pos[1]-tile_size)) == 0: pos_to_highlight.append((sprite_pos[0]+tile_size,sprite_pos[1]-tile_size))
                    if possible_moves.count('bottom_right_diagonally') == 1 and enemy_possible_checks.count((sprite_pos[0]+tile_size,sprite_pos[1]+tile_size)) == 0: pos_to_highlight.append((sprite_pos[0]+tile_size,sprite_pos[1]+tile_size))
                    if possible_moves.count('bottom_left_diagonally') == 1 and enemy_possible_checks.count((sprite_pos[0]-tile_size,sprite_pos[1]+tile_size)) == 0: pos_to_highlight.append((sprite_pos[0]-tile_size,sprite_pos[1]+tile_size))
                
                if self.type == 'knight':
                    if possible_moves.count('l_topleft') == 1: pos_to_highlight.append((sprite_pos[0]-tile_size,sprite_pos[1]-2*tile_size))
                    if possible_moves.count('l_topright') == 1: pos_to_highlight.append((sprite_pos[0]+tile_size,sprite_pos[1]-2*tile_size))
                    if possible_moves.count('l_bottomright') == 1: pos_to_highlight.append((sprite_pos[0]+tile_size,sprite_pos[1]+2*tile_size))
                    if possible_moves.count('l_bottomleft') == 1: pos_to_highlight.append((sprite_pos[0]-tile_size,sprite_pos[1]+2*tile_size))
                    if possible_moves.count('l_lefttop') == 1: pos_to_highlight.append((sprite_pos[0]-2*tile_size,sprite_pos[1]-tile_size))
                    if possible_moves.count('l_righttop') == 1: pos_to_highlight.append((sprite_pos[0]+2*tile_size,sprite_pos[1]-tile_size))
                    if possible_moves.count('l_rightbottom') == 1: pos_to_highlight.append((sprite_pos[0]+2*tile_size,sprite_pos[1]+tile_size))
                    if possible_moves.count('l_leftbottom') == 1: pos_to_highlight.append((sprite_pos[0]-2*tile_size,sprite_pos[1]+tile_size))

                    for sprite in self.all_b_sprites_group.sprites():
                        if ((sprite.rect.topleft[0]+tile_size,sprite.rect.topleft[1]+2*tile_size) == sprite_pos): pos_to_kill.append(sprite.rect.topleft)
                        elif ((sprite.rect.topleft[0]-tile_size,sprite.rect.topleft[1]+2*tile_size) == sprite_pos): pos_to_kill.append(sprite.rect.topleft)
                        elif ((sprite.rect.topleft[0]-tile_size,sprite.rect.topleft[1]-2*tile_size) == sprite_pos): pos_to_kill.append(sprite.rect.topleft)
                        elif ((sprite.rect.topleft[0]+tile_size,sprite.rect.topleft[1]-2*tile_size) == sprite_pos): pos_to_kill.append(sprite.rect.topleft)
                        elif ((sprite.rect.topleft[0]+2*tile_size,sprite.rect.topleft[1]+tile_size) == sprite_pos): pos_to_kill.append(sprite.rect.topleft)
                        elif ((sprite.rect.topleft[0]-2*tile_size,sprite.rect.topleft[1]+tile_size) == sprite_pos): pos_to_kill.append(sprite.rect.topleft)
                        elif ((sprite.rect.topleft[0]-2*tile_size,sprite.rect.topleft[1]-tile_size) == sprite_pos): pos_to_kill.append(sprite.rect.topleft)
                        elif ((sprite.rect.topleft[0]+2*tile_size,sprite.rect.topleft[1]-tile_size) == sprite_pos): pos_to_kill.append(sprite.rect.topleft)
                
                if self.type == 'pawn':
                    if possible_moves.count('top') == 1:
                        if sprite_pos[1] < 800:
                            pos_to_highlight.append((sprite_pos[0],sprite_pos[1]-tile_size))
                        elif sprite_pos[1] == 800:
                            for i in range(1,3):
                                pos_to_highlight.append((sprite_pos[0],sprite_pos[1]-tile_size*i))
                    for sprite in self.all_b_sprites_group.sprites():
                        if (sprite_pos[0]-tile_size,sprite_pos[1]-tile_size) == sprite.rect.topleft:
                            pos_to_kill.append(sprite.rect.topleft)
                        elif (sprite_pos[0]+tile_size,sprite_pos[1]-tile_size) == sprite.rect.topleft:
                            pos_to_kill.append(sprite.rect.topleft)
                    
                """for pos in pos_to_highlight:
                    for sprite in self.all_b_sprites_group.sprites():
                        if sprite.rect.topleft == pos:
                            possible_kill_pos.append(pos)"""
                for pos in possible_kill_pos:
                    for sprite in self.all_b_sprites_group.sprites():
                        if sprite.rect.topleft == pos:
                            pos_to_kill.append(pos)


                self.highlight(pos_to_highlight, pos_to_kill)
            
            return True

        
    def check_opposite_moves(self,enemy_pieces):
        possible_checks_pos = []
        if enemy_pieces == self.all_b_sprites_group:
            for sprite in enemy_pieces:
                pos = sprite.rect.topleft
                if self.b_pawns_group.sprites().count(sprite) == 1:
                    possible_checks_pos.extend(((pos[0]+tile_size,pos[1]+tile_size),(pos[0]-tile_size,pos[1]-tile_size)))
                if self.b_knights_group.sprites().count(sprite) == 1:
                    possible_checks_pos.extend(((pos[0]-2*tile_size,pos[1]-tile_size),(pos[0]-tile_size,pos[1]-2*tile_size),(pos[0]+tile_size,pos[1]-2*tile_size),(pos[0]+2*tile_size,pos[1]-tile_size),
                                               (pos[0]+2*tile_size,pos[1]+tile_size),(pos[0]+tile_size,pos[1]+2*tile_size),(pos[0]-2*tile_size,pos[1]+tile_size),(pos[0]-tile_size,pos[1]+2*tile_size)))
        else:
            pass
        
        return possible_checks_pos

    def move_piece(self,mouse_pos):
        """Takes mouse_pos and moves the piece to the position where the users wants it and this position is valid

        Args:
            mouse_pos (tuple): position_of_mouse (x,y)
        """
        sprite_pos = self.collided_sprite[0].rect.topleft
        if True:   # was self.type != 'king'
            for pos in self.highlight_sprite_group.sprites():
                for sprite in self.all_b_sprites_group.sprites():
                    if sprite.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and sprite.rect.topleft == pos.rect.topleft:
                        self.collided_sprite[0].rect.topleft = sprite.rect.topleft
                        sprite.kill()

            for sprite in self.highlight_sprite_group.sprites():
                if sprite.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and self.all_b_sprites_group.sprites().count(sprite) == 1:
                    self.collided_sprite[0].rect.topleft = sprite.rect.topleft
                    sprite.kill()
                if sprite.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    self.collided_sprite[0].rect.topleft = sprite.rect.topleft
                
            self.highlight_sprite_group.empty()
            self.collided_sprite.clear()

        
 
    def highlight(self,pos_to_highlight,possible_kill_pos):
        """Highlight positions passed to it 

        Args:
            pos_to_highlight (list): list with positions to highlight 
            possible_kill_pos (list): list with positions to kill 
        """
        if bool(self.highlight_sprite_group.sprites()) is False :
            for pos in pos_to_highlight:
                highlight_sprite = Highlight(tile_size, pos, highlight_color)                
                self.highlight_sprite_group.add(highlight_sprite)
            for pos in possible_kill_pos:
                highlight_sprite = Highlight(tile_size, pos, kill_color)
                self.highlight_sprite_group.add(highlight_sprite)
        else:
            self.highlight_sprite_group.empty()

    def check_possible_moves(self,sprite_pos):
        """Checks possible moves, adding and removing possible moves if certain conditions has been met"""
        possible_moves = ['top','right','bottom','left','top_left_diagonally','top_right_diagonally','bottom_right_diagonally','bottom_left_diagonally','l_topleft','l_topright','l_bottomright','l_bottomleft','l_lefttop','l_righttop','l_rightbottom','l_leftbottom']
        
        if self.w_pawns_group.sprites().count(self.collided_sprite[0]) == 1:
            self.type = 'pawn'
        elif self.w_rocks_group.sprites().count(self.collided_sprite[0]) == 1:
            self.type = 'rock'
        elif self.w_bishops_group.sprites().count(self.collided_sprite[0]) == 1:
            self.type = 'bishop'
        elif self.w_knights_group.sprites().count(self.collided_sprite[0]) == 1:
            self.type = 'knight'
        elif self.w_queen_group.sprites().count(self.collided_sprite[0]) == 1:
            self.type = 'queen'
        elif self.w_king_group.sprites().count(self.collided_sprite[0]) == 1:
            self.type = 'king'
            
        for sprite in self.all_pieces_sprites_group.sprites():
            if sprite.rect.topleft != sprite_pos:
                on_right = sprite_pos[0] == self.bottomright_board_tile_pos[0]
                on_left = sprite_pos[0] == self.bottomleft_board_tile_pos[0]
                on_top = sprite_pos[1] == self.topright_board_tile_pos[1]
                on_bottom = sprite_pos[1] == self.bottomleft_board_tile_pos[1]
                on_top_knight = sprite_pos[1] == self.topright_board_tile_pos[1] + tile_size
                on_bottom_knight = sprite_pos[1] == self.bottomleft_board_tile_pos[1] - tile_size 
                on_left_knight = sprite_pos[0] == self.topleft_board_tile_pos[0] + tile_size
                on_right_knight = sprite_pos[0] == self.topright_board_tile_pos[0] - tile_size

                if ((sprite.rect.topleft[0] == sprite_pos[0] and sprite.rect.topleft[1]+tile_size == sprite_pos[1]) or on_top) and possible_moves.count('top') == 1: possible_moves.remove('top')                  
                if ((sprite.rect.topleft[1] == sprite_pos[1] and sprite.rect.topleft[0]-tile_size == sprite_pos[0]) or on_right) and possible_moves.count('right') == 1: possible_moves.remove('right')                  
                if ((sprite.rect.topleft[0] == sprite_pos[0] and sprite.rect.topleft[1]-tile_size == sprite_pos[1]) or on_bottom) and possible_moves.count('bottom') == 1: possible_moves.remove('bottom')
                if ((sprite.rect.topleft[1] == sprite_pos[1] and sprite.rect.topleft[0]+tile_size == sprite_pos[0]) or on_left) and possible_moves.count('left') == 1: possible_moves.remove('left')
                if (((sprite.rect.topleft[0]+tile_size,sprite.rect.topleft[1]+tile_size) == sprite_pos) or on_left or on_top) and possible_moves.count('top_left_diagonally') == 1: possible_moves.remove('top_left_diagonally')
                if (((sprite.rect.topleft[0]-tile_size,sprite.rect.topleft[1]+tile_size) == sprite_pos) or on_right or on_top) and possible_moves.count('top_right_diagonally') == 1: possible_moves.remove('top_right_diagonally')
                if (((sprite.rect.topleft[0]-tile_size,sprite.rect.topleft[1]-tile_size) == sprite_pos) or on_right or on_bottom) and possible_moves.count('bottom_right_diagonally') == 1: possible_moves.remove('bottom_right_diagonally')
                if (((sprite.rect.topleft[0]+tile_size,sprite.rect.topleft[1]-tile_size) == sprite_pos) or on_left or on_bottom) and possible_moves.count('bottom_left_diagonally') == 1: possible_moves.remove('bottom_left_diagonally')        
                if (((sprite.rect.topleft[0]+tile_size,sprite.rect.topleft[1]+2*tile_size) == sprite_pos) or on_left or on_top or on_top_knight) and possible_moves.count('l_topleft') == 1: possible_moves.remove('l_topleft')
                if (((sprite.rect.topleft[0]-tile_size,sprite.rect.topleft[1]+2*tile_size) == sprite_pos) or on_right or on_top or on_top_knight) and possible_moves.count('l_topright') == 1: possible_moves.remove('l_topright')
                if (((sprite.rect.topleft[0]-tile_size,sprite.rect.topleft[1]-2*tile_size) == sprite_pos) or on_right or on_bottom or on_bottom_knight) and possible_moves.count('l_bottomright') == 1: possible_moves.remove('l_bottomright')
                if (((sprite.rect.topleft[0]+tile_size,sprite.rect.topleft[1]-2*tile_size) == sprite_pos) or on_left or on_bottom or on_bottom_knight) and possible_moves.count('l_bottomleft') == 1: possible_moves.remove('l_bottomleft')
                if (((sprite.rect.topleft[0]+2*tile_size,sprite.rect.topleft[1]+tile_size) == sprite_pos) or on_left or on_top or on_left_knight) and possible_moves.count('l_lefttop') == 1: possible_moves.remove('l_lefttop')
                if (((sprite.rect.topleft[0]-2*tile_size,sprite.rect.topleft[1]+tile_size) == sprite_pos) or on_right or on_top or on_right_knight) and possible_moves.count('l_righttop') == 1: possible_moves.remove('l_righttop')
                if (((sprite.rect.topleft[0]-2*tile_size,sprite.rect.topleft[1]-tile_size) == sprite_pos) or on_right or on_bottom or on_right_knight) and possible_moves.count('l_rightbottom') == 1: possible_moves.remove('l_rightbottom')
                if (((sprite.rect.topleft[0]+2*tile_size,sprite.rect.topleft[1]-tile_size) == sprite_pos) or on_left or on_bottom or on_left_knight) and possible_moves.count('l_leftbottom') == 1: possible_moves.remove('l_leftbottom')

        if self.type == 'rock':
            rock_possible_moves = ['top','right','bottom','left']
            possible_moves = list(set(possible_moves).intersection(rock_possible_moves))
        if self.type == 'knight':
            knight_possible_moves = ['l_topleft','l_topright','l_bottomright','l_bottomleft','l_lefttop','l_righttop','l_rightbottom','l_leftbottom']
            possible_moves = list(set(possible_moves).intersection(knight_possible_moves))
        if self.type == 'bishop':
            bishop_possible_moves = ['top_left_diagonally','top_right_diagonally','bottom_right_diagonally','bottom_left_diagonally']
            possible_moves = list(set(possible_moves).intersection(bishop_possible_moves))
        if self.type == 'queen':
            queen_possible_moves = ['top','right','bottom','left','top_left_diagonally','top_right_diagonally','bottom_right_diagonally','bottom_left_diagonally']
            possible_moves = list(set(possible_moves).intersection(queen_possible_moves))
        if self.type == 'pawn':
            pawn_possible_moves = ['top']
            possible_moves = list(set(possible_moves).intersection(pawn_possible_moves))
        if self.type == 'king':
            king_possible_moves = ['top','right','bottom','left','top_left_diagonally','top_right_diagonally','bottom_right_diagonally','bottom_left_diagonally']
            possible_moves = list(set(possible_moves).intersection(king_possible_moves))

        return possible_moves

    def run(self):

        self.create_chess_board(chess_board)
        self.create_chess_board_wrap(chess_board_wrap)

        # highlights
        self.highlight_sprite_group.update()
        self.highlight_sprite_group.draw(self.display_surface)

        # pawns
        self.b_pawns_group.update()
        self.b_pawns_group.draw(self.display_surface)
        self.w_pawns_group.update()
        self.w_pawns_group.draw(self.display_surface)

        # rocks
        self.b_rocks_group.update()
        self.b_rocks_group.draw(self.display_surface)
        self.w_rocks_group.update()
        self.w_rocks_group.draw(self.display_surface)

        # knights
        self.b_knights_group.update()
        self.b_knights_group.draw(self.display_surface)
        self.w_knights_group.update()
        self.w_knights_group.draw(self.display_surface)

        # bishops
        self.b_bishops_group.update()
        self.b_bishops_group.draw(self.display_surface)
        self.w_bishops_group.update()
        self.w_bishops_group.draw(self.display_surface)

        # queens
        self.b_queen_group.update()
        self.b_queen_group.draw(self.display_surface)
        self.w_queen_group.update()
        self.w_queen_group.draw(self.display_surface)

        # kings
        self.b_king_group.update()
        self.b_king_group.draw(self.display_surface)
        self.w_king_group.update()
        self.w_king_group.draw(self.display_surface)

        


