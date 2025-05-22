import pawnPiece, knightPiece, bishopPiece, rookPiece, queenPiece, kingPiece
import ai.ai
from pieceMove import PieceMove

class ChessPiece:
    
    CHESS_PIECE_WHITE = "W"
    CHESS_PIECE_BLACK = "B"

    #initalize peice
    def __init__(self, x_pos, y_pos, piece_color, piece_type, piece_value):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.piece_color = piece_color
        self.piece_type = piece_type
        self.piece_value = piece_value

    #get legal mvoes
    def get_legal_moves(self, chessBoard):
        moves = []
        if self.piece_type in ["Bishop", "Queen"]:
            moves.extend(self.get_diagonal_moves(chessBoard))
        if self.piece_type in ["Rook", "Queen"]:
            moves.extend(self.get_horizontal_moves(chessBoard))
        return self.remove_invalid_moves(moves)

    #get diagonal moves
    def get_diagonal_moves(self, chessBoard):
        diagonal_moves = []
        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        for dx, dy in directions:
            for i in range(1, 8):
                x, y = self.x_pos + dx * i, self.y_pos + dy * i
                if not chessBoard.in_bounds(x, y): break
                piece = chessBoard.get_piece(x, y)
                move = self.get_move(chessBoard, x, y)
                if move: diagonal_moves.append(move)
                if piece: break
        return diagonal_moves

    #get hotizontal moves
    def get_horizontal_moves(self, chessBoard):
        horizontal_moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            for i in range(1, 8):
                x, y = self.x_pos + dx * i, self.y_pos + dy * i
                if not chessBoard.in_bounds(x, y): break
                piece = chessBoard.get_piece(x, y)
                move = self.get_move(chessBoard, x, y)
                if move: horizontal_moves.append(move)
                if piece: break
        return horizontal_moves

    #get move
    def get_move(self, chessBoard, xto, yto):
        if chessBoard.in_bounds(xto, yto):
            piece = chessBoard.get_piece(xto, yto)
            if piece == 0 or piece.piece_color != self.piece_color:
                return PieceMove(self.x_pos, self.y_pos, xto, yto)
        return 0

    #remove illegal mnoves
    def remove_illegal_moves(self, moves):
        return [move for move in moves if move != 0]