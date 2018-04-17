from ttt_game import board


class AlphaBetaPrunning:
    def __init__(self):
        self.max_depth = float('inf')

    def run(self, player, board, maxDepth):
        if maxDepth < 1:
            return False
        self.max_depth = maxDepth
        self.__abprunning(player, board, float('-inf'), float('inf'), 0)

    def __abprunning(self, player, board, alpha, beta, currDepth):
        if currDepth == self.max_depth or board.is_game_over():
            return self.__score(player, board, currDepth)
        currDepth += 1
        if board.get_turn() == player:
            return self.__get_max(player, board, alpha, beta, currDepth)
        else:
            return self.__get_min(player, board, alpha, beta, currDepth)

    def __get_max(self, player, board, alpha, beta, currDepth):
        best_move = -1
        for move in board.get_available_moves():
            mod_board = board.copy()
            mod_board.move(move)
            score = self.__abprunning(player, mod_board, alpha, beta, currDepth)
            if score > alpha:
                alpha = score
                best_move = move
            if alpha >= beta:
                break
        if best_move != -1:
            board.move(best_move)
        return alpha

    def __get_min(self, player, board, alpha, beta, currDepth):
        best_move = -1
        for move in board.get_available_moves():
            mod_board = board.copy()
            mod_board.move(move)
            score = self.__abprunning(player, mod_board, alpha, beta, currDepth)
            if score < beta:
                beta = score
                best_move = move
            if alpha >= beta:
                break
        if best_move != -1:
            board.move(best_move)
        return beta

    def __score(self, player, board, currDepth):
        if player == board.State.Blank:
            return False
        opponent = board.State.O if player == board.State.X else board.State.X
        if board.is_game_over() and board.get_winner() == player:
            return 10 - currDepth
        elif board.is_game_over() and board.get_winner() == opponent:
            return -10 + currDepth
        else:
            return 0
