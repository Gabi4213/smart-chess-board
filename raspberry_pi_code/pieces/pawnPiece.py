import chessPiece

class Pawn(chessPiece):

    CHESS_PIECE_TYPE = "P"
    CHESS_PIECE_VALUE = 100

    #initalize piece    
    def __init__(self, x_pos, y_pos, piece_color):
        super(Pawn, self).__init__(x_pos, y_pos, piece_color, Pawn.CHESS_PIECE_TYPE, Pawn.CHESS_PIECE_VALUE)

    #get starting pos
    def get_starting_position(self):
        if (self.piece_color == chessPiece.CHESS_PIECE_BLACK):
            return self.y_pos == 1
        else:
            return self.y_pos == 6

    #get legal moves
    def get_legal_chess_piece_moves(self, board):
        chess_piece_moves = []

        #move direction
        move_direction = -1
        if (self.piece_color == chessPiece.CHESS_PIECE_BLACK):
            move_direction = 1

        #move forward once
        if (board.get_piece(self.x_pos, self.y_pos+move_direction) == 0):
            chess_piece_moves.append(self.get_move(board, self.x_pos, self.y_pos + move_direction))

        #mvoe forward twice
        if (self.get_starting_position() and board.get_piece(self.x_pos, self.y_pos+ move_direction) == 0 and board.get_piece(self.x_pos, self.y_pos + move_direction*2) == 0):
            chess_piece_moves.append(self.get_move(board, self.x_pos, self.y_pos + move_direction * 2))

        #capture pieces
        piece = board.get_piece(self.x_pos + 1, self.y_pos + move_direction)
        if (piece != 0):
            chess_piece_moves.append(self.get_move(board, self.x_pos + 1, self.y_pos + move_direction))

        piece = board.get_piece(self.x_pos - 1, self.y_pos + move_direction)
        if (piece != 0):
            chess_piece_moves.append(self.get_move(board, self.x_pos - 1, self.y_pos + move_direction))

        return self.remove_null_from_list(chess_piece_moves)

    #duplicate self
    def duplicate(self):
        return Pawn(self.x_pos, self.y_pos, self.piece_color)
