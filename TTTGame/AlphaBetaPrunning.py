from TTTGame import Board


class AlphaBetaPrunning:
    def __init__(self):
        self.maxDepth = float('inf')

    def run(self, player, board, maxDepth):
        if maxDepth < 1:
            return False
        self.maxDepth = maxDepth
        self.__abprunning(player, board, float('-inf'), float('inf'), 0)

    def __abprunning(self, player, board, alpha, beta, currDepth):
        if currDepth == self.maxDepth or board.isGameOver():
            return self.__score(player, board, currDepth)
        currDepth += 1
        if board.getTurn() == player:
            return self.__getMax(player, board, alpha, beta, currDepth)
        else:
            return self.__getMin(player, board, alpha, beta, currDepth)

    def __getMax(self, player, board, alpha, beta, currDepth):
        bestMove = -1
        for move in board.getAvaliableMoves():
            modBoard = board.copy()
            modBoard.move(move)
            score = self.__abprunning(player, modBoard, alpha, beta, currDepth)
            if score > alpha:
                alpha = score
                bestMove = move
            if alpha >= beta:
                break
        if bestMove != -1:
            board.move(bestMove)
        return alpha

    def __getMin(self, player, board, alpha, beta, currDepth):
        bestMove = -1
        for move in board.getAvaliableMoves():
            modBoard = board.copy()
            modBoard.move(move)
            score = self.__abprunning(player, modBoard, alpha, beta, currDepth)
            if score < beta:
                beta = score
                bestMove = move
            if alpha >= beta:
                break
        if bestMove != -1:
            board.move(bestMove)
        return beta

    def __score(self, player, board, currDepth):
        if player == Board.State.Blank:
            return False
        opponent = Board.State.O if player == Board.State.X else Board.State.X
        if board.isGameOver() and board.getWinner() == player:
            return 10 - currDepth
        elif board.isGameOver() and board.getWinner() == opponent:
            return -10 + currDepth
        else:
            return 0
