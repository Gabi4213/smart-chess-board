import chessPiece

class Rook(chessPiece):

    CHESS_PIECE_TYPE = "R"
    CHESS_PIECE_VALUE = 500

    #initalize piece
    def __init__(self, x_pos, y_pos, piece_color):
        super(Rook, self).__init__(x_pos, y_pos, piece_color, Rook.CHESS_PIECE_TYPE, Rook.CHESS_PIECE_VALUE)

    #get legal moves
    def get_legal_chess_piece_moves(self, board):

        #horizontal moves
        return self.get_legal_horizontal_chess_piece_moves(board)

    #duplicate self
    def duplicate(self):
        return Rook(self.x_pos, self.y_pos, self.piece_color)