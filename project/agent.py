import numpy as np
from enum import Enum
from game import Hand, Card, Blackjack, GameState, Actions, sum_gamestates
import random
from known_strat import regular_table_known, ace_table_known, pair_table_known
import pickle

TABLE_SIZE = (16*10)+(8*10)+(10*10) #360
MAX_BET = 100

class Agent:
    def __init__(self, nr_rounds, decision_tables=None, betting_table=None):
        self.money = nr_rounds * MAX_BET * 2
        self.score = 0
        self.nr_rounds = nr_rounds
        if decision_tables is None:
            self.decision_tables = DecisionTables()
        elif isinstance(decision_tables, list):
            self.decision_tables = DecisionTables(all_tables=decision_tables)
        else:
            self.decision_tables = decision_tables 
        if betting_table is None:
            self.betting_table = BettingTable()
        else:
            self.betting_table = BettingTable(betting_table)
        
    def getAgentFitness(self):
        return self.score / self.nr_rounds
    
    def getAgentFitnessMoney(self):
        return self.money / self.nr_rounds

    def getAgentStrategy(self):
        return self.decision_tables

    def playGame(self):
        self.score = 0
        card_count = 0
        game = Blackjack() # create an instance
        for i in range(self.nr_rounds):
            bet = self.betting_table.lookupBet(card_count=card_count)
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
            card_count = game.getCardCount()
            # if card_count >=30 or card_count <= -30:
            #     print(card_count)
            for score in player_hands:
                self.money += score.value * bet

    def __str__(self):
        return str(self.decision_tables)
            

LOOKUP_REGULAR = 0
LOOKUP_ACE     = 1
LOOKUP_PAIR    = 2

class BettingTable():
    def __init__(self, betting_table = None):
        if betting_table is None:
            # >=30 29-25 24-20 19-15 14-10 9-5 4-1 0 -1-(-4) -5-(-9) -10-(-14) -15-(-19) -20-(-24) -25-(-29) <=(-30)
            self.bets = np.zeros(15)
            self.bets = np.random.randint(1, 100, size=15)
        else:
            self.bets = betting_table

    def lookupBet(self, card_count):
        match card_count:
            case count if count >= 30:
                return self.bets[0]
            case count if 25 <= count <= 29:
                return self.bets[1]
            case count if 20 <= count <= 24:
                return self.bets[2]
            case count if 15 <= count <= 19:
                return self.bets[3]
            case count if 10 <= count <= 14:
                return self.bets[4]
            case count if 5 <= count <= 9:
                return self.bets[5]
            case count if 1 <= count <= 4:
                return self.bets[6]
            case 0:
                return self.bets[7]
            case count if -4 <= count <= -1:
                return self.bets[8]
            case count if -9 <= count <= -5:
                return self.bets[9]
            case count if -14 <= count <= -10:
                return self.bets[10]
            case count if -19 <= count <= -15:
                return self.bets[11]
            case count if -24 <= count <= -20:
                return self.bets[12]
            case count if -29 <= count <= -25:
                return self.bets[13]
            case count if count <= -30:
                return self.bets[14]
            case _:
                print("error bet lookup; card count is: " + str(card_count))

    def updateBetCell(self, pos, new_bet):
        self.bets[pos] = new_bet

   
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
        if agent_hand.scoreHand() == 21:
            return Actions.ST
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
        elif agent_hand.aces() > 0 and len(agent_hand.hand) == 2:
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
        hand_states = ["(A ,A )","(2 ,2 )", "(3 ,3 )", "(4 ,4 )", "(5 ,5 )", "(6 ,6 )", "(7 ,7 )", "(8 ,8 )", "(9 ,9 )", "(10,10)"]
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
    
def save_agent_to_file(agent, filename_pickle):
    with open(filename_pickle, 'wb') as file:
        pickle.dump(agent, file) # Pickling in case we want to run experiments on the best agent.

if __name__ == "__main__":
    known_strat = DecisionTables(lookup_table_regular=regular_table_known,lookup_table_ace=ace_table_known, lookup_table_pair=pair_table_known)
    agent = Agent(100000, decision_tables=known_strat)
    agent.decision_tables.printTables()
    agent.playGame()
    print(agent.getAgentFitness())
    save_agent_to_file(agent, "known_strat_agent.pkl")

    # betting_table = BettingTable()
    # print(betting_table.bets)

