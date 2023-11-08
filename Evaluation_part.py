from ChessBoard import Chess_t
import numpy as np
import time
Chess = Chess_t()
PIECES = {'q' : 900, 'r' : 500, 'b' : 400, 'n' : 400, 'p' : 100}

class Bot():
    def __init__(self):
        self.DEPTH = 0
    def Get_all_moves(self, Board, Turn):
        Poss_Moves = []
        All_Pieces = np.where(np.char.islower(Board) if Turn == 'Black'
                              else np.char.isupper(Board))
        for x,y in zip(All_Pieces[1], All_Pieces[0]):
            Poss_Moves.extend(Chess.Get_possible_moves(Board, x, y))
        All_moves = Chess.Moves_verify(Board, Poss_Moves, Turn)
        return All_moves
    
    def Point_fn(self, string):
        if string.lower() in PIECES:
            return PIECES[string.lower()] * (-1 if string.islower() else 1)
        else:
            return 0
        
    def Change_tour(self, Turn):
        if Turn == 'White':
            return 'Black'
        else:
            return 'White'
        
    def Evaluate(self, Board, Turn):
        Board2 = Board.flatten()
        point = 0
        for case in Board2:
            point += self.Point_fn(case)
        return point
    
    def Exploration(self, Board, Turn, Depth):
        if self.DEPTH == 0:
            self.DEPTH = Depth
        if Depth == self.DEPTH:
            Start = time.time()
            self.Counter = 0
        if Depth == 0:
            self.Counter += 1
            return self.Evaluate(Board, Turn)
        Moves = np.array(self.Get_all_moves(Board, Turn))
        # Choice = np.random.choice(Moves)
        # print(Choice)
        Point = np.array([])
        for move in Moves:
            Board2 = Chess.Move_to(Board, move)
            Point = np.append(Point,self.Exploration(Board2, self.Change_tour(Turn), Depth - 1))
        
        if Depth != self.DEPTH:
            if len(Point) == 0:
                if Chess.Check_for_check(Board, Turn, 'NO'):
                    return 9999 * (-1 if Turn == 'White' else 1)
                else:
                    return 0
            else:
                if Turn == 'White':
                    return max(Point)
                else:
                    return min(Point)
        else:
            Time_taken = time.time() - Start
            self.DEPTH = 0
            if len(Point) == 0:
                print(str(Turn) + ' lost')
                return None, None, None
            if Turn == 'White':
                Mask = Point == max(Point)
            else:
                Mask = Point == min(Point)
            
            Best_moves = Moves[Mask]
            Choice = np.random.choice(Best_moves)
            return Choice, self.Counter, Time_taken