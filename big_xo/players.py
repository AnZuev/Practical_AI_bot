from big_xo.libs import *


class Player:
    def __init__(self, name='Human'):
        self.name = name
        self.player_type = None
        self.game = None

    def set_type(self, player_type):
        self.player_type = player_type

    def set_game(self, game):
        self.game = game

    def up(self):
        print("It is time to move, {}".format(self.name))
        # something happend

    def move(self, cell):
        self.game.make_a_move(self.player_type, cell)


class AI:
    def __init__(self, name="AI"):
        self.name = name

    def set_type(self, player_type):
        self.player_type = player_type

    def set_game(self, game):
        self.game = game

    def up(self):
        print("{} has started thinking, wait for a couple of years, please.".format(self.name))
        self.think()

    def think(self):
        my_scores, opponent_scores = score_game(g.board.board, self.player_type)
        my_total_score, opponent_total_score, difference = get_total_scores(my_scores, opponent_scores)

        my_wi = get_max_element_index_from_2d_matrix(my_scores)
        opponent_wi = get_max_element_index_from_2d_matrix(opponent_scores)

        my_best_window = self.game.board.board[my_wi[0]: my_wi[0] + WINDOW_SIZE, my_wi[1]:my_wi[1] + WINDOW_SIZE]
        opponent_best_window = self.game.board.board[opponent_wi[0]: opponent_wi[0] + WINDOW_SIZE,
                               opponent_wi[1]:opponent_wi[1] + WINDOW_SIZE]

        my_best = find_best_move_within_window(my_best_window, self.player_type)
        opponent_best = find_best_move_within_window(opponent_best_window, -1 * self.player_type)

        t_board = np.copy(self.game.board.board)
        t_board[my_best[0]] = self.player_type
        _, _, diff1 = get_total_scores(*score_game(t_board, self.player_type))
        t_board[my_best[0]] = 0

        t_board[opponent_best[0]] = self.player_type
        _, _, diff2 = get_total_scores(*score_game(t_board, self.player_type))
        t_board[opponent_best[0]] = 0

        if diff2 > diff1:
            final_move = opponent_best[0]
        else:
            final_move = my_best[0]

        print("{}: my move is {}".format(self.name, final_move))
        self.move(final_move)

    def move(self, cell):
        self.game.make_a_move(self.player_type, cell)