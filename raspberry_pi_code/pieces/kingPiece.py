import chessPiece
import pieceMove
import rookPiece

class King(chessPiece):

    CHESS_PIECE_TYPE = "K"
    CHESS_PIECE_VALUE = 20000

    #initalize piece
    def __init__(self, x_pos, y_pos, piece_color):
        super().__init__(x_pos, y_pos, piece_color, King.CHESS_PIECE_TYPE, King.CHESS_PIECE_VALUE)

    #get legal moves
    def get_legal_chess_piece_moves(self, board):
        chess_piece_moves = []

        #move directions
        move_directions = [
            (1, 0), (1, 1), (0, 1), (-1, 1),
            (-1, 0), (-1, -1), (0, -1), (1, -1)
        ]
        
        #add to list
        for dx, dy in move_directions:
            chess_piece_moves.append(self.get_move(board, self.x_pos + dx, self.y_pos + dy))

        #castling moves

        #kingside
        chess_piece_moves.append(self.get_castle_move(board, 1))

        #queenside
        chess_piece_moves.append(self.get_castle_move(board, -1))

        return self.remove_null_from_list(chess_piece_moves)

    def get_castle_move(self, board, direction):

        #get rook position
        rook_offset = 3 if direction == 1 else -4
        piece_in_corner = board.get_piece(self.x_pos + rook_offset, self.y_pos)

        #check if rook is not captured and valid
        if piece_in_corner == 0 or piece_in_corner.CHESS_PIECE_TYPE != rookPiece.CHESS_PIECE_TYPE:
            return None

        #check rook color
        if piece_in_corner.piece_color != self.piece_color:
            return None

        #make sure king hasn't moved
        if (self.piece_color == chessPiece.CHESS_PIECE_WHITE and board.CHESS_PIECE_WHITE_king_moved) or \
           (self.piece_color == chessPiece.CHESS_PIECE_BLACK and board.CHESS_PIECE_BLACK_king_moved):
            return None

        #check if there is a piece between the king and rook
        range_check = range(1, 3) if direction == 1 else range(-1, -4, -1)
        for i in range_check:
            if board.get_piece(self.x_pos + i, self.y_pos) != 0:
                return None

        return pieceMove(self.x_pos, self.y_pos, self.x_pos + (2 * direction), self.y_pos)

    #duplicate self
    def duplicate(self):
        return King(self.x_pos, self.y_pos, self.piece_color)
