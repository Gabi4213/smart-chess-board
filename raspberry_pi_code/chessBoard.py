import pieces.chessPiece
from pieces.pieceMove import Move

class Board:

    WIDTH = 8
    HEIGHT = 8

    #initialize function
    def __init__(self, chesspieces, CHESS_PIECE_WHITE_king_moved=False, CHESS_PIECE_BLACK_king_moved=False):
        self.chesspieces = chesspieces
        self.CHESS_PIECE_WHITE_king_moved = CHESS_PIECE_WHITE_king_moved
        self.CHESS_PIECE_BLACK_king_moved = CHESS_PIECE_BLACK_king_moved

    #duplicate board
    @classmethod
    def duplicate(cls, chessboard):
        chesspieces = [[0 for _ in range(Board.WIDTH)] for _ in range(Board.HEIGHT)]
        for x_pos in range(Board.WIDTH):
            for y_pos in range(Board.HEIGHT):
                piece = chessboard.chesspieces[x_pos][y_pos]
                if piece != 0:
                    chesspieces[x_pos][y_pos] = piece.duplicate()
        return cls(chesspieces, chessboard.CHESS_PIECE_WHITE_king_moved, chessboard.CHESS_PIECE_BLACK_king_moved)

    #setup board from fen
    @classmethod
    def from_fen(cls, fen):
        chesspieces = [[0 for _ in range(Board.WIDTH)] for _ in range(Board.HEIGHT)]
        rows = fen.split(' ')[0].split('/')
        for y in range(8):
            row = rows[y]
            x = 0
            for char in row:
                if char.isdigit():
                    x += int(char)
                else:
                    color = pieces.chessPiece.Piece.CHESS_PIECE_WHITE if char.isupper() else pieces.chessPiece.Piece.CHESS_PIECE_BLACK
                    piece_type = char.lower()
                    piece = None
                    if piece_type == 'p':
                        piece = pieces.chessPiece.Pawn(x, y, color)
                    elif piece_type == 'r':
                        piece = pieces.chessPiece.Rook(x, y, color)
                    elif piece_type == 'n':
                        piece = pieces.chessPiece.Knight(x, y, color)
                    elif piece_type == 'b':
                        piece = pieces.chessPiece.Bishop(x, y, color)
                    elif piece_type == 'q':
                        piece = pieces.chessPiece.Queen(x, y, color)
                    elif piece_type == 'k':
                        piece = pieces.chessPiece.King(x, y, color)
                        if color == pieces.chessPiece.Piece.CHESS_PIECE_WHITE:
                            CHESS_PIECE_WHITE_king_moved = False
                        else:
                            CHESS_PIECE_BLACK_king_moved = False
                    chesspieces[x][y] = piece
                    x += 1

        #castling 
        castling_rights = fen.split(' ')[2] if len(fen.split(' ')) > 2 else "-"
        white_king_moved = 'K' not in castling_rights and 'Q' not in castling_rights
        black_king_moved = 'k' not in castling_rights and 'q' not in castling_rights

        return cls(chesspieces, white_king_moved, black_king_moved)

    #get legal moves
    def get_legal_chess_piece_moves(self, piece_color):
        chess_piece_moves = []
        for x_pos in range(Board.WIDTH):
            for y_pos in range(Board.HEIGHT):
                piece = self.chesspieces[x_pos][y_pos]
                if (piece != 0):
                    if (piece.piece_color == piece_color):
                        chess_piece_moves += piece.get_legal_chess_piece_moves(self)

        return chess_piece_moves

    #make move - mianly used for simulating moves
    def make_move(self, move):
        piece = self.chesspieces[move.xfrom][move.yfrom]
        self.move_piece(piece, move.xto, move.yto)

        #pawn promotion
        if (piece.CHESS_PIECE_TYPE == pieces.chessPiece.Pawn.CHESS_PIECE_TYPE):
            if (piece.y_pos == 0 or piece.y_pos == Board.HEIGHT-1):
                self.chesspieces[piece.x_pos][piece.y_pos] = pieces.chessPiece.Queen(piece.x_pos, piece.y_pos, piece.piece_color)


        if (piece.CHESS_PIECE_TYPE == pieces.chessPiece.King.CHESS_PIECE_TYPE):

            #set king as moved
            if (piece.piece_color == pieces.chessPiece.Piece.CHESS_PIECE_WHITE):
                self.CHESS_PIECE_WHITE_king_moved = True
            else:
                self.CHESS_PIECE_BLACK_king_moved = True
            
            #kingside castling
            if (move.xto - move.xfrom == 2):
                rook = self.chesspieces[piece.x_pos+1][piece.y_pos]
                self.move_piece(rook, piece.x_pos+1, piece.y_pos)

            #queenside castling
            if (move.xto - move.xfrom == -2):
                rook = self.chesspieces[piece.x_pos-2][piece.y_pos]
                self.move_piece(rook, piece.x_pos+1, piece.y_pos)
    
    #move piece
    def move_piece(self, piece, xto, yto):
        self.chesspieces[piece.x_pos][piece.y_pos] = 0
        piece.x_pos = xto
        piece.y_pos = yto

        self.chesspieces[xto][yto] = piece


    #cehck if its in check
    def is_check(self, piece_color):
        
        #check the color
        other_piece_color = pieces.chessPiece.Piece.CHESS_PIECE_WHITE
        if piece_color == pieces.chessPiece.Piece.CHESS_PIECE_WHITE:
            other_piece_color = pieces.chessPiece.Piece.CHESS_PIECE_BLACK

        #find legal movbes
        for move in self.get_legal_chess_piece_moves(other_piece_color):
            
            #simulate the moves
            copy = Board.duplicate(self)
            copy.make_move(move)

            #cehck if the opposing move places it into check
            king_found = False

            #itterate through moves
            for x_pos in range(Board.WIDTH):
                for y_pos in range(Board.HEIGHT):
                    piece = copy.chesspieces[x_pos][y_pos]
                    if piece != 0:
                        #check color and type and then set to true if so
                        if piece.piece_color == piece_color and piece.CHESS_PIECE_TYPE == pieces.chessPiece.King.CHESS_PIECE_TYPE:
                            king_found = True

            #if no king is founbd then it is in check
            if not king_found:
                return True

        #if no move resutls in cehck return false
        return False


    #get piece at tile
    def get_piece(self, x_pos, y_pos):
        if (not self.in_bounds(x_pos, y_pos)):
            return 0

        return self.chesspieces[x_pos][y_pos]

    #check if its in board bounds
    def in_bounds(self, x_pos, y_pos):
        return (x_pos >= 0 and y_pos >= 0 and x_pos < Board.WIDTH and y_pos < Board.HEIGHT)
