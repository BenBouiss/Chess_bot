import numpy as np
from random import randint
import time

class Chess_t():  
    def __init__(self):
        self.White_inv = []
        self.Black_inv = []
        self.Letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.Prom = ['q', 'b', 'r', 'n']
        self.Selection = []
        self.Selected = (0,0)
        self.Poss_move = []
        self.Target = None
        
        self.Init_Board = np.array([['-','-','-','-','-','-','-','-',],
             ['-','-','-','-','-','-','-','-',],
             ['-','-','-','-','-','-','-','-',],
             ['-','-','-','-','-','-','-','-',],
             ['-','-','-','-','-','-','-','-',],
             ['-','-','-','-','-','-','-','-',],
             ['-','-','-','-','-','-','-','-',],
             ['-','-','-','-','-','-','-','-',],
             ])
    
    def decode(self):
        code = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        Caract = code.split('/')
        for Row, i in reversed(list(enumerate(Caract))):
            offset = 0
            for Col, j in enumerate(i):
                if j.isdigit():
                    offset = int(j) - 1
                else:
                    self.Init_Board[Row][Col+offset] = j
                    
    def Get_couleur(self, string):
        if string.islower():
            return 'Black'
        else:
            return 'White'
        
        
    def Moves_to_string(self, pos1, pos2, type1, type2):
        init = type1 + self.Letter[pos1[0]] + str(pos1[1])
        fin = type2 + self.Letter[pos2[0]] + str(pos2[1])
        return init + fin
    
    def Moves_promo_to_string(self, pos1, pos2, type1, type2, Choix):
        init = type1 + self.Letter[pos1[0]] + str(pos1[1])
        fin = type2 + self.Letter[pos2[0]] + str(pos2[1])
        return init + fin + '=' + Choix
    
    def String_to_position(self, string):
        if len(string) == 6 or len(string) == 8:
            x1 = self.Letter.index(string[1])
            y1 = int(string[2])
            x2 = self.Letter.index(string[4])
            y2 = int(string[5])
            return (x1,y1), (x2,y2)
    
    
    def Move_to(self, Board, string):
        pos1, pos2 = self.String_to_position(string)
        Board2 = np.array(Board)
        Board2[pos1[1]][pos1[0]] = '-'
        if len(string) == 6:
            Board2[pos2[1]][pos2[0]] = string[0]
        else:
            Board2[pos2[1]][pos2[0]] = string[7]
        return Board2
    
    
    def Get_possible_moves(self, Board, x, y):
        Piece = Board[y][x]
        Coord = (x,y)
        Couleur = self.Get_couleur(Piece)
        if Piece.lower() == 'p':
            Possible_moves = self.Get_Pawn_Moves(Piece, Coord, Board, Couleur)
            
        if Piece.lower() == 'n':
            Possible_moves = self.Get_Knight_Moves(Piece, Coord, Board, Couleur)  
            
        if Piece.lower() == 'b':
            Possible_moves = self.Get_Bishop_Moves(Piece, Coord, Board, Couleur)
            
        if Piece.lower() == 'r':
            Possible_moves = self.Get_Rook_Moves(Piece, Coord, Board, Couleur)
            
        if Piece.lower() == 'q':
            Possible_moves = self.Get_Rook_Moves(Piece, Coord, Board, Couleur)
            Possible_moves.extend(self.Get_Bishop_Moves(Piece, Coord, Board, Couleur))
            
        if Piece.lower() == 'k':
            Possible_moves = self.Get_King_Moves(Piece, Coord, Board, Couleur)
            
        return Possible_moves
            
            
    def Generate_promo_moves(self, Piece, Board, x, y, Target, xt, yt):
        Move = []
        
        for i in self.Prom:
            if Piece.isupper():
                Prom = i.upper()
            else:
                Prom = i
            Move.append(self.Moves_promo_to_string((x, y),(xt, yt), Piece, Target, Prom))
        return Move
            
    def Get_Pawn_Moves(self, Piece, Coord, Board, Couleur):
        x, y = Coord
        Poss_moves = []
        
        Target_pos = y + (1 if Couleur == 'Black' else -1)
        if Target_pos < 7 and Target_pos>=1: ##Y Upper/lower boundaries
            if Board[Target_pos][x] == '-':
                Target = Board[Target_pos][x]
                Poss_moves.append(self.Moves_to_string(Coord, (x, Target_pos), Piece,
                                                  Target))
        if (Target_pos == 7 or Target_pos == 0):
            if Board[Target_pos][x] == '-':
                Poss_moves.extend(self.Generate_promo_moves(Piece, Board, x, y, 
                '-', x, Target_pos))
        
        if ((y == 1 and Couleur == 'Black' and Board[y + 2][x] == '-' and Board[y + 1][x] == '-') 
            or (y == 6 and Couleur == 'White' and Board[y - 2][x] == '-' and Board[y - 1][x] == '-')):
            
            Target_pos = y + (2 if Couleur == 'Black' else -2)
            Poss_moves.append(self.Moves_to_string(Coord, (x, Target_pos), Piece, 
                                              '-'))
            
        for i in range(2):
            if (0 <= y + (1 if Couleur == 'Black' else -1)<8) and (0<= x + (1 if i==0 else -1) <8):
                Target = Board[y + (1 if Couleur == 'Black' else -1)][x + (1 if i==0 else -1)]
                if Target != '-' and Couleur != self.Get_couleur(Target):
                    x_target = x + (1 if i==0 else -1)
                    y_target = y + (1 if Couleur == 'Black' else -1)
                    if y_target == 7 or y_target == 0:
                        Poss_moves.extend(self.Generate_promo_moves(Piece, Board, x, y, 
                            Target, x_target, y_target))
                    else:
                        Poss_moves.append(self.Moves_to_string(Coord, (x_target, y_target),
                                     Piece, Target))
        
        return Poss_moves
        
    def Get_Knight_Moves(self, Piece, Coord, Board, Couleur):
        x,y = Coord
        poss = [1, 2, 2, 1]
        Poss_moves = []
        for i in range(8):
            sensx = 1 if 0<= i <4 else -1
            sensy = -1 if 2<= i <6 else 1
            dx,dy = sensx * poss[i%4], sensy * poss[(i+2)%4]
            if -1< x + dx < 8 and -1< y + dy < 8 :
                Target = Board[dy + y][dx + x]
                if Target == '-' or self.Get_couleur(Target) != Couleur:
                    Poss_moves.append(self.Moves_to_string(Coord, (x+dx, y+dy),
                    Piece, Target))
        return Poss_moves
    
    
    def Get_King_Moves(self, Piece, Coord, Board, Couleur):
        x, y = Coord
        Cut = Board[y-1 if y!=0 else 0 :y+2,x-1 if x!=0 else 0:x+2]
        King = np.where(Cut == Piece)
        x_k, y_k = King[1], King[0]
        if Couleur == 'White':
            Tot = np.where(((Cut == '-') | (np.char.islower(Cut))))
        else:
            Tot = np.where(((Cut == '-') | (np.char.isupper(Cut))))
        Poss_moves = []
        for x1,y1 in zip(Tot[1], Tot[0]):
            dx, dy = x1 - x_k, y1 - y_k
            Target = Board[y+dy, x+dx]
            Poss_moves.append(self.Moves_to_string(Coord, (x+dx[0], y+dy[0]),
            Piece, Target[0]))
        return Poss_moves
        
    def Get_Bishop_Moves(self, Piece, Coord, Board, Couleur):
        x, y = Coord
        dxs = [1, 1, -1, -1]
        dys = [-1, 1, 1, -1]
        Poss_moves = []
        for dx, dy in zip(dxs, dys):
            while (0<= x + dx < 8) and (0<= y + dy < 8):
                Target = Board[y + dy, x + dx]
                if  Target == '-':
                    Poss_moves.append(self.Moves_to_string(Coord, (x+dx, y+dy),
                    Piece, Target))
                    dx+= 1 if dx>0 else -1
                    dy+= 1 if dy>0 else -1
                elif self.Get_couleur(Target) != Couleur:
                    Poss_moves.append(self.Moves_to_string(Coord, (x+dx, y+dy),
                    Piece, Target))
                    break
                else:
                    break
        return Poss_moves
    
    def Get_Rook_Moves(self, Piece, Coord, Board, Couleur):
        x, y = Coord
        dxs = [1, 0, -1, 0]
        dys = [0, 1, 0, -1]
        Poss_moves = []
        for dx, dy in zip(dxs, dys):
            while (0<= x + dx < 8) and (0<= y + dy < 8):
                Target = Board[y + dy, x + dx]
                if  Target == '-':
                    Poss_moves.append(self.Moves_to_string(Coord, (x+dx, y+dy),
                    Piece, Target))
                    dx+= 1 * (dx>0) - 1*(dx<0)
                    dy+= 1 * (dy>0) - 1*(dy<0)
                elif self.Get_couleur(Target) != Couleur:
                    Poss_moves.append(self.Moves_to_string(Coord, (x+dx, y+dy),
                    Piece, Target))
                    break
                else:
                    break
        return Poss_moves
        
    def Moves_verify(self, Board, Moves, Turn):
        Moves2 = list(Moves)
        for Move in Moves:
            Board2 = self.Move_to(Board, Move)
            Target_king = np.where(Board2 == ('K' if Turn == 'White' else 'k'))
            x_k, y_k = Target_king[1], Target_king[0]
            if (not self.Verify_Diagonales(Board2, (x_k, y_k), Turn) or
                not self.Verify_Horiz(Board2, (x_k, y_k), Turn) or
                not self.Verify_Horse(Board2, (x_k, y_k), Turn)):
                Moves2.remove(Move)
        return Moves2
    
    def Verify_Diagonales(self, Board, Coord_k, Couleur):
        x, y = Coord_k
        dxs = [1, 1, -1, -1]
        dys = [-1, 1, 1, -1]
        for dx, dy in zip(dxs, dys):
            while (0<= x + dx < 8) and (0<= y + dy < 8):
                Target = Board[y + dy, x + dx][0]
                if  Target == '-':
                    dx+= 1 if dx>0 else -1
                    dy+= 1 if dy>0 else -1
                elif self.Get_couleur(Target) != Couleur and ((
                        Target.lower() == 'b' or Target.lower() == 'q') 
                        or ((Target == 'p' or Target.lower() == 'k') and dy == -1) or 
                        ((Target == 'P' or Target.lower() == 'k') and dy == 1)):
                    return False
                else:
                    break
        return True
    def Verify_Horiz(self, Board, Coord_k, Couleur):
        x, y = Coord_k
        dxs = [1, 0, -1, 0]
        dys = [0, 1, 0, -1]
        for dx, dy in zip(dxs, dys):
            while (0<= x + dx < 8) and (0<= y + dy < 8):
                Target = Board[y + dy, x + dx][0]
                # print(Target, (dx, dy), Couleur, self.Get_couleur(Target))
                if  Target == '-':
                    dx+= 1 * (dx>0) - 1*(dx<0)
                    dy+= 1 * (dy>0) - 1*(dy<0)
                elif Target.lower() == 'k':
                    if (self.Get_couleur(Target) != Couleur and np.power(dx + dy, 2) == 1):
                        return False
                    else:
                        break
                elif self.Get_couleur(Target) != Couleur and (Target.lower() == 'q' or Target.lower() == 'r'): 
                    return False

                else:
                    break
        return True
    
    def Verify_Horse(self, Board, Coord_k, Couleur):
        x, y = Coord_k
        if Couleur == 'White':
            Horses = np.where(Board == 'n')
        else: 
            Horses = np.where(Board == 'N')
        if len(Horses) == 2:
            for xh, yh in zip(Horses[1], Horses[0]):
                if ((abs(xh - x) == 2 and abs(yh - y) == 1) or (abs(xh - x) == 1 and abs(yh - y) == 2)):
                    return False
        return True
    
    
    def Check_for_check(self, Board, Turn, Indic = 'YES'):
        Target_king = np.where(Board == ('K' if Turn == 'White' else 'k'))
        x_k, y_k = Target_king[1], Target_king[0]
        if (not self.Verify_Diagonales(Board, (x_k, y_k), Turn) or
                not self.Verify_Horiz(Board, (x_k, y_k), Turn) or
                not self.Verify_Horse(Board, (x_k, y_k), Turn)):
                if 'YES':
                    print('Check')
                return True
        return False
    
    def Check_for_mate(self, Board, Turn):
        Poss_Moves = []
        All_Pieces = np.where(np.char.islower(Board) if Turn == 'Black'
                              else np.char.isupper(Board))
        for x,y in zip(All_Pieces[1], All_Pieces[0]):
            Poss_Moves.extend(self.Get_possible_moves(Board, x, y))
        All_moves = self.Moves_verify(Board, Poss_Moves, Turn)
        if All_moves == [] and self.Check_for_check(Board, Turn):
            print('Mate')
            return True
        return False
    
    def Check_for_draw(self, Board):
        if len(np.where(np.char.islower(Board))[0]) == 1 and len(np.where(np.char.isupper(Board))[0]) == 1:
            return True
        else:
            return False