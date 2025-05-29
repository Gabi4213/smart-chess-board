import chessAI
from pieceMove import PieceMove

class ChessPiece():

    CHESS_PIECE_WHITE = "W"
    CHESS_PIECE_BLACK = "B"

    #initalize peice
    def __init__(self, x_pos, y_pos, piece_color, CHESS_PIECE_TYPE, piece_CHESS_PIECE_VALUE):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.piece_color = piece_color
        self.CHESS_PIECE_TYPE = CHESS_PIECE_TYPE
        self.piece_CHESS_PIECE_VALUE = piece_CHESS_PIECE_VALUE

    #get legal mvoes
    def get_legal_moves(self, chessBoard):
        moves = []
        if self.CHESS_PIECE_TYPE in ["Bishop", "Queen"]:
            moves.extend(self.get_diagonal_moves(chessBoard))
        if self.CHESS_PIECE_TYPE in ["Rook", "Queen"]:
            moves.extend(self.get_horizontal_moves(chessBoard))
        return self.remove_illegal_moves(moves)

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


class Pawn(ChessPiece):

    CHESS_PIECE_TYPE = "P"
    CHESS_PIECE_VALUE = 100

    def __init__(self, x_pos, y_pos, piece_color):
        super(Pawn, self).__init__(x_pos, y_pos, piece_color, Pawn.CHESS_PIECE_TYPE, Pawn.CHESS_PIECE_VALUE)

    #get starting pos
    def get_starting_position(self):
        if (self.piece_color == ChessPiece.CHESS_PIECE_BLACK):
            return self.y_pos == 1
        else:
            return self.y_pos == 6

    def get_legal_moves(self, board):
     moves = []

     #move direction
     direction = 1 if self.piece_color == ChessPiece.CHESS_PIECE_BLACK else -1

     #move forward once
     if board.get_piece(self.x_pos, self.y_pos + direction) == 0:
         moves.append(self.get_move(board, self.x_pos, self.y_pos + direction))

         #mvoe forward twice
         if self.get_starting_position() and board.get_piece(self.x_pos, self.y_pos + 2 * direction) == 0:
             moves.append(self.get_move(board, self.x_pos, self.y_pos + 2 * direction))

     #capture pieces - right
     right_piece = board.get_piece(self.x_pos + 1, self.y_pos + direction)
     if right_piece != 0:
         moves.append(self.get_move(board, self.x_pos + 1, self.y_pos + direction))

     #capture pieces - left
     left_piece = board.get_piece(self.x_pos - 1, self.y_pos + direction)
     if left_piece != 0:
         moves.append(self.get_move(board, self.x_pos - 1, self.y_pos + direction))

     return self.remove_illegal_moves(moves)

    
    #duplicate self
    def duplicate(self):
        return Pawn(self.x_pos, self.y_pos, self.piece_color)

class Knight(ChessPiece):

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

        return self.remove_illegal_moves(chess_piece_moves)

    #duplicate self
    def duplicate(self):
        return Knight(self.x_pos, self.y_pos, self.piece_color)

class Bishop(ChessPiece):

    CHESS_PIECE_TYPE = "B"
    CHESS_PIECE_VALUE = 300

    #initalize piece
    def __init__(self, x_pos, y_pos, piece_color):
        super(Bishop, self).__init__(x_pos, y_pos, piece_color, Bishop.CHESS_PIECE_TYPE, Bishop.CHESS_PIECE_VALUE)

    #get legal moves
    def get_legal_chess_piece_moves(self, board):

        #get diagonal moves
        return self.get_diagonal_moves(board)

    #initalize duplicate self
    def duplicate(self):
        return Bishop(self.x_pos, self.y_pos, self.piece_color)

class Rook(ChessPiece):

    CHESS_PIECE_TYPE = "R"
    CHESS_PIECE_VALUE = 500

    #initalize piece
    def __init__(self, x_pos, y_pos, piece_color):
        super(Rook, self).__init__(x_pos, y_pos, piece_color, Rook.CHESS_PIECE_TYPE, Rook.CHESS_PIECE_VALUE)
   
    #get legal moves
    def get_legal_chess_piece_moves(self, board):

        #horizontal moves
        return self.get_horizontal_moves(board)

    def duplicate(self):
        return Rook(self.x_pos, self.y_pos, self.piece_color)

class Queen(ChessPiece):

    CHESS_PIECE_TYPE = "Q"
    CHESS_PIECE_VALUE = 900

    #initalize film
    def __init__(self, x_pos, y_pos, piece_color):
        super(Queen, self).__init__(x_pos, y_pos, piece_color, Queen.CHESS_PIECE_TYPE, Queen.CHESS_PIECE_VALUE)

    #get legal moves
    def get_legal_chess_piece_moves(self, board):

        #queen is diagonal adn horizontal
        diagonal = self.get_diagonal_moves(board)
        horizontal = self.get_horizontal_moves(board)
        
        return horizontal + diagonal

    #duplicate self
    def duplicate(self):
        return Queen(self.x_pos, self.y_pos, self.piece_color)

class King(ChessPiece):

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

        return self.remove_illegal_moves(chess_piece_moves)

    def get_castle_move(self, board, direction):

        #get rook position
        rook_offset = 3 if direction == 1 else -4
        piece_in_corner = board.get_piece(self.x_pos + rook_offset, self.y_pos)

        #check if rook is not captured and valid
        if piece_in_corner == 0 or piece_in_corner.CHESS_PIECE_TYPE != Rook.CHESS_PIECE_TYPE:
            return None

        #check rook color
        if piece_in_corner.piece_color != self.piece_color:
            return None

        #make sure king hasn't moved
        if (self.piece_color == ChessPiece.CHESS_PIECE_WHITE and board.CHESS_PIECE_WHITE_king_moved) or \
           (self.piece_color == ChessPiece.CHESS_PIECE_BLACK and board.CHESS_PIECE_BLACK_king_moved):
            return None

        #check if there is a piece between the king and rook
        range_check = range(1, 3) if direction == 1 else range(-1, -4, -1)
        for i in range_check:
            if board.get_piece(self.x_pos + i, self.y_pos) != 0:
                return None

        return PieceMove(self.x_pos, self.y_pos, self.x_pos + (2 * direction), self.y_pos)

    #duplicate self
    def duplicate(self):
        return King(self.x_pos, self.y_pos, self.piece_color)
