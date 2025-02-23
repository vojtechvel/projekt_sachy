#Projekt šachů pro dva hráče

import pygame
import multiprocessing
from draw import *
from constants import *
pygame.init()

#/////////////////////////////////////
#funkce kotrolující tahy nebo stav hry
#/////////////////////////////////////

# fukce kontrouje všechny validní tahy a následně je vrací
def check_options(pieces, locations, turn):
    global castling_moves
    moves_list = []
    all_moves_list = []
    castling_moves = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list, castling_moves = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list

# funkce kontroluje možné tahy krále i s rošádou kterou vrací
def check_king(position, color):
    moves_list = []
    castle_moves = check_castling()

    # 8 možných tahů pro krále
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations   
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(8):
        #pokud je cílová pozice na šachovnici a není tam žádný vlastní figurka tak se přidá do možných tahů
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
     
    return moves_list, castle_moves

# funkce kontroluje možné tahy střelce
def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # 0-nahoru doprava,1-nahoru doleva,2-dolů doprava,3-dolů doleva
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            #dokud je cesta volná a není tam žádný vlastní tak se přidává do možných tahů a posunuje se o jeden, pokud cizí figurka tak se přidá a cesta končí
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

# funkce kontroluje možné tahy věže
def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # dolů, nahoru, doprava, doleva
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            #funguje stejně jako u střelce
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

# funkce kontroluje možné tahy královny. je složena z funkcí střelce a věže
def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list

# funkce kontroluje možné tahy pěšce
def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        #pokud pěšec má volnou cestu dopředu, nebo není na konci šachovnice tak se přidává se do možných tahů
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
            # pokud je pěšec na začátku šachovnice a má volnou cestu o dvě pole dopředu tak se přidává do možných tahů
            # aby se mohl pohnout o dvě pole je implementována kontrola pro pozici o jendo před ním
            if (position[0], position[1] + 2) not in white_locations and \
                    (position[0], position[1] + 2) not in black_locations and position[1] == 1:
                moves_list.append((position[0], position[1] + 2))
        #pokud je o jedno pole vpřed a jedno pole doprava nebo doleva cizí figurka tak se přidává do možných tahů
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
        #kontooruje en pesant
        if (position[0] + 1, position[1] + 1) == black_ep:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) == black_ep:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
            if (position[0], position[1] - 2) not in white_locations and \
                    (position[0], position[1] - 2) not in black_locations and position[1] == 6:
                moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
        if (position[0] + 1, position[1] - 1) == white_ep:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) == white_ep:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list

# funkce kontroluje možné tahy koně
def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 možných tahů pro koně
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list

# funkce kontrojuje možné tahy pro vybranou figurku
def check_valid_moves(white_options, black_options):
    
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection] 
    return valid_options

# funkce pro kontrolu možnosti hrát rošádu
def check_castling():
    
    # aby se mohlo provést rošáda musí být král a věž na svých startovních pozicích král nebýt v šachu a v cestě mezi králem a věží nesmí být žádná figurka 
    castle_moves = []  # valídní tahy se ukládají v typu[(král_pozice, věž_pozice)]
    rook_indexes = []
    rook_locations = []
    king_index = 0
    king_pos = (0, 0) 
    #kontrola jestli se vězě nepohly
    if turn_step > 1:
        for i in range(len(white_pieces)):
            if white_pieces[i] == 'rook':
                rook_indexes.append(white_moved[i])
                rook_locations.append(white_locations[i])
            if white_pieces[i] == 'king':
                king_index = i
                king_pos = white_locations[i]
                #pokud  se král nepohyboval a není v šachu a věž tak se může provést rošáda
        if not white_moved[king_index] and False in rook_indexes and not check:
            for i in range(len(rook_indexes)):
                castle = True
                #vypočítání volných souřadnic mezi králem a věží
                if rook_locations[i][0] > king_pos[0]:
                    empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]),
                                     (king_pos[0] + 3, king_pos[1])]
                else:
                    empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]
                #kontrola zda se na volných souřadnicích nachází  figurka nebo jestli tam může soupeř táhnout
                for j in range(len(empty_squares)):
                    if empty_squares[j] in white_locations or empty_squares[j] in black_locations or \
                            empty_squares[j] in black_options or rook_indexes[i]:
                        castle = False
                if castle:
                    castle_moves.append((empty_squares[1], empty_squares[0]))
    else:
        for i in range(len(black_pieces)):
            if black_pieces[i] == 'rook':
                rook_indexes.append(black_moved[i])
                rook_locations.append(black_locations[i])
            if black_pieces[i] == 'king':
                king_index = i
                king_pos = black_locations[i]
        if not black_moved[king_index] and False in rook_indexes and not check:
            for i in range(len(rook_indexes)):
                castle = True
                if rook_locations[i][0] > king_pos[0]:
                    empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]),
                                     (king_pos[0] + 3, king_pos[1])]
                else:
                    empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]
                for j in range(len(empty_squares)):
                    if empty_squares[j] in white_locations or empty_squares[j] in black_locations or \
                            empty_squares[j] in white_options or rook_indexes[i]:
                        castle = False
                if castle:
                    castle_moves.append((empty_squares[1], empty_squares[0]))
    return castle_moves



