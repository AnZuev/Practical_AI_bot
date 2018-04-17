from Big_xo.libs import *


class Player:
    def __init__(self, bot, chat_id, name='Human'):
        self.name = name
        self.player_type = None
        self.game = None
        self.bot = bot
        self.chat_id = chat_id

    def set_type(self, player_type):
        self.player_type = player_type

    def set_game(self, game):
        self.game = game

    def up(self):
        print("HumanPlayer: up()")
        print(self.chat_id)
        print(self.bot)
        self.bot.sendMessage(
            chat_id=self.chat_id,
            text="Your turn\n{}".format(self.game.board.print_board()),
            parse_mode='Markdown'
        )

    def move(self, cell):
        self.game.make_a_move(self.player_type, cell)


class AI:
    def __init__(self, bot, chat_id, name="AI"):
        self.name = name
        self.player_type = None
        self.game = None
        self.bot = bot
        self.chat_id = chat_id

    def set_type(self, player_type):
        self.player_type = player_type

    def set_game(self, game):
        self.game = game

    def up(self):
        self.bot.sendMessage(
            chat_id=self.chat_id,
            text="{} has started thinking, wait for a couple of years, please.".format(self.name)
        )
        self.think()

    def think(self):
        my_scores, opponent_scores = score_game(self.game.board.board, self.player_type)

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

        if diff2 >= diff1:
            final_move = opponent_best[0][0] + opponent_wi[0], opponent_best[0][1] + opponent_wi[1]
        else:
            final_move = my_best[0][0] + my_wi[0], my_best[0][1] + my_wi[1]

        self.bot.sendMessage(
            chat_id=self.chat_id,
            text="{}: my move is {}".format(self.name, (final_move[0] + 1, final_move[1] + 1))
        )
        self.move(final_move)

    def move(self, cell):
        self.game.make_a_move(self.player_type, cell)
