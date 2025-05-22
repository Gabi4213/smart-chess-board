import chessPiece

class Queen(chessPiece):

    CHESS_PIECE_TYPE = "Q"
    CHESS_PIECE_VALUE = 900

    #initalize film
    def __init__(self, x_pos, y_pos, piece_color):
        super(Queen, self).__init__(x_pos, y_pos, piece_color, Queen.CHESS_PIECE_TYPE, Queen.CHESS_PIECE_VALUE)

    #get legal moves
    def get_legal_chess_piece_moves(self, board):

        #queen is diagonal adn horizontal
        diagonal = self.get_legal_diagonal_chess_piece_moves(board)
        horizontal = self.get_legal_horizontal_chess_piece_moves(board)
        
        return horizontal + diagonal

    #duplicate self
    def duplicate(self):
        return Queen(self.x_pos, self.y_pos, self.piece_color)