# funkce kontroluje en pesant
#kontroluje minulý pohyb pěšce pokud byl o dva se nastaví do lokací
def check_ep(old_coords, new_coords):
    if turn_step <= 1:
        index = white_locations.index(old_coords)
        ep_coords = (new_coords[0], new_coords[1] - 1)
        piece = white_pieces[index]
    else:
        index = black_locations.index(old_coords)
        ep_coords = (new_coords[0], new_coords[1] + 1)
        piece = black_pieces[index]
    if piece == 'pawn' and abs(old_coords[1] - new_coords[1]) > 1:
        # pokud platí tak pokračuj
        pass
    else:#pokud ne tak se nastaví na (100,100)(neexistující pozice. aby nenastaly errory
        ep_coords = (100, 100)
    return ep_coords

# testujeme jestli se nějaký pěšec dostal na konec šachovnice
def check_promotion():
    pawn_indexes = []
    white_promotion = False
    black_promotion = False
    promote_index = 100
    for i in range(len(white_pieces)):
        if white_pieces[i] == 'pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if white_locations[pawn_indexes[i]][1] == 7:
            white_promotion = True
            promote_index = pawn_indexes[i]
    pawn_indexes = []
    for i in range(len(black_pieces)):
        if black_pieces[i] == 'pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if black_locations[pawn_indexes[i]][1] == 0:
            black_promotion = True
            promote_index = pawn_indexes[i]
    return white_promotion, black_promotion, promote_index

# funkce kontroluje jakou figurku na vylepšení si hráč vybral
def check_promo_select():
    mouse_pos = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    x_pos = mouse_pos[0] // 100
    y_pos = mouse_pos[1] // 100
    if white_promote and left_click and x_pos > 7 and y_pos < 4:
        white_pieces[promo_index] = white_promotions[y_pos]
    elif black_promote and left_click and x_pos > 7 and y_pos < 4:
        black_pieces[promo_index] = black_promotions[y_pos]




#//////////////
#ostatní funkce
#//////////////


#funkce pro aktualizování herního času
def change_time():
    global b_seconds, b_minutes, w_seconds, w_minutes, winner, game_over
    if turn_step == 0 or turn_step == 1:
        w_seconds -= 1
        if w_seconds < 0:
            w_seconds = 59
            w_minutes -= 1
        if w_minutes < 0:
            w_minutes = 0
            w_seconds = 0
            winner = 'black'
            game_over = True  
    elif turn_step == 2 or turn_step == 3:
        b_seconds -= 1
        if b_seconds < 0:
            b_seconds = 59
            b_minutes -= 1
        if b_minutes < 0:
            b_minutes = 0
            b_seconds = 0
            winner = 'white'
            game_over = True


