from Big_xo.game import *
from Big_xo.players import *


ai = AI("AI Player")
human = Player("Human Player")
g = BigGame(human, ai,   10)

human.move((2, 3))
