from Big_xo.libs import *


class Board:
    def __init__(self, board_size):
        self.board = np.zeros((board_size, board_size), dtype=int)

    def update(self, player, cell, bot, update):
        if self.board[int(cell[0])][int(cell[1])] == 0:

            self.board[int(cell[0])][int(cell[1])] = player
            bot.sendMessage(
                chat_id=update.message.chat.id,
                text=self.print_board()
            )
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
            for item in innerlist:
                result += str(item) + '  '
            result += '\n'
        return result



class BigGame:
    def __init__(self, player1, player2, bot, update, board_size = 100):
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

        bot.sendMessage(
            chat_id=update.message.chat.id,
            text=self.board.print_board() + '\nPlease, enter cell coordinate in format xy:'
        )

    def start(self, bot, update):
        self.current_player = PLAYER_TYPE['x']
        self.players[str(self.current_player)].up(bot, update, update.message.text)

    def make_a_move(self, player, cell, bot, update):
        if self.finished:
            bot.sendMessage(
                chat_id=update.message.chat.id,
                text="Game is already finished, winner is {}".format(self.winner.name)
            )
            return
        if player != self.current_player:
            bot.sendMessage(
                chat_id=update.message.chat.id,
                text="{} is about to move, not {}".format(self.current_player.name, self.players[str(player)].name)
            )
        if not self.board.update(player, cell, bot, update):
            bot.sendMessage(
                chat_id=update.message.chat.id,
                text="Move {} is invalid".format(cell)
            )
            self.players[str(self.current_player)].up(bot, update, cell)
        else:
            bot.sendMessage(
                chat_id=update.message.chat.id,
                text=self.board.print_board()
            )
            self.check_ending()
            # print("\n")
            self.current_player = -1 * self.current_player
            if not self.finished:
                self.players[str(self.current_player)].up(bot, update, cell)
            else:
                bot.sendMessage(
                    chat_id=update.message.chat.id,
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
