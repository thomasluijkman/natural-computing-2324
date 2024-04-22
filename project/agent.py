import numpy as np
from enum import Enum
from game import Hand, Card
# Store number of rounds taken, money, true count
# TODO table with splittable cards, table with ace in hand, rest
# Evolutionairy algorithm\


#For each use in functions calls and make it more usable
HT = 0
ST = 1 #Stand
SP = 2 #Split
DH = 3 #Double if possible otherwise hit
DS = 4 #Double if possible otherwise stand
# insurance = 5

OTHER_TABLE = 0
ACE_TABLE = 1
PAIR_TABLE = 2


class Agent:
    def __init__(self):
        self.money = 500
        self.decision_table = Decision_tables()
        self.epochs = 10000

    def mutate_tables(self):
        pass
        # TODO not quite sure how we want to do this yet.
        
    def get_agent_fitness(self):
        return self.money
    
    def get_agent_strat(self):
        return self.decision_table

class Actions(Enum):
    HT = 0
    ST = 1 #Stand
    SP = 2 #Split
    DH = 3 #Double if possible otherwise hit
    DS = 4 #Double if possible otherwise stand
    # insurance = 5

class Decision_tables():

    def __init__(self):
        self.lookup_table_other = np.zeros((16,10))
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
        
    def update_table_cell(self, table, pos, action):
        try:
            x, y = pos
            
            def check_position_range(table_name, table, x, y):
                if x < 0 or x >= len(table) or y < 0 or y >= len(table[0]):
                    raise ValueError(f"Cannot update table: position ({x},{y}) out of range for '{table_name}' table")

            match table:
                case 0: # Other Table
                    check_position_range("other", self.lookup_table_other, x, y)
                    self.lookup_table_other[x][y] = action
                case 1: # Ace Table
                    check_position_range("ace", self.lookup_table_ace, x, y)
                    self.lookup_table_ace[x][y] = action
                case 2: # Pair Table
                    check_position_range("pair", self.lookup_table_pair, x, y)
                    self.lookup_table_pair[x][y] = action
                case _:
                    raise ValueError("Invalid table index while trying to update table")
        except ValueError as e:
                print(e)  # Print the error message
    
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
    agent2 = Agent()
    tables = agent.decision_table
    tables.print_table_other()
    tables.update_table_cell(OTHER_TABLE, (4,4), ST)
    tables.print_table_other()
    agent2.decision_table.print_table_other()

    

