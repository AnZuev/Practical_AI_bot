from big_xo.libs import *


class Board:
    def __init__(self, board_size):
        self.board = np.zeros((board_size, board_size))

    def update(self, player, cell):
        if self.board[cell[0]][cell[1]] == 0:
            self.board[cell[0]][cell[1]] = player
            return True
        return False



class Game:
    def __init__(self, player1, player2, board_size = 100):
        self.board = Board(board_size)
        self.players = dict({
            '1': player1,
            '-1': player2
        })
        player1.set_game(self)
        player1.set_type(PLAYER_TYPE['x'])
        player2.set_game(self)
        player2.set_type(PLAYER_TYPE['o'])

        self.finished = False
        self.winner = None

        self.current_player = PLAYER_TYPE['x']
        self.players[str(self.current_player)].up()
        print(self.board.board)

    def make_a_move(self, player, cell):
        if self.finished:
            print("Game is already finished, winner is {}".format(self.winner.name))
            return
        if player != self.current_player:
            print("{} is about to move, not {}".format(self.current_player.name, self.players[str(player)].name))
        if not self.board.update(player, cell):
            print("Move {} is invalid".format(cell))
            self.players[str(self.current_player)].up()
        else:
            print(self.board.board)
            self.check_ending()
            print("\n")
            self.current_player = -1 * self.current_player
            if not self.finished:
                self.players[str(self.current_player)].up()
            else:
                print("Game is finished. {} won".format(self.winner.name))

    def check_ending(self):
        my_scores, opponent_scores = score_game(self.board.board, PLAYER_TYPE['x'])
        my_total_score, opponent_total_score, difference = get_total_scores(my_scores, opponent_scores)
        if my_total_score >= SCORES['five']:
            self.finished = True
            self.winner = self.players[str(PLAYER_TYPE['x'])]
        elif opponent_total_score >= SCORES['five']:
            self.finished = True
            self.winner = self.players[str(PLAYER_TYPE['o'])]