#funkce pro kontrolu šachmatu
#spustí se pokud je šach a fukce provede všechny možné tahy a pokud se nenaskytne tah který by opakovný šach 
#odstranil tak se jedná o šachmat
def check_checkmate():
    
    if turn_step < 2:
        king_index = white_pieces.index('king')
        king_location = white_locations[king_index]
        if king_location in black_options:
            for i in range(len(white_options)):
                black_pieces_im = black_pieces
                black_locations_im = black_locations
                if white_options[i] in black_options or white_options[i] in black_locations:
                    if not white_options[i] in check_king(king_location, 'white'):
                        imaginary_move = white_options[i]
                        if imaginary_move in black_locations:
                            black_pieces_im.pop(black_locations_im.index(imaginary_move))
                            black_locations_im.pop(black_locations_im.index(imaginary_move))
                        white_locations.append(imaginary_move)
                        black_options_im = check_options(black_pieces_im, black_locations_im, 'black')
                        white_locations.pop(imaginary_move)
                        if not king_location in black_options_im:
                            return False
                    elif white_options[i] in check_king(king_location, 'white'):
                        if not white_options[i] in black_options:
                            return False
        else:
            return False
                                          
    else:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            if king_location in white_options:
                for i in range(len(black_options)):
                    white_pieces_im = white_pieces
                    white_locations_im = white_locations
                    if black_options[i] in white_options or black_options[i] in white_locations:
                        if not black_options[i] in check_king(king_location, 'black'):
                            imaginary_move = black_options[i]
                            if imaginary_move in white_locations:
                                white_pieces_im.pop(white_locations_im.index(imaginary_move))
                                white_locations_im.pop(white_locations_im.index(imaginary_move))
                            black_locations.append(imaginary_move)
                            white_options_im = check_options(white_pieces_im, white_locations_im, 'white')
                            black_locations.pop(imaginary_move)
                            if not king_location in white_options_im:
                                return False
                        elif black_options[i] in check_king(king_location, 'black'):
                            if not black_options[i] in white_options:
                                return False
            else:
                return False
    return True

def makes_im_move(turn_ste, white_location, black_location, white_piec, black_piec, step):
    global black_wins, white_wins
    turn_step_im = turn_ste
    white_locations_im = white_location[:]
    black_locations_im = black_location[:]
    white_pieces_im = white_piec[:]
    black_pieces_im = black_piec[:]
    steps = step
    steps += 1
    simulations = 0

    if turn_step_im < 2:
        for i in range(len(white_pieces_im)):
            if len(white_pieces_im) <= i:
                continue
            if white_pieces_im[i] == 'pawn':
                moves = check_pawn(white_locations_im[i], 'white')
            elif white_pieces_im[i] == 'rook':
                moves = check_rook(white_locations_im[i], 'white')
            elif white_pieces_im[i] == 'knight':
                moves = check_knight(white_locations_im[i], 'white')
            elif white_pieces_im[i] == 'bishop':
                moves = check_bishop(white_locations_im[i], 'white')
            elif white_pieces_im[i] == 'queen':
                moves = check_queen(white_locations_im[i], 'white')
            else:
                continue
            for j in range(len(moves)):
                if moves[j] in black_locations_im:
                    black_pieces_im.pop(black_locations_im.index(moves[j]))
                    black_locations_im.pop(black_locations_im.index(moves[j]))
                white_locations_im[i] = moves[j]
                
                if steps<=4:
                    if steps % 2 != 0:
                        a = check_checkmate()
                        if a:
                            simulations += 1
                            white_wins += 1
                            return simulations
                    turn_step_im = 2
                    simulations += makes_im_move(turn_step_im, white_locations_im, black_locations_im, white_pieces_im, black_pieces_im, steps)
                else:
                    simulations += 1
                    a = check_checkmate()
                    if a:
                        white_wins += 1
            white_locations_im = white_location[:]
            black_locations_im = black_location[:]
            white_pieces_im = white_piec[:]
            black_pieces_im = black_piec[:]
    else:
        for i in range(len(black_pieces_im)):
            if len(black_pieces_im) <= i:
                continue
            if black_pieces_im[i] == 'pawn':
                moves = check_pawn(black_locations_im[i], 'black')
            elif black_pieces_im[i] == 'rook':
                moves = check_rook(black_locations_im[i], 'black')
            elif black_pieces_im[i] == 'knight':
                moves = check_knight(black_locations_im[i], 'black')
            elif black_pieces_im[i] == 'bishop':
                moves = check_bishop(black_locations_im[i], 'black')
            elif black_pieces_im[i] == 'queen':
                moves = check_queen(black_locations_im[i], 'black')
            else:
                continue
            for j in range(len(moves)):
                if moves[j] in white_locations_im:
                    white_pieces_im.pop(white_locations_im.index(moves[j]))
                    white_locations_im.pop(white_locations_im.index(moves[j])) 
                if len(black_locations_im) <= i:
                    continue 
                black_locations_im[i] = moves[j]
                if steps<=4:
                    if steps % 2 != 0:
                        a = check_checkmate()
                        if a:
                            simulations += 1
                            black_wins += 1
                            return simulations
                    turn_step_im = 0
                    simulations += makes_im_move(turn_step_im, white_locations_im, black_locations_im, white_pieces_im, black_pieces_im, steps)
                else:
                    simulations += 1
                    a = check_checkmate()
                    if a:
                        black_wins += 1
                white_locations_im = white_location[:]
                black_locations_im = black_location[:]
                white_pieces_im = white_piec[:]
                black_pieces_im = black_piec[:]
    return simulations
                
                    


