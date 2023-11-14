import numpy as np
import time
import chess
import random
PIECES = {'q' : 900, 'r' : 500, 'b' : 400, 'n' : 400, 'p' : 100}

PIECE_SPACE = {
    'p': (   0,   0,   0,   0,   0,   0,   0,   0,
            78,  83,  86,  73, 102,  82,  85,  90,
             7,  29,  21,  44,  40,  31,  44,   7,
           -17,  16,  -2,  15,  14,   0,  15, -13,
           -26,   3,  10,   9,   6,   1,   0, -23,
           -22,   9,   5, -11, -10,  -2,   3, -19,
           -31,   8,  -7, -37, -36, -14,   3, -31,
             0,   0,   0,   0,   0,   0,   0,   0),
    'n': ( -66, -53, -75, -75, -10, -55, -58, -70,
            -3,  -6, 100, -36,   4,  62,  -4, -14,
            10,  67,   1,  74,  73,  27,  62,  -2,
            24,  24,  45,  37,  33,  41,  25,  17,
            -1,   5,  31,  21,  22,  35,   2,   0,
           -18,  10,  13,  22,  18,  15,  11, -14,
           -23, -15,   2,   0,   2,   0, -23, -20,
           -74, -23, -26, -24, -19, -35, -22, -69),
    'b': ( -59, -78, -82, -76, -23,-107, -37, -50,
           -11,  20,  35, -42, -39,  31,   2, -22,
            -9,  39, -32,  41,  52, -10,  28, -14,
            25,  17,  20,  34,  26,  25,  15,  10,
            13,  10,  17,  23,  17,  16,   0,   7,
            14,  25,  24,  15,   8,  25,  20,  15,
            19,  20,  11,   6,   7,   6,  20,  16,
            -7,   2, -15, -12, -14, -15, -10, -10),
    'r': (  35,  29,  33,   4,  37,  33,  56,  50,
            55,  29,  56,  67,  55,  62,  34,  60,
            19,  35,  28,  33,  45,  27,  25,  15,
             0,   5,  16,  13,  18,  -4,  -9,  -6,
           -28, -35, -16, -21, -13, -29, -46, -30,
           -42, -28, -42, -25, -25, -35, -26, -46,
           -53, -38, -31, -26, -29, -43, -44, -53,
           -30, -24, -18,   5,  -2, -18, -31, -32),
    'q': (   6,   1,  -8,-104,  69,  24,  88,  26,
            14,  32,  60, -10,  20,  76,  57,  24,
            -2,  43,  32,  60,  72,  63,  43,   2,
             1, -16,  22,  17,  25,  20, -13,  -6,
           -14, -15,  -2,  -5,  -1, -10, -20, -22,
           -30,  -6, -13, -11, -16, -11, -16, -27,
           -36, -18,   0, -19, -15, -15, -21, -38,
           -39, -30, -31, -13, -31, -36, -34, -42),
    'k': (   4,  54,  47, -99, -99,  60,  83, -62,
           -32,  10,  55,  56,  56,  55,  10,   3,
           -62,  12, -57,  44, -67,  28,  37, -31,
           -55,  50,  11,  -4, -19,  13,   0, -49,
           -55, -43, -52, -28, -51, -47,  -8, -50,
           -47, -42, -43, -79, -64, -32, -29, -32,
            -4,   3, -14, -50, -57, -18,  13,   4,
            17,  30,  -3, -14,   6,  -1,  40,  18),
}

CHECKMATE = 99999

Transposition_table = {}
'''
Transposition_table: dict
Key : hash (Fen code ex : "3b1q1q/1N2PRQ1/rR3KBr/B4PP1/2Pk1r1b/1P2P1N1/2P2P2/8 b") avec état du board et qui doit bouger
Items : tuple avec en premier le dplc nécessaire, en second le score et 3ème depth

'''

