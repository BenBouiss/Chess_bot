import pygame as p
from ChessBoard import Chess_t
import numpy as np
from Evaluation_part import Bot
import time
from collections import Counter
import os
import glob
import cProfile
import pstats
Image = {}
MAX_FPS = 60
WIDTH = HEIGHT = 512
dim = 8
SQ_size = WIDTH // dim 
path = 'Mate/'
def loadimage():
    path = "Image/"
    List = ['wK', 'wQ', 'wB', 'wN', 'wR', 'wP','bK', 'bQ', 'bB', 'bN', 'bR', 'bP']
    List2 = ['K', 'Q', 'B', 'N', 'R', 'P','k', 'q', 'b', 'n', 'r', 'p']
    for ind, i in enumerate(List): 
        Image[List2[ind]] = p.transform.scale(
            p.image.load(path + i + '.png'), (SQ_size, SQ_size))
def init(screen):
    #pygame.draw.rect(screen, color, (x,y,width,height), thickness)
    for i in range(8):
        for j in range(8):
            p.draw.rect(screen, (p.Color('white') if (i+j)%2 == 0 else p.Color('dark grey'))
                                 , (j*SQ_size, i*SQ_size, SQ_size, SQ_size), 0)
            p.display.flip()
            
def DrawPieces(screen, Board):
    for row, i in enumerate(Board):
        for col, j in enumerate(i):
            if j!= '-':
                screen.blit(Image[j], p.Rect(col*SQ_size, row*SQ_size, 
                                             SQ_size, SQ_size))
    p.display.flip()
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    loadimage()
    running = True
    init(screen)
    
    
    Chess = Chess_t()
    Chess.decode()
    Board = Chess.Init_Board
    # print(Board)
    
    Eval = Bot()
    
    DrawPieces(screen, Board)
    Tour = 'White'
    # print(Tour + 's turn')
    Tour_bot = []
    # Tour_bot = ['Black']
    Win = False
    DEPTH = 2
    while running:
        if not Win:
            if Tour in Tour_bot:
                start = time.time()
                Choice, count, TIME = Eval.Exploration(Board, Tour, Depth = DEPTH)
                #cProfile.runctx('Eval.Exploration(Board, Tour, Depth = DEPTH)', 
                #                {'Board': Board, 'Tour': Tour, 'DEPTH' : DEPTH, 
                #                 'Eval': Eval},{}, sort='tottime')
                #T = pstats.Stats("Test")
                #T.sort_stats("cumulative").print_stats()
                if Choice == None:
                    if Chess.Check_for_mate(Board, Tour):
                        Won = Chang_tour(Tour)
                    else:
                        Won = 'Neither'
                    print(Board)
                    p.image.save(screen, path + Won + '_' + str(round(time.time())) + '.jpg')
                    return Won
                    running = False
                else:
                    # if TIME <= 0.1:
                    #     DEPTH += 1
                    #     print(DEPTH)
                    # elif TIME > 0.5:
                    #     DEPTH += -1
                    Board = Chess.Move_to(Board, Choice)
                    update_screen_2(screen, Choice, Board, Chess)
                    Tour = Chang_tour(Tour)
                    end = time.time()
                    if Chess.Check_for_draw(Board):
                        Won = 'Neither'
                        return Won
                    # print(Choice)
                    # print('Elapsed time : ' + str(end - start)
                    # + ' after ' + str(count) + ' positions analysed')
                    # print(Tour + 's turn')
                    Chess.Selection = []
        
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                if Tour not in Tour_bot:
                    if e.type == p.MOUSEBUTTONUP:
                        pos = p.mouse.get_pos()
                        xclick = pos[0] // SQ_size
                        yclick = pos[1] // SQ_size
                        
                        if len(Chess.Selection) == 0:
                            Tar = Board[yclick][xclick]
                            if  Tar != '-' and Chess.Get_couleur(Tar) == Tour:
                                Chess.Selection.append([xclick, yclick])
                                Possible_moves = Chess.Get_possible_moves(Board, xclick, yclick)
                                Possible_moves = Chess.Moves_verify(Board, Possible_moves, Tour)
                                Display_all(screen, Possible_moves)
                                if Possible_moves == []:
                                    Chess.Selection = []
                                
                        elif Chess.Selection[0] == [xclick, yclick]:
                            Chess.Selection = [] #Deselection
                            update_screen(screen, Board)
                            
                        else: # Possible move
        
                            ### Initiate move based on the move string ex : PA2-A4
                            pos1, pos2 = Chess.Selection[0], [xclick, yclick]
                            type1, type2 = Board[tuple(pos1[::-1])], Board[tuple(pos2[::-1])]
                            Move = Chess.Moves_to_string(pos1, pos2, type1, type2)
                            if type1.lower() == 'p' and (pos2[1] == 7 or pos2[1] == 0):
                                Move = ask_for_prom(Tour, Move)
                                
                            ###
                            if Move in Possible_moves:
                                Board = Chess.Move_to(Board, Move)
                                # print(Chess.Board)
                                update_screen(screen, Board)
                                Other_turn = Chang_tour(Tour)
                                if Chess.Check_for_check(Board, Other_turn):
                                    if Chess.Check_for_mate(Board, Other_turn):
                                        print(str(Other_turn) + ' lost')
                                        Win = True
                                Tour = Chang_tour(Tour)
                                print(Tour + 's turn')
                                Chess.Selection = []    
    
                    
        clock.tick(MAX_FPS)
        p.display.flip()
    # p.quit()
    return 0
def update_screen(screen, Board):
    init(screen)
    DrawPieces(screen, Board)

def update_screen_2(screen, Move, Board, Chess): #Meilleur option d'affichage
    Pos_s= Chess.String_to_position(Move)
    
    for Pos in Pos_s:
        p.draw.rect(screen, (p.Color('white') if (Pos[0]+Pos[1])%2 == 0 else p.Color('dark grey'))
                , (Pos[0]*SQ_size, Pos[1]*SQ_size, SQ_size, SQ_size), 0)
        Target = Board[Pos[1], Pos[0]]
        if Target != '-':
            screen.blit(Image[Target], p.Rect(Pos[0]*SQ_size, Pos[1]*SQ_size, 
                            SQ_size, SQ_size))
                          
def Display_all(screen, Moves):
    Letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    for Move in Moves:
        pos2 = String_to_position(Move, Letter)

        p.draw.rect(screen, p.Color('Salmon'), (pos2[0]*SQ_size, pos2[1]*SQ_size, 
                SQ_size, SQ_size), 0)
        
def Chang_tour(Tour):
    if Tour == 'White':
        return 'Black'
    else:
        return 'White'

def String_to_position(string, Letter):
    if len(string) == 6 or len(string) == 8:
        x = Letter.index(string[4])
        y = int(string[5])
        return (x,y)
    pass

def ask_for_prom(Tour, Move):
    Choix = input('What piece : ')   
    Choix = Choix.upper() if Tour == 'White' else Choix.lower() 
    return Move + '=' + Choix
if __name__ == '__main__':
    Files = glob.glob(path + '*')
    for file in Files:
        os.remove(file)
    Number = 1000
    Winner = []
    for i in range(Number):
    # while 'Neither' not in Winner:
        Start = time.time()
        Winner.append(main())
        end = time.time()
        print(str(i) + '/' + str(Number) + ' in : ' + str(end - Start) )
        i+=1
    print(Counter(Winner))