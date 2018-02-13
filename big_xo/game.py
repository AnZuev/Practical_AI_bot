from big_xo.libs import *


class Board:
    def __init__(self, board_size):
        self.board = np.zeros((board_size, board_size), dtype=int)

    def update(self, player, cell):
        if self.board[cell[0]][cell[1]] == 0:
            self.board[int(cell[0])][int(cell[1])] = player
            return True
        return False

    def print_board(self):
        result = '__'
        line = 0
        for i in range(len(self.board)):
            result += str(i+1) + '_'
        result += '\n'
        for innerlist in self.board:
            line += 1
            result += str(line) + '|'
            for item in map(lambda x: 'x' if x == 1 else 'o' if x == -1 else '_', innerlist):
                result += str(item) + '  '
            result += '\n'
        return result


class Game:
    def __init__(self, player1, player2, bot, chat_id, board_size=100):
        self.board = Board(board_size)
        self.bot = bot
        self.chat_id = chat_id

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
        self.current_player = self.current_player = PLAYER_TYPE['x']

    def start(self):
        self.bot.sendMessage(
            chat_id=self.chat_id,
            text="Game started.\n{}".format(self.board.print_board())
        )

        self.players[str(self.current_player)].up()

    def make_a_move(self, player, cell):
        print("Big game: making move")
        if self.finished:
            self.bot.sendMessage(
                chat_id=self.chat_id,
                text="Game is already finished, winner is {}".format(self.winner.name)
            )
            return
        if player != self.current_player:
            self.bot.sendMessage(
                chat_id=self.chat_id,
                text="{} is about to move, not {}".format(self.current_player.name, self.players[str(player)].name)
            )
        if not self.board.update(player, cell):
            self.bot.sendMessage(
                chat_id=self.chat_id,
                text="Move {} is invalid. Try another one".format((cell[0] + 1, cell[0] + 1))
            )
            self.players[str(self.current_player)].up()
        else:

            self.check_ending()
            # print("\n")
            self.current_player = -1 * self.current_player
            if not self.finished:
                print("Asking another player to move")
                self.players[str(self.current_player)].up()
            else:
                self.bot.sendMessage(
                    chat_id=self.chat_id,
                    text="Game is finished. {} won".format(self.winner.name)
                )

    def check_ending(self):
        my_scores, opponent_scores = score_game(self.board.board, PLAYER_TYPE['x'])
        my_total_score, opponent_total_score, difference = get_total_scores(my_scores, opponent_scores)
        if my_total_score >= SCORES['five']:
            self.finished = True
            self.winner = self.players[str(PLAYER_TYPE['x'])]
        elif opponent_total_score >= SCORES['five']:
            self.finished = True
            self.winner = self.players[str(PLAYER_TYPE['o'])]