def chance():
    simulations = 0
    steps = 0
    simulations += makes_im_move(turn_step, white_locations, black_locations, white_pieces, black_pieces, steps)
    if turn_step < 2:
        if white_wins == 0 or simulations == 0:
            w_chance = 0
        else:
            w_chance = (white_wins / simulations)
    else:
        if black_wins == 0 or simulations == 0:
            b_chance = 0
        else:
            b_chance = (black_wins / simulations)
    print(simulations)

def del_king_move():
    if "king" in white_pieces and "king" in black_pieces:
        if turn_step > 2:
            index = white_pieces.index('king')
            for i in range(len(white_options[index])):
                if white_options[index][i] in black_options:
                    white_options[index].pop(i) 
        else:
            index = black_pieces.index('king')
            for i in range(len(black_options[index])):
                if black_options[index][i] in white_options:
                    black_options[index].pop(i)
            

#////////////////////////
# loop pro hlavní část hry
#////////////////////////



#na začátku kontrojuje volné tahy
##proces = multiprocessing.Process(target=chance)
##proces2 = multiprocessing.Process(target=chance)
global black_options, white_options
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
del_king_move()
run = True
while run:
    timer.tick(fps)
    # kontrola času pro časovač a blikání u šachu
    if time < 60 and not start and not game_over and not tie:
        time += 1
    elif time >= 60 and not start and not game_over and not tie:
        time = 0
        change_time()
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('dark gray')
    draw_board()
    draw_pieces()
    if start:
        draw_start()
    draw_captured()
    draw_check(black_options, white_options, counter)
    if not game_over:
        white_promote, black_promote, promo_index = check_promotion()
        if white_promote or black_promote:
            draw_promotion()
            check_promo_select()
    #pokud je vybraná figurka tak se vykreslí a zkontrolují možné tahy
    if selection != 100:
        valid_moves = check_valid_moves(white_options, black_options)	
        draw_valid(valid_moves)
        if selected_piece == 'king':
            draw_castling(castling_moves)
    # event handling/spracovávání událostí
    for event in pygame.event.get():
        #pokud je zmáčknuté křížek tak se hra ukončí
        if event.type == pygame.QUIT:
            run = False
        #pokud je zmáčknuté tlačítko ENTER a hra je na začátku tak se nastaví časomíra na 10 minut 
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and start:
            start = False
            b_minutes, w_minutes = 10, 10
            b_seconds, w_seconds = 0, 0
        #pokud je zmáčknuté tlačítko TAB a hra je na začátku tak se nastaví časomíra na 5 minut 
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB and start:
            start = False
            b_minutes, w_minutes = 5, 5 
            b_seconds, w_seconds = 0, 0
        #reakce na klik myší když není konec hry a není na začátek hry
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over and not start:
            #upravení souřadnic na typ (6,6) z typu (600,600)(čtverečnové vybírání)
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
            #pokud jsou tyto souřadnice tak se kliklo na tlačítko remíza
            if click_coords == (8, 9) or click_coords == (9, 9):
                  tie = True
            #pokud je na tahu bílý hráč
            if turn_step <= 1:
                #pokud jsou tyto souřadnice tak se kliklo na tlačítko VZDÁT
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'black'
                #pokud jsou souřadnice na terci kde je nějaká bílá figurka tak se uloží do proměnné selection a turn_step se změní na 1
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    selected_piece = white_pieces[selection]
                    if turn_step == 0:
                        turn_step = 1
                #pokud jsou souřadnice na možných tazích a je vybraná figurka tak se provede tah
                if click_coords in valid_moves and selection != 100:
                    #zde se zpracovává kontrola en passant před tím než se načtou nové možné tahy 
                    white_ep = check_ep(white_locations[selection], click_coords)
                    white_locations[selection] = click_coords
                    white_moved[selection] = True
                    #pokud je na souřadnicích černá figurka tak se sebrá a přidá do seznamu sebraných figur
                    if click_coords in black_locations:
                        black_piece = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece])
                        if black_pieces[black_piece] == 'king':
                            winner = 'white'
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                        black_moved.pop(black_piece)
                    if click_coords == black_ep:
                        black_piece = black_locations.index((black_ep[0], black_ep[1] - 1))
                        captured_pieces_white.append(black_pieces[black_piece])
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                        black_moved.pop(black_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    del_king_move()
                    turn_step = 2
                    selection = 100
                    valid_moves = []
                elif selection != 100 and selected_piece == 'king':
                    for q in range(len(castling_moves)):
                        if click_coords == castling_moves[q][0]:
                            white_locations[selection] = click_coords
                            white_moved[selection] = True
                            if click_coords == (1, 0):
                                rook_coords = (0, 0)
                            else:
                                rook_coords = (7, 0)
                            rook_index = white_locations.index(rook_coords)
                            white_locations[rook_index] = castling_moves[q][1]
                            black_options = check_options(black_pieces, black_locations, 'black')
                            white_options = check_options(white_pieces, white_locations, 'white')
                            del_king_move()
                            turn_step = 2
                            selection = 100
                            valid_moves = []
            """if proces.is_alive():
                proces.terminate()	
            proces.start()"""
            #tah černého hráče
            if turn_step > 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'white'
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    selected_piece = black_pieces[selection]
                    if turn_step == 2:
                        turn_step = 3
                if click_coords in valid_moves and selection != 100:
                    black_ep = check_ep(black_locations[selection], click_coords)
                    black_locations[selection] = click_coords
                    black_moved[selection] = True
                    if click_coords in white_locations:
                        white_piece = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece])
                        if white_pieces[white_piece] == 'king':
                            winner = 'black'
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                        white_moved.pop(white_piece)
                    if click_coords == white_ep:
                        white_piece = white_locations.index((white_ep[0], white_ep[1] + 1))
                        captured_pieces_black.append(white_pieces[white_piece])
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                        white_moved.pop(white_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    del_king_move()
                    turn_step = 0
                    selection = 100
                    valid_moves = []
                elif selection != 100 and selected_piece == 'king':
                    for q in range(len(castling_moves)):
                        if click_coords == castling_moves[q][0]:
                            black_locations[selection] = click_coords
                            black_moved[selection] = True
                            if click_coords == (1, 7):
                                rook_coords = (0, 7)
                            else:
                                rook_coords = (7, 7)
                            rook_index = black_locations.index(rook_coords)
                            black_locations[rook_index] = castling_moves[q][1]
                            black_options = check_options(black_pieces, black_locations, 'black')
                            white_options = check_options(white_pieces, white_locations, 'white')
                            del_king_move()
                            turn_step = 0
                            selection = 100
                            valid_moves = []
            """if  proces2.is_alive():
                proces2.terminate()
            proces2.start()"""
        #pokud je zmáčknuté tlačítko ENTER když hráč požáda o remízu nastaví se konec hry na remízu
        if event.type == pygame.KEYDOWN and tie and not start:
            if event.key == pygame.K_RETURN:
                winner = 'remiza'
                game_over = True
            #pokud TAB tak se pokračuje ve hře
            elif event.key == pygame.K_TAB:
                tie = False
        
        #pokud je zmáčknuté tlačítko ENTER a hra je u konce tak se hra restartuje
        if event.type == pygame.KEYDOWN and game_over and not start:
            if event.key == pygame.K_RETURN:
                start = True
                tie = False
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                white_moved = [False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False]
                black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                black_moved = [False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')
                del_king_move()
                black_chance = 50
                white_chance = 50
    if tie:
        draw_tie()
                
    if winner != '':
        game_over = True
        draw_game_over()

    pygame.display.flip()
pygame.quit()
