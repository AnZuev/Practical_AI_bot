from TTTGame import Board
from TTTGame import AlphaBetaPrunning
class Game:

    def play(self):
        self.board = Board.Board()
        self.abp = AlphaBetaPrunning.AlphaBetaPrunning()
        print("You will play as?\ntype X or O")
        self.wish = input().upper()
        if self.wish not in ("X", "O"):
            self.wish="X"
        print("Select level.\nEasy - 1\nMedium -2\nHard - 3\ntype 1 or 2 or 3.")
        self.difficulty = input()
        if self.difficulty =="1":
            self.difficulty=1
        if self.difficulty =="2":
            self.difficulty=3
        if self.difficulty =="3":
            self.difficulty=9
        else:    
            self.difficulty = 3
        print("New game started.")
        while True:
            self.__nextStep()
            if self.board.getTurn().value == self.wish:
                self.__status()
            if self.board.isGameOver():
                self.__printWinner()
                if not self.__tryAgain():
                    break

    def __nextStep(self):
        if self.board.getTurn().value == self.wish:
            self.__getPlayerMove()
        else:
            self.abp.run(self.board.getTurn(), self.board, self.difficulty)
    
    def __status(self):
        print(str(self.board))
        
    def __getPlayerMove(self):
        print("Index of move: ")
        try:
            val = int(input()) - 1
            if 0 > val or val > self.board.BOARD_SIDE ** 2:
                print("Index must be an integer between 1 and %d." % self.board.BOARD_SIDE ** 2)
            elif not self.board.move(val):
                print("The selected index must be blank. This one is already Occupied.")
        except ValueError:
            print("Index must be an integer between 1 and %d." % self.board.BOARD_SIDE ** 2)
     
    def __printWinner(self):
        winner = self.board.getWinner()
        if winner == Board.State.Blank:
            print("Draw")
        else:
            print(str(winner.name) + " win!")
    
    def __tryAgain(self):
        if self.__tryAgainCheck():
            print("You will play as X or O?\ntype X or O")
            self.wish = input().upper()
            if self.wish in ("X", "O"):
                print("Select level.\nEasy - 1\nMedium -2\nHard - 3\ntype 1 or 2 or 3.")
                self.difficulty = input()
                if self.difficulty =="1":
                    self.difficulty=1
                if self.difficulty =="2":
                    self.difficulty=3
                if self.difficulty =="3":
                    self.difficulty=9
                else:    
                    self.difficulty = 3
                self.board.reset()
                return True
            else:
                print("Invalid input.\nYou will play as X.")
                self.wish="X"
                self.difficulty = 3
                self.board.reset()
                return True
        return False  

    def __tryAgainCheck(self):
        while True:
            print("Try again? y/n")
            answer = input().lower()
            if answer == "y":
                return True
            if answer == "n":
                return False
            print("Invalid input.")
            
        
game = Game()
game.play()    
