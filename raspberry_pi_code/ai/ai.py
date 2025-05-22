import chessBoard, pieces.chessPiece, ai.transpositionTables, numpy

class ChessAI:

    INFINITE = 10000000

    @staticmethod
    def evaluate(board):

        #get the material score
        material = ChessAI.get_material_score(board)

        #get transposition table scores
        pawns = ChessAI.get_piece_transposition_score(board, pieces.chessPiece.Pawn.CHESS_PIECE_TYPE, ai.transpositionTables.PAWN_PIECE_TABLE)
        knights = ChessAI.get_piece_transposition_score(board, pieces.chessPiece.Knight.CHESS_PIECE_TYPE, ai.transpositionTables.KNIGHT_PIECE_TABLE)
        bishops = ChessAI.get_piece_transposition_score(board, pieces.chessPiece.Bishop.CHESS_PIECE_TYPE, ai.transpositionTables.BISHOP_PIECE_TABLE)
        rooks = ChessAI.get_piece_transposition_score(board, pieces.chessPiece.Rook.CHESS_PIECE_TYPE, ai.transpositionTables.ROOK_PIECE_TABLE)
        queens = ChessAI.get_piece_transposition_score(board, pieces.chessPiece.Queen.CHESS_PIECE_TYPE, ai.transpositionTables.QUEEN_PIECE_TABLE)

        #return the material score and tables
        return material + pawns + knights + bishops + rooks + queens

    @staticmethod
    def get_material_score(board):

        #set scores to 0
        white_score = 0
        black_score = 0

        #loop through the chessboard and get material
        for x_pos in range(8):
            for y_pos in range(8):
                piece = board.chesspieces[x_pos][y_pos]
                if piece != 0:
                    if piece.piece_color == pieces.chessPiece.Piece.CHESS_PIECE_WHITE:
                        white_score += piece.CHESS_PIECE_VALUE
                    else:
                        black_score += piece.CHESS_PIECE_VALUE

        #return white - black (user is alwasy white)
        return white_score - black_score

    @staticmethod
    def get_piece_transposition_score(board, piece_type, table):

        #set scores to 0
        white_score = 0
        black_score = 0

        #loop through the chessboard and get transposition values
        for x_pos in range(8):
            for y_pos in range(8):
                piece = board.chesspieces[x_pos][y_pos]
                if piece != 0 and piece.CHESS_PIECE_TYPE == piece_type:
                    if piece.piece_color == pieces.chessPiece.Piece.CHESS_PIECE_WHITE:
                        white_score += table[x_pos][y_pos]
                    else:
                        black_score += table[7 - x_pos][y_pos]

        #return white - black (user is alwasy white)
        return white_score - black_score

    @staticmethod
    def get_ai_move(chessboard, illegal_moves):

        #set best move to 0 and best to infinate
        best_move = 0
        best_score = ChessAI.INFINITE

        #loop thoguh legal moves and if invalid or illegal return
        for move in chessboard.get_legal_chess_piece_moves(pieces.chessPiece.Piece.CHESS_PIECE_BLACK):
            if ChessAI.is_illegal_move(move, illegal_moves):
                continue

            #create copy of the board and make the move
            copy = chessboard.Board.duplicate(chessboard)
            copy.make_move(move)

            #alpha beta pruning
            score = ChessAI.alpha_beta_pruning(copy, 6, -ChessAI.INFINITE, ChessAI.INFINITE, True)

            #set the best score if it is better
            if score < best_score:
                best_score = score
                best_move = move

        #return 0 if there is no best move
        if best_move == 0:
            return 0

        #create copy of the board and make the move
        copy = chessboard.Board.duplicate(chessboard)
        copy.make_move(best_move)

        #check pieces and append illegal moves, then get ai move
        if copy.is_check(pieces.chessPiece.Piece.CHESS_PIECE_BLACK):
            illegal_moves.append(best_move)
            return ChessAI.get_ai_move(chessboard, illegal_moves)

        #return best move
        return best_move

    #return illegal moves
    @staticmethod
    def is_illegal_move(move, invalid_moves):
        return any(invalid_move.is_tile_equal(move) for invalid_move in invalid_moves)

    @staticmethod
    def minimax(board, depth, maximizing):
        
        #if depth is 0 then minmax wont work
        if depth == 0:
            return ChessAI.evaluate(board)

        #set best score
        best_score = -ChessAI.INFINITE if maximizing else ChessAI.INFINITE

        #get legal moves
        for move in board.get_legal_chess_piece_moves(pieces.chessPiece.Piece.CHESS_PIECE_WHITE if maximizing else pieces.chessPiece.Piece.CHESS_PIECE_BLACK):
            
            #create copy of the board and make the move
            copy = board.Board.duplicate(board)
            copy.make_move(move)

            #use minmax
            score = ChessAI.minimax(copy, depth-1, not maximizing)

            #set best score
            if maximizing:
                best_score = max(best_score, score)
            else:
                best_score = min(best_score, score)

        #return best score
        return best_score

    @staticmethod
    def alpha_beta_pruning(chessboard, depth, a, b, maximizing):
        
        #if depth 0 return back to evaluate
        if depth == 0:
            return ChessAI.evaluate(chessboard)

        #set best score
        best_score = -ChessAI.INFINITE if maximizing else ChessAI.INFINITE

        #get legal moves
        for move in chessboard.get_legal_chess_piece_moves(pieces.chessPiece.Piece.CHESS_PIECE_WHITE if maximizing else pieces.chessPiece.Piece.CHESS_PIECE_BLACK):
            
            #create copy of the board and make the move
            copy = chessboard.Board.duplicate(chessboard)
            copy.make_move(move)

            #get the max and min and call alphja beta again
            best_score = max(best_score, ChessAI.alpha_beta_pruning(copy, depth-1, a, b, False)) if maximizing else min(best_score, ChessAI.alpha_beta_pruning(copy, depth-1, a, b, True))
            a = max(a, best_score) if maximizing else a
            b = min(b, best_score) if not maximizing else b

            #break early
            if b <= a:
                break

        #return best score
        return best_score
