import chessPiece

class Bishop(chessPiece):

    CHESS_PIECE_TYPE = "B"
    CHESS_PIECE_VALUE = 300

    #initalize piece
    def __init__(self, x_pos, y_pos, piece_color):
        super(Bishop, self).__init__(x_pos, y_pos, piece_color, Bishop.CHESS_PIECE_TYPE, Bishop.CHESS_PIECE_VALUE)

    #get legal moves
    def get_legal_chess_piece_moves(self, board):

        #get diagonal moves
        return self.get_legal_diagonal_chess_piece_moves(board)

    #initalize duplicate self
    def duplicate(self):
        return Bishop(self.x_pos, self.y_pos, self.piece_color)