class Bot():
    def __init__(self, DEPTH_max = 0, Use_transposition = False):
        self.DEPTH = DEPTH_max
        self.Counter = 0
        self.Use_transposition = Use_transposition
        self.Transposition_table = Transposition_table
        self.Accessed_table_counter = 0
    def Get_all_moves(self, Board_fen):
        pass
    def Point_fn(self, string, index):
        name = string.lower()
        if name in PIECES:
            if string.islower():
                index = 63 - index
            return (PIECES[name]+PIECE_SPACE[name][index]) * (-1 if string.islower() else 1)
        else:
            return 0
        
    def Evaluate(self, Board_fen:str):
        point = 0
        offset = 0
        for ind, case in enumerate(Board_fen.split(' ')[0]):
            if case.isnumeric():
                offset=int(case)
            elif case == "/":
                offset=0
            point += self.Point_fn(case, index=ind + offset)
        return point

    def Exploration(self, board:object, Depth):
        
        global Counter_min_max, Counter_alpha_beta
        Counter_min_max, Counter_alpha_beta = 0, 0
        
        self.DEPTH_MAX = Depth
        min_max = False
        if min_max:
            move_min_max, point_min_max = self.Exploration_min_max(board, Depth)
            point_min_max = point_min_max *(-1 if not board.turn else 1)
        
        alpha = -CHECKMATE
        beta = CHECKMATE
        move_alpha_beta, point_alpha_beta = self.Exploration_alpha_beta(board, Depth, alpha, beta)
        point_alpha_beta = point_alpha_beta *(-1 if not board.turn else 1)
        
        #print(f'Min max:\nAfter : {Counter_min_max} branches, Scores : {point_min_max}, Bestmove : {move_min_max}')
        print(f'Alpha beta:\nAfter : {Counter_alpha_beta} branches, Scores : {point_alpha_beta}, Bestmove : {move_alpha_beta}')
        #input()
        return move_alpha_beta, point_alpha_beta
    
    def Exploration_min_max(self, board:object, Depth):
        global Counter_min_max
        Counter_min_max+=1
        if board.is_fivefold_repetition():
            return -1, 0
        if board.is_insufficient_material():
            return -1, 0
        
        if self.Use_transposition:
            fen = board.fen()
            extract = (" ").join(fen.split(' ')[0:2])
            if extract in Transposition_table:
                if Transposition_table[extract][2]+1 >= Depth:
                    self.Accessed_table_counter +=1
                    return Transposition_table[extract][0], -Transposition_table[extract][1]
        
        if Depth == 0:
            return None,  self.Evaluate(board.fen())
        
        #print(board)
        #print(list(board.generate_legal_moves()))
        All_moves = list(board.generate_legal_moves())
        random.shuffle(All_moves)
        Move_points = []
        Max_score = -CHECKMATE
        for move in All_moves:
            board.push(move)
            mv, Point = self.Exploration_min_max(board, Depth -1)
            flag = 1
            if Depth != 1 or (Depth == 1 and board.turn):
                flag = -1
                Point= Point * (-1)
            board.pop()
            Move_points.append(Point)

            if Point > Max_score:
                Max_score = Point
                Best_move = move
        
        if len(Move_points) == 0:
            if board.outcome().winner == True:
                return -1, -CHECKMATE
            elif board.outcome().winner == False:
                return -1, CHECKMATE
            return -1, 0
        
        #if Depth == self.DEPTH_MAX:
        #    print(f'For depth = {Depth} {board.turn} {flag}\nAll moves : {All_moves}\nAll scores : {Move_points}' )
        #    input()
            
        #if Depth != 0:
        #    print(f'For depth = {Depth} {board.turn} {not board.turn} {flag}\nAll moves : {All_moves}\nAll scores : {Move_points}' )
        #    input()
#        if board.turn:
#            mask = np.array(Move_points) == max(Move_points)
#        else:
#            mask = np.array(Move_points) == min(Move_points)

#        selected_moves = np.array(All_moves)[mask]
#        Best_move = np.random.choice(selected_moves)
        
        if self.Use_transposition:
            if not extract in Transposition_table:
                Transposition_table[extract] = (Best_move, Max_score, Depth)
            elif extract in Transposition_table:
                if Transposition_table[extract][2] <= Depth:
                    Transposition_table[extract] = (Best_move, Max_score, Depth)
        return Best_move, Max_score 
    
    def Exploration_alpha_beta(self, board:object, Depth, alpha, beta):
        global Counter_alpha_beta
        Counter_alpha_beta+=1
        if board.is_fivefold_repetition():
            return -1, 0
        if board.is_insufficient_material():
            return -1, 0
        
        if self.Use_transposition:
            fen = board.fen()
            extract = (" ").join(fen.split(' ')[0:2])
            if extract in Transposition_table:
                if Transposition_table[extract][2]+1 >= Depth:
                    self.Accessed_table_counter +=1
                    return Transposition_table[extract][0], -Transposition_table[extract][1]
        
        if Depth == 0:
            return None,  self.Evaluate(board.fen())
        
        #print(board)
        #print(list(board.generate_legal_moves()))
        All_moves = list(board.generate_legal_moves())
        random.shuffle(All_moves)
        Move_points = []
        Max_score = -CHECKMATE
        if len(All_moves)!=0:
            Best_move = All_moves[0]
        for move in All_moves:
            board.push(move)
            mv, Point = self.Exploration_alpha_beta(board, Depth -1, -beta, -alpha)
            flag = 1
            if Depth != 1 or (Depth == 1 and board.turn):
                flag = -1
                Point= Point * (-1)
            board.pop()
            Move_points.append(Point)

            if Point >= Max_score:
                Max_score = Point
                Best_move = move
                
            if Max_score > alpha:
                alpha = Max_score
            if alpha >= beta:
                break
            
        if len(Move_points) == 0:
            if board.outcome().winner == True:
                return -1, -CHECKMATE
            elif board.outcome().winner == False:
                return -1, CHECKMATE
            return -1, 0
        
        #if Depth == self.DEPTH_MAX:
        #    print(f'For depth = {Depth} {board.turn} {flag}\nAll moves : {All_moves}\nAll scores : {Move_points}' )
        #    input()
            
        #if Depth != 0:
        #    print(f'For depth = {Depth} {board.turn} {not board.turn} {flag}\nAll moves : {All_moves}\nAll scores : {Move_points}' )
        #    input()
#        if board.turn:
#            mask = np.array(Move_points) == max(Move_points)
#        else:
#            mask = np.array(Move_points) == min(Move_points)

#        selected_moves = np.array(All_moves)[mask]
#        Best_move = np.random.choice(selected_moves)
        
        if self.Use_transposition:
            if not extract in Transposition_table:
                Transposition_table[extract] = (Best_move, Max_score, Depth)
            elif extract in Transposition_table:
                if Transposition_table[extract][2] <= Depth:
                    Transposition_table[extract] = (Best_move, Max_score, Depth)
        return Best_move, Max_score 