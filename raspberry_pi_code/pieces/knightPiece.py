import chessPiece

class Knight(chessPiece):

    CHESS_PIECE_TYPE = "N"
    CHESS_PIECE_VALUE = 300

    #initalize piece
    def __init__(self, x_pos, y_pos, piece_color):
        super(Knight, self).__init__(x_pos, y_pos, piece_color, Knight.CHESS_PIECE_TYPE, Knight.CHESS_PIECE_VALUE)

    #get legal moves
    def get_legal_chess_piece_moves(self, board):
        chess_piece_moves = []

        #move directions
        move_directions = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]

        #add to list
        for dx, dy in move_directions:
            chess_piece_moves.append(self.get_move(board, self.x_pos + dx, self.y_pos + dy))

        return self.remove_null_from_list(chess_piece_moves)

    #duplicate self
    def duplicate(self):
        return Knight(self.x_pos, self.y_pos, self.piece_color)
    