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
    HT = 0
    ST = 1 #Stand
    SP = 2 #Split
    DH = 3 #Double if possible otherwise hit
    DS = 4 #Dboule if possible otherwise stand
    # insurance = 5

class Decision_tables():
    def __init__(self):
        self.lookup_table_other = np.zeros((16,10))
        count = 0
        for i in range(16):
            for j in range(10):
                self.lookup_table_other[i][j] = count
                count =+ 1
        self.lookup_table_ace = np.zeros((8,10))
        self.lookup_table_pair = np.zeros((10,10))

    def lookup_action(self, agent_hand, dealer_hand):
        # Include special case for J, Q and K
        if dealer_hand.hand[0].rank >= 10:
            y = 9
        else: 
            y = dealer_hand.hand[0].rank - 1 # The table starts with and A (index 0) and continues with all the numbers until 10 (index 9)
        if agent_hand.pair(): 
            #compute index
            if agent_hand.hand[0].rank >= 10:
                x = 9
            else: 
                x = agent_hand.hand[0].rank - 1
            return self.lookup_table_pair[x][y]
        elif agent_hand.aces() > 0:
            #compute index 
            x = agent_hand.scoreHand() - 11 - 2 # minus ace - 2 for indexing
            return self.lookup_table_pair[x][y]
        else:
            #compute index
            x = agent_hand.scoreHand() - 5
            return self.lookup_table_other[x][y]
    
    def print_table_other(self):
        table = self.lookup_table_other
        if (len(table) == 0) or (len(table[0]) == 0):
            print("Table is empty!")
        table_string = "   | A  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10  \n"
        table_string += ("-" * (len(table[0]) * 5 + 5)) + "\n"
        for j, row in enumerate(table):
            for i, col in enumerate(row):
                if i == 0:
                    table_string += f"{j + 5}  | {Actions(col).name} |" if j + 5 < 10 else f"{j + 5} | {Actions(col).name} |"
                elif i < len(row) - 1:
                    table_string += f" {Actions(col).name} |"
                else:
                    table_string += f" {Actions(col).name}  " + "\n"
            table_string += ("-" * (len(row) * 5 + 5)) + "\n"
        print(table_string)
    
    def print_table_ace(self):
        table = self.lookup_table_ace
        if (len(table) == 0) or (len(table[0]) == 0):
            print("Table is empty!")
        hand_states = ["(A,2)", "(A,3)", "(A,4)", "(A,5)", "(A,6)", "(A,7)", "(A,8)", "(A,9)"]
        table_string = "      | A  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10  \n"
        table_string += ("-" * (len(table[0]) * 5 + 6)) + "\n"
        for j, row in enumerate(table):
            for i, col in enumerate(row):
                if i == 0:
                    table_string += f"{hand_states[j]} | {Actions(col).name} |"
                elif i < len(row) - 1:
                    table_string += f" {Actions(col).name} |"
                else:
                    table_string += f" {Actions(col).name}  " + "\n"
            table_string += ("-" * (len(row) * 5 + 6)) + "\n"
        print(table_string)
    
    def print_table_pair(self):
        table = self.lookup_table_pair
        if (len(table) == 0) or (len(table[0]) == 0):
            print("Table is empty!")
        hand_states = ["(2 ,2 )", "(3 ,3 )", "(4 ,4 )", "(5 ,5 )", "(6 ,6 )", "(7 ,7 )", "(8 ,8 )", "(9 ,9 )", "(10,10)", "(A ,A )"]
        table_string = "        | A  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10  \n"
        table_string += ("-" * (len(table[0]) * 5 + 8)) + "\n"
        for j, row in enumerate(table):
            for i, col in enumerate(row):
                if i == 0:
                    table_string += f"{hand_states[j]} | {Actions(col).name} |"
                elif i < len(row) - 1:
                    table_string += f" {Actions(col).name} |"
                else:
                    table_string += f" {Actions(col).name}  " + "\n"
            table_string += ("-" * (len(row) * 5 + 8)) + "\n"
        print(table_string)
            
    
        

if __name__ == "__main__":
    agent = Agent()
    # tables = Decision_tables()
    # tables.print_table_pair()
    agent_hand = game.Hand()
    agent_hand.addCard(game.Card(0, 2))
    dealer_hand = game.Hand()
    agent_hand.addCard(game.Card(0, 10))
    print("Agent's hand score:", agent_hand.scoreHand())
    print("Dealer's hand score:", dealer_hand.scoreHand())
    dealer_hand.addCard(game.Card(0, 2))
    dealer_hand.addCard(game.Card(0, 10))
    print("Agent's hand score after dealer's turn:", agent_hand.scoreHand())
    print("Dealer's hand score after dealer's turn:", dealer_hand.scoreHand())
    

