from ttt_game.board import Board


class AlphaBetaPrunning:
    def __init__(self):
        self.maxDepth = float('inf')

    def run(self, player, board, max_depth):
        if max_depth < 1:
            return False
        self.maxDepth = max_depth
        self.__abprunning(player, board, float('-inf'), float('inf'), 0)

    def __abprunning(self, player, board, alpha, beta, curr_depth):
        if curr_depth == self.maxDepth or board.is_game_over():
            return self.__score(player, board, curr_depth)
        curr_depth += 1
        if board.getTurn() == player:
            return self.__get_max(player, board, alpha, beta, curr_depth)
        else:
            return self.__get_min(player, board, alpha, beta, curr_depth)

    def __get_max(self, player, board, alpha, beta, curr_depth):
        best_move = -1
        for move in board.get_avaliable_moves():
            mod_board = board.copy()
            mod_board.move(move)
            score = self.__abprunning(player, mod_board, alpha, beta, curr_depth)
            if score > alpha:
                alpha = score
                best_move = move
            if alpha >= beta:
                break
        if best_move != -1:
            board.move(best_move)
        return alpha

    def __get_min(self, player, board, alpha, beta, curr_depth):
        best_move = -1
        for move in board.get_avaliable_moves():
            mod_board = board.copy()
            mod_board.move(move)
            score = self.__abprunning(player, mod_board, alpha, beta, curr_depth)
            if score < beta:
                beta = score
                best_move = move
            if alpha >= beta:
                break
        if best_move != -1:
            board.move(best_move)
        return beta

    def __score(self, player, board, curr_depth):
        if player == board.State.Blank:
            return False
        opponent = board.State.O if player == board.State.X else board.State.X
        if board.is_game_over() and board.get_winner() == player:
            return 10 - curr_depth
        elif board.isGameOver() and board.get_winner() == opponent:
            return -10 + curr_depth
        else:
            return 0
