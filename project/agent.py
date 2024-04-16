import numpy as np
from enum import Enum
import game
# Store number of rounds taken, money, true count
# TODO table with splittable cards, table with ace in hand, rest
# Evolutionairy algorithm\


class Agent:
    def __init__(self):
        self.money = 500
        self.decision_table = Decision_tables()
        self.epochs = 10000


class Actions(Enum):
    hit = 0
    stand = 1
    split = 2
    double_h = 3
    double_s = 4
    split = 5
    insurance = 6

class Decision_tables():
    def __init__(self):
        self.lookup_table_other = np.zeros((10,10))
        self.lookup_table_ace = np.zeros((7,10))
        self.lookup_table_pair = np.zeros((10,10))

    def lookup_action(self, agent_hand, dealer_hand):
        y = dealer_hand.hand[0].rank - 1 # The table starts with and A (index 0) and continues with all the numbers until 10 (index 9)
        # Include special case for J, Q and K
        if dealer_hand.hand[0].rank > 10:
            y = 9
        if agent_hand.pair(agent_hand): 
            #compute index
            x = agent_hand.hand[0]-1
            if agent_hand.hand[0].rank > 10:
                x = 9
            return self.lookup_table_pair[x][y]
        elif agent_hand.aces() > 0:
            #compute index 
            x = agent_hand.scoreHand() - 11 - 2 # minus ace - 2 for indexing
            return self.lookup_table_pair[x][y]
        else:
            #compute index
            x = agent_hand.scoreHand() - 8
            return self.lookup_table_other[x][y]

