import Evaluation_part
import chess
import time
import os
from stockfish import Stockfish

clear = lambda: os.system('clear')
#stockfish = Stockfish(path=f"{os.getcwd()}/Stockfish/stockfish/src/stockfish")
path=f"{os.getcwd()}/Stockfish/stockfish/src/stockfish"
print(os.getcwd())
stockfish = Stockfish(path = path)



fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0"
bot = Evaluation_part.Bot(DEPTH_max=4, Use_transposition = True)
#bot.Exploration(Board_fen=fen, Depth = 2)
board = chess.Board(fen)

Testing = True
running = True
depth = 2
min_depth = 3
MAX_DEPTH = 8

while running:
    Start = time.time()
    move, point = bot.Exploration(board=board, Depth = depth)
    print(f'Score : {point}, turn : {board.turn}')
    #point = point *(-1 if not board.turn else 1)
    if time.time() - Start < 1:
        depth = min(depth+1, MAX_DEPTH)
    else:
        depth = max(min_depth, depth-1)
    if move == None:
        running = False
        break
    if type(move) == int:
        running = False
    else:
        board.push(move)
    #clear()
    stockfish.set_fen_position(board.fen())
    stockfish_valid = stockfish.get_evaluation()['value']
    os.system('clear')
    print(f"Choice : {move} with estimation of : {point*-1 if not board.turn else 1}, after : {round(time.time() - Start, 2)} s at depth = {depth}")
    print(board.turn)
    print(f"Stockfish estimation : {stockfish_valid}")
    print(board)
    print(f'Cached positions : {len(Evaluation_part.Transposition_table)}')
    print(f'Number of cached positions accessed : {bot.Accessed_table_counter}')