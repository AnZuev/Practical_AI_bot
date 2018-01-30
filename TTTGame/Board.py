from enum import Enum
from copy import deepcopy
class State(Enum):
    Blank = "-"
    X = "X"
    O = "O"
class Board:
    def __init__(self):
        self.BOARD_SIDE = 3
        self.winner = State.Blank
        self.playerTurn = State.X
        self.avaliableMoves = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.board = [[State.Blank for j in range(self.BOARD_SIDE)] for i in range(self.BOARD_SIDE)]
        self.moveCounter = 0
        self.gameOver = False
        
    def move(self, index):
        return self.__move(index % self.BOARD_SIDE, index // self.BOARD_SIDE)
    
    def reset(self):
        self.BOARD_SIDE = 3
        self.winner = State.Blank
        self.playerTurn = State.X
        self.avaliableMoves = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.board = [[State.Blank for j in range(self.BOARD_SIDE)] for i in range(self.BOARD_SIDE)]
        self.moveCounter = 0
        self.gameOver = False
    
    def __move(self, x, y):
        if self.gameOver:
            return False
        if self.board[y][x] == State.Blank:
            self.board[y][x] = self.playerTurn
        else:
            return False
        self.moveCounter += 1
        self.avaliableMoves.remove(y * self.BOARD_SIDE + x)
        if self.moveCounter == self.BOARD_SIDE ** 2:
                self.winner = State.Blank;
                self.gameOver = True;
        self.__checkRow(y)
        self.__checkColumn(x)
        self.__checkDiagonalFromTopLeft(x, y)
        self.__checkDiagonalFromTopRight(x, y)
        
        self.playerTurn = State.O if self.playerTurn == State.X else State.X
        return True
    
    def isGameOver(self):
        return self.gameOver
    
    def getTurn(self):
        return self.playerTurn
    
    def getWinner(self):
        if self.isGameOver():
            return self.winner
        
    def getAvaliableMoves(self):
        return self.avaliableMoves
    
    def copy(self):
        newBoard = Board()
        newBoard.board = deepcopy(self.board)
        newBoard.playerTurn = self.playerTurn
        newBoard.winner = self.winner
        newBoard.moveCounter = self.moveCounter
        newBoard.gameOver = self.gameOver
        newBoard.avaliableMoves = deepcopy(self.avaliableMoves) 
        return newBoard
    
    def __str__(self):
        ans = ""
        for j in self.board:
            for i in j:
                ans += " ".join(i.value) + " "
            ans += "\n"
        return ans
        
    
    def __checkRow(self, row):
        for i in range(1, self.BOARD_SIDE):
            if self.board[row][i] != self.board[row][i - 1]:
                break
            if i == self.BOARD_SIDE - 1:
                self.winner = self.playerTurn;
                self.gameOver = True;
    
    def __checkColumn(self, column):
        for i in range(1, self.BOARD_SIDE):
            if self.board[i][column] != self.board[i - 1][column]:
                break
            if i == self.BOARD_SIDE - 1:
                self.winner = self.playerTurn;
                self.gameOver = True;
                
    def __checkDiagonalFromTopLeft(self, x, y):
        if x == y:
            for i in range(1, self.BOARD_SIDE):
                if self.board[i][i] != self.board[i - 1][i - 1]:
                    break
                if i == self.BOARD_SIDE - 1:
                    self.winner = self.playerTurn;
                    self.gameOver = True;
    
    def __checkDiagonalFromTopRight(self, x, y):
        if (self.BOARD_SIDE - 1 - x) == y:
            for i in range(1, self.BOARD_SIDE):
                if self.board[self.BOARD_SIDE - 1 - i][i] != self.board[self.BOARD_SIDE - i][i - 1]:
                    break
                if i == self.BOARD_SIDE - 1:
                    self.winner = self.playerTurn;
                    self.gameOver = True;
        
