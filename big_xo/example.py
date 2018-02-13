from big_xo.game import *
from big_xo.players import *


ai = AI("AI Player")
human = Player("Human Player")
g = Game(human, ai,   10)

human.move((2, 3))
