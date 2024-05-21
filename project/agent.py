import numpy as np
from enum import Enum
from game import Hand, Card, Blackjack, GameState, Actions, sum_gamestates
import random

class Agent:
    def __init__(self, decision_tables=None):
        self.money = 500
        self.score = 0
        if decision_tables is None:
            self.decision_tables = DecisionTables()
        elif isinstance(decision_tables, list):
            self.decision_tables = DecisionTables(all_tables=decision_tables)
        else:
            self.decision_tables = decision_tables 
        
    def getAgentFitness(self, nr_rounds):
        return self.score / nr_rounds
    
    def getAgentStrategy(self):
        return self.decision_tables

    def playGame(self, nr_rounds):
        self.score = 0
        game = Blackjack() # create an instance
        for i in range(nr_rounds):
            (player_hands, dealer_hand) = game.startGame() # initialise the game: deal initial cards to dealer and agent, player_hands == list of hands
            while player_hands != [] and any(isinstance(ph, Hand) for ph in player_hands): 
                for hand_index, player_hand in enumerate(player_hands): # for each player hand -> select action and play the round
                    if isinstance(player_hand, GameState):
                        continue
                    action = self.decision_tables.lookupAction(player_hand, dealer_hand)
                    game.agentAction(hand_index, action) # Send selected action to the game, the game should act on the action and change the hand
                    # Additionally, game should check if the state is winning/loosing and change the hands list value to GameState value 
                player_hands = game.getAllAgentHands() # Returns int score if game is finished otherwise hand i.e. [Hand1, 1, hand3]
            round_score = sum_gamestates(player_hands) # Update the score
            self.score += round_score

    def __str__(self):
        return str(self.decision_tables)
            

LOOKUP_REGULAR = 0
LOOKUP_ACE     = 1
LOOKUP_PAIR    = 2

class DecisionTables():
    def __init__(self, lookup_table_regular=None, lookup_table_ace=None, lookup_table_pair=None, all_tables=None):
        self.tables = []
        if all_tables is not None:
            self.tables = all_tables
        else:
            if lookup_table_regular is not None:
                assert (lookup_table_regular.shape == (16,10))
                self.tables.append(lookup_table_regular)
            else:
                regular = np.random.choice([Actions.HT,Actions.ST, Actions.DH, Actions.DS], size=(16, 10))
                self.tables.append(regular)
            if lookup_table_ace is not None:
                assert (lookup_table_ace.shape == (8,10))
                self.tables.append(lookup_table_ace)
            else:
                ace = np.random.choice([Actions.HT,Actions.ST, Actions.DH, Actions.DS], size=(8, 10))
                self.tables.append(ace)
            if lookup_table_pair is not None:
                assert (lookup_table_pair.shape == (10,10))
                self.tables.append(lookup_table_pair)
            else:
                pair = np.random.choice(list(Actions), size=(10, 10))
                self.tables.append(pair)
    
    def getAllTables(self):
        return self.tables

    def lookupAction(self, agent_hand, dealer_hand):
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
            return self.tables[LOOKUP_PAIR][x][y]
        elif agent_hand.aces() > 0:
            #compute index 
            x = agent_hand.scoreHand() - 11 - 2 # minus ace - 2 for indexing
            return self.tables[LOOKUP_ACE][x][y]
        else:
            #compute index
            x = agent_hand.scoreHand() - 5
            return self.tables[LOOKUP_REGULAR][x][y]
        
    def updateTableCell(self, table, pos, action):
        x, y = pos
        
        def check_position_range(table_name, table, x, y):
            if x < 0 or x >= len(table) or y < 0 or y >= len(table[0]):
                raise ValueError(f"Cannot update table: position ({x},{y}) out of range for '{table_name}' table")
            
        match table:
            case 0: # Regular Table
                check_position_range("regular", self.tables[LOOKUP_REGULAR], x, y)
                self.tables[LOOKUP_REGULAR][x][y] = action.value
            case 1: # Ace Table
                check_position_range("ace", self.tables[LOOKUP_ACE], x, y)
                self.tables[LOOKUP_ACE][x][y] = action.value
            case 2: # Pair Table
                check_position_range("pair", self.tables[LOOKUP_PAIR], x, y)
                self.tables[LOOKUP_PAIR][x][y] = action.value
            case _:
                raise ValueError("Invalid table index while trying to update table")
    
    def str_regular_table(self):
        table = self.tables[LOOKUP_REGULAR]
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
        return table_string
    
    def str_ace_table(self):
        table = self.tables[LOOKUP_ACE]
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
        return table_string
    
    def str_pair_table(self):
        table = self.tables[LOOKUP_PAIR]
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
        return table_string

    def printTables(self):
        print(str(self))

    def __str__(self):
        string = ""
        string += "Regular Table:" + "\n"
        string += self.str_regular_table() + "\n"
        string += "Ace Table:" + "\n"
        string += self.str_ace_table() + "\n"
        string += "Pair Table:" + "\n"
        string += self.str_pair_table()
        return string

if __name__ == "__main__":
    agent = Agent()
    agent.decision_tables.printTables()
    print(agent.getAgentFitness())
    agent.playGame(200)
    print(agent.getAgentFitness())
