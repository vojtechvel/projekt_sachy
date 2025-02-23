import pygame
pygame.init()
from constants import *

#///////////////////
#funkce vykreslující
#///////////////////


# funkce pro vykreslení šachovnice
#funguje na principu že pozadí je šedé a každý druhý čtverec se vyhreslí čverec tmavěšedý
def draw_board():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light gray', [700 - (column * 200), row * 100, 100, 100])
        pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
        pygame.draw.rect(screen, 'gold', [0, 800, WIDTH, 100], 5)
        pygame.draw.rect(screen, 'gold', [800, 0, 200, HEIGHT], 5)
        pygame.draw.rect(screen, 'gold', [0, 900, 200, 800], 2)
        pygame.draw.rect(screen, 'gold', [200, 900, 200, 800], 2)
        pygame.draw.rect(screen, 'gold', [400, 900, 200, 800], 2)
        pygame.draw.rect(screen, 'gold', [600, 900, 200, 800], 2)
        screen.blit(medium_font.render(f'B: {w_minutes:02}:{w_seconds:02}', True, 'black'), (405, 930))
        screen.blit(medium_font.render(f'Č: {b_minutes:02}:{b_seconds:02}', True, 'black'), (5, 930))
        screen.blit(medium_font.render(f'Č: {b_chance}%', True, 'black'), (205, 930))
        screen.blit(medium_font.render(f'B: {w_chance}%', True, 'black'), (605, 930))
        #bude se měnit podle turn_step
        status_text = ['Bílá: vyber si figurku!', 'Bílá: vyber cíl!',
                       'Černá: vyber si figurku!', 'Černá vyber si cíl!']
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 820))
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)
        screen.blit(medium_font.render('VZDÁT', True, 'black'), (810, 830))
        screen.blit(medium_font.render('REMÍZA', True, 'black'), (810, 930))
        #vykreslí se pouze jestli je možné vylepšení pěšce
        if white_promote or black_promote:
            pygame.draw.rect(screen, 'gray', [0, 800, WIDTH - 200, 100])
            pygame.draw.rect(screen, 'gold', [0, 800, WIDTH - 200, 100], 5)
            screen.blit(big_font.render('Vyber figurku pro vylepšení', True, 'black'), (20, 820))

# funkce která vykresluje figurky na šachovnici
def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        #pěšec je menší než ostatní figurky tím pádem potřebuje vlastní posun pozice
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 100 + 22, white_locations[i][1] * 100 + 30))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10))
        #pokud je turn_step menší než 2(hraje bílý) tak se vykreslí červený obdélník kolem vybrané figurky
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1,
                                                 100, 100], 2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 100 + 22, black_locations[i][1] * 100 + 30))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10))
        #pokud je turn_step větší než 2 tak se vykreslí modrý obdélník kolem vybrané figurky
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1,
                                                  100, 100], 2)

#funkce vykresluje startovní obrazovku s výběrem typu hry
def draw_start():
    pygame.draw.rect(screen, 'black', [200, 200, 550, 100])
    screen.blit(font.render('Vítejte ve hře!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Zmáčkni ENTER pro start hry "rapid šach"(10 minut)', True, 'white'), (210, 240))
    screen.blit(font.render(f'Zmáčkni TAB pro start hry "blitz šach"(5 minut)', True, 'white'), (210, 270))

# funkce vykresluje validní tahy
#parametr moves je seznam s pozicemi kam může figurka táhnout a podle nich se vykresluje kolečko a to je červené(bílý) nebo modré(černý)
def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)

# funkce vykresluje sebrané figurky na bok obrazovky. každá další figurka se vykreslí o 50px níže
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (825, 5 + 50 * i))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (925, 5 + 50 * i))

# když je zahraný šach tak se vykreslí blikající(každou půl sekundu) čtverec kolem krále
def draw_check(black_options, white_options, counter):
    global check
    check = False
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                #pokud je král v možnocech černého hráče
                if king_location in black_options[i]:
                    check = True
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * 100 + 1,
                                                              white_locations[king_index][1] * 100 + 1, 100, 100], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    check = True
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [black_locations[king_index][0] * 100 + 1,
                                                               black_locations[king_index][1] * 100 + 1, 100, 100], 5)

# vykresluje čtverec pro konec hry. Bud remíza nebo výhra jednoho z hráčů
def draw_game_over():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    if winner == 'remiza':
        screen.blit(font.render('Hra skončila remízou!', True, 'white'), (210, 210))
        screen.blit(font.render(f'Zmáčkni ENTER pro restart', True, 'white'), (210, 240))
    else:    
        if winner == 'white':
            screen.blit(font.render(f'Bílý vyhrál hru!', True, 'white'), (210, 210))
        else:
            screen.blit(font.render(f'Černý vyhrál hru!', True, 'white'), (210, 210))
        screen.blit(font.render(f'Zmáčkni ENTER pro restart', True, 'white'), (210, 240))

# vykresluje čtverec pro remízu
def draw_tie():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 100])
    screen.blit(font.render('chceš uznat remízu?', True, 'white'), (210, 210))
    screen.blit(font.render(f'Zmáčkni ENTER pro potvrzení', True, 'white'), (210, 240))
    screen.blit(font.render(f'Zmáčkni TAB pro pokračování', True, 'white'), (210, 270))

# vykreslí rošádu. Kolem krále a vzdálenější věže se vykreslí kolečko a mezi nimi čára
def draw_castling(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0][0] * 100 + 50, moves[i][0][1] * 100 + 70), 8)
        screen.blit(font.render('king', True, 'black'), (moves[i][0][0] * 100 + 30, moves[i][0][1] * 100 + 70))
        pygame.draw.circle(screen, color, (moves[i][1][0] * 100 + 50, moves[i][1][1] * 100 + 70), 8)
        screen.blit(font.render('rook', True, 'black'),
                    (moves[i][1][0] * 100 + 30, moves[i][1][1] * 100 + 70))
        pygame.draw.line(screen, color, (moves[i][0][0] * 100 + 50, moves[i][0][1] * 100 + 70),
                         (moves[i][1][0] * 100 + 50, moves[i][1][1] * 100 + 70), 2)

# vykreslí výběr pro povýšení pěšce
def draw_promotion():
    pygame.draw.rect(screen, 'dark gray', [800, 0, 200, 420])
    if white_promote:
        color = 'white'
        for i in range(len(white_promotions)):
            piece = white_promotions[i]
            index = piece_list.index(piece)
            screen.blit(white_images[index], (860, 5 + 100 * i))
    elif black_promote:
        color = 'black'
        for i in range(len(black_promotions)):
            piece = black_promotions[i]
            index = piece_list.index(piece)
            screen.blit(black_images[index], (860, 5 + 100 * i))
    pygame.draw.rect(screen, color, [800, 0, 200, 420], 8)