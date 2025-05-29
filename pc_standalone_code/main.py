import chessBoard 
import chessPieces
import chessAI
from pieceMove import PieceMove

# convert character to x pos
def letter_to_xpos(letter):
    letter = letter.upper()
    if letter == 'A':
        return 0
    if letter == 'B':
        return 1
    if letter == 'C':
        return 2
    if letter == 'D':
        return 3
    if letter == 'E':
        return 4
    if letter == 'F':
        return 5
    if letter == 'G':
        return 6
    if letter == 'H':
        return 7
    raise ValueError("error enter a valid letter")

#convert x ppos back to character
def xpos_to_letter(x):
    return chr(ord('a') + x)

#take user input and return the move
def get_user_move():
    move_str = input("enter a move: ")
    move_str = move_str.replace(" ", "")
    try:
        xfrom = letter_to_xpos(move_str[0:1])
        yfrom = 8 - int(move_str[1:2])
        xto = letter_to_xpos(move_str[2:3])
        yto = 8 - int(move_str[3:4])
        return PieceMove(xfrom, yfrom, xto, yto)
    except ValueError:
        print("invalid format")
        return get_user_move()

#check if user move is legal
def is_user_move_legal(board):
    while True:
        move = get_user_move()
        valid = False
        possible_moves = board.get_legal_moves(chessPieces.ChessPiece.CHESS_PIECE_WHITE)
        if not possible_moves:
            return 0
        for possible_move in possible_moves:
            if move.is_tile_equal(possible_move):
                valid = True
                break
        if valid:
            break
        else:
            print("illegal move")
    return move

#convert to format like w2w4
def move_to_output_string(move):
    return f"{xpos_to_letter(move.xfrom)}{8 - move.yfrom}{xpos_to_letter(move.xto)}{8 - move.yto}"

#create the chessboard from fen
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
chessBoard = chessBoard.Board.from_fen(fen)

while True:
    move = is_user_move_legal(chessBoard)
    if move == 0:
        if chessBoard.is_check(chessPieces.ChessPiece.CHESS_PIECE_WHITE):
            print("checkmate black wins")
        else:
            print("stalemate")
        break

    chessBoard.make_move(move)

    ai_move = chessAI.ChessAI.get_ai_move(chessBoard, [])
    if ai_move == 0:
        if chessBoard.is_check(chessPieces.ChessPiece.CHESS_PIECE_BLACK):
            print("checkmate white wins")
        else:
            print("stalemate.")
        break

    chessBoard.make_move(ai_move)
    print("ai move:", move_to_output_string(ai_move))
