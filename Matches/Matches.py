import random


# Использование:
# 1. Создать объект класса
# 2. Если человек ходит первый, то вызывать функцию makeMove пока getCurrentNumber>0
# 3. Если бот ходит первый, то вызвать сначала функцию respondMove, далее как в п.2
# 4. При повторном использовании либо заного создать объект, либо вызвать функцию restart

class Matches:
    
    currentNumber = 21
    
    def __init__(this):
        this.currentNumber = 21
        
        
    def restart(this):
        this.currentNumber = 21
    
    
    def makeMove(this, move):
    

        if move<1 or move>3:
            return "Wrong move. You can only take 1, 2 or 3 matches"
    
        if this.currentNumber-move<0:
            return "Wrong move. Can't take more than there currently are"
    
    
        if this.currentNumber == move:
            this.currentNumber = 0
            return "You've lost!"
    
    
    
    

    
        this.currentNumber -= move
    
        return this.respondMove()
    
    
    
    def respondMove(this):
    
        rem = (this.currentNumber-1)%4
    
        answer = rem
    
        if rem==0:
            answer = random.randint(1,3)
        
        this.currentNumber -= answer
    
        return "I take " + str(answer) + ". Current number of matches: " + str(this.getCurrentNumber())
    
    
    
    
    
    def getCurrentNumber(this):
        return this.currentNumber
    
    def maxPossibleMove(this):
        return min(3, this.currentNumber)
            

    
