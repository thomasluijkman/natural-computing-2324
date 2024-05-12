import random
from enum import Enum

################################
# SINGLE CARD CLASS DEFINITION #
################################
ACE = 1
JACK = 11
QUEEN = 12
KING = 13

class GameState(Enum):
    Dealer_won_doubledown = -2
    Dealer_won = -1
    Agent_draw = 0
    Agent_won = 1
    Agent_won_doubledown = 2

def sum_gamestates(gamestates):
    total_sum = 0
    for state in gamestates:
        total_sum += state.value
    return total_sum

class Actions(Enum):
    HT = 0 #Hit
    ST = 1 #Stand
    SP = 2 #Split
    DH = 3 #Double if possible otherwise hit
    DS = 4 #Double if possible otherwise stand
    # insurance = 5

class Card:
    """A card is defined by two numbers: 
    Suit -- 0 = hearts, 1 = diamonds, 2 = clubs, 3 = spades
    Rank -- 1 = ace, 11 = jack, 12 = queen, 13 = king (all other numbers are obvious)
    """
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.suit == other.suit and self.rank == other.rank
        return False
    
    def __lt__(self, other):
        return self.rank < other.rank

    def __le__(self, other):
        return (self < other) and (self == other)
    
    def __str__(self):
        suit = ""
        rank = ""
        match self.suit:
            case 0: suit = "♥"
            case 1: suit = "♦"
            case 2: suit = "♣"
            case 3: suit = "♠"
            case _: suit = "?"
        match self.rank:
            case 1:  rank = "A"
            case 11: rank = "J"
            case 12: rank = "Q"
            case 13: rank = "K"
            case _:  rank = str(self.rank)
        return suit+rank

class Hand:
    def __init__(self, hand=[]):
        self.hand = hand.copy()
        self.doubled = False
    
    def addCard(self, card):
        """Adds a card to the hand"""
        self.hand.append(card)
    
    def aces(self):
        """Counts the number of aces in a hand"""
        no_aces = 0
        for card in self.hand:
            if card.rank == ACE:
                no_aces += 1
        return no_aces
    
    def pair(self):
        return len(self.hand) == 2 and self.hand[0].rank == self.hand[1].rank
    
    def scoreHand(self):
        """Returns the highest score of the current hand as long as it is under 21 (if possible)"""
        score = 0
        for card in self.hand:
            if card.rank == ACE:
                score += 11
            else:
                score += min(card.rank, 10)
        for _ in range(self.aces(),0,-1):
            if score > 21:
                score -= 10
        return score
    
    def isBlackjack(self):
        """Returns true if the hand is blackjack, false otherwise"""
        return self.scoreHand() == 21 and len(self.hand) == 2
    
    def isBust(self):
        """Returns true if there is no way for the hand to have a score below 21, false otherwise"""
        score = self.scoreHand()
        return not (score <= 21)

    def __str__(self):
        return str([str(i) for i in self.hand])

RESHUFFLE_CARD = Card(-1, -1)

##############################
# BLACKJACK CLASS DEFINITION #
##############################
MIN_BET = 2
MAX_BET = 500

class Blackjack:
    """Blackjack class contains:
        - deck ([Card]): a deck of n*52 cards
        - no_decks (int): the number of decks in the shoe
        - played ([Card]): a list of all cards played during this round (can later be used for counting purposes)

        Player variables:
        - player_hand (Hand): contains all the cards in the player's hand
        - player_money (int): the money currently in possesion of the player
        - player_bet (int): how much the player is betting in a round
        
        Dealer variables:
        - dealer_hand (Hand)
        - dealer_reshuffle (bool): true if the dealer should reshuffle at the end of the round"""
    def __init__(self, no_decks=1):
        # Initialise deck for the game
        deck = []
        for _ in range(no_decks):
            deck += self.newDeck()
        self.shoe = deck
        random.shuffle(self.shoe)
        self.no_decks = no_decks

        # Initialise list of played cards
        self.played = []

        # Initialise variables for the player
        self.player_hands = []
        self.player_money = 200
        self.player_bet = 0

        # Initialise variables for the dealer
        self.dealer_hand = Hand()
        self.dealer_reshuffle = False

    def startGame(self):
        self.player_hands.append(Hand([self.drawCard(), self.drawCard()]))
        self.dealer_hand = Hand([self.drawCard(), self.drawCard()])
        if self.dealer_hand.isBlackjack():
            self.player_hands = [GameState.Dealer_won]
        return (self.player_hands, self.dealer_hand)
    
    def getAllAgentHands(self):
        return self.player_hands
    
    def agentAction(self, hand_index, action):
        match action:
            case Actions.HT:
                self.agentHits(hand_index)
            case Actions.ST:
                self.agentStands(hand_index)
            case Actions.SP:
                old_hand = self.player_hands[hand_index]
                if old_hand.pair():
                    new_hand_1 = Hand([old_hand[0], self.drawCard()])
                    new_hand_2 = Hand([old_hand[1], self.drawCard()])
                    self.player_hands[hand_index] = new_hand_1
                    self.player_hands.append(new_hand_2)
                else:
                    raise SplitError
            case Actions.DH:
                if len(self.player_hands[hand_index].hand) == 2:
                    self.agentDoublesDown(hand_index)
                else:
                    self.agentHits(hand_index)
            case Actions.DS:
                if len(self.player_hands[hand_index].hand) == 2:
                    self.agentDoublesDown(hand_index)
                else:
                    self.agentStands(hand_index)
    
    def agentDoublesDown(self, hand_index):
        drawn = self.drawCard()
        self.player_hands[hand_index].addCard(drawn)
        self.player_hands[hand_index].doubled = True
        self.dealerDrawsUntil17()
        self.defineIfAgentWon(hand_index)
    
    def agentHits(self, hand_index):
        drawn = self.drawCard()
        self.player_hands[hand_index].addCard(drawn)
        if self.player_hands[hand_index].isBust():
            self.player_hands[hand_index] = GameState.Dealer_won
        elif self.player_hands[hand_index].scoreHand() == 21:
            if self.player_hands[hand_index].doubled:
                self.player_hands[hand_index] = GameState.Agent_won_doubledown
            else:
                self.player_hands[hand_index] = GameState.Agent_won

    
    def agentStands(self, hand_index):
        self.dealerDrawsUntil17()
        self.defineIfAgentWon(hand_index)
        

    def defineIfAgentWon(self, hand_index):
        player_score = self.player_hands[hand_index].scoreHand()
        dealer_score = self.player_hands[hand_index].scoreHand()
        if player_score < dealer_score:
            self.player_hands[hand_index] = GameState.Dealer_won_doubledown if self.player_hands[hand_index].doubled else GameState.Dealer_won
        elif player_score == dealer_score:
            self.player_hands[hand_index] = GameState.Agent_draw
        elif player_score > dealer_score:
            self.player_hands[hand_index] = GameState.Agent_won_doubledown if self.player_hands[hand_index].doubled else GameState.Agent_won
        else:
            raise Exception("Whoopsies!")
    
    def dealerDrawsUntil17(self):
        dealing = True
        while dealing:
            dealer_score = self.dealer_hand.scoreHand()
            if dealer_score <= 16:
                drawn = self.drawCard()
                self.dealer_hand.addCard(drawn)
            elif dealer_score > 16 and not self.dealer_hand.isBust():
                dealing = False
            else: # Dealer is bust
                dealing = False

    def resetRound(self):
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.player_bet = 0
        if self.dealer_reshuffle:
            deck = []
            for _ in self.no_decks:
                deck += self.newDeck()
            self.shoe = deck
            random.shuffle(self.shoe)

    def newDeck(self):
        """Generates a new deck containing all 52 basic cards (so no jokers)"""
        deck = []
        for suit in range(0,4):
            for rank in range(1,14):
                deck.append(Card(suit, rank))
        return deck
    
    def drawCard(self):
        """Takes the last card (the top card) from the deck and returns it.
           Also adds this card to the played deck."""
        drawn = self.shoe[-1]
        self.shoe = self.shoe[:-1]
        self.played.append(drawn)
        if drawn == RESHUFFLE_CARD:
            self.dealer_reshuffle = True
            drawn = self.drawCard()
        return drawn
    
    def payout(self, verbose=False):
        player_score = self.player_hand.scoreHand()
        dealer_score = self.dealer_hand.scoreHand()

        pay = 0
        if self.player_hand.isBlackjack() and self.dealer_hand.isBlackjack():
            pay = 0
            print('Both player and dealer have Blackjack, so it\'s a tie!') if verbose else {}
        elif self.player_hand.isBlackjack():
            pay = int(1.5 * self.player_bet)
            print('Player has Blackjack, so is awarded 1.5 times their bet!') if verbose else {}
        elif not self.player_hand.isBust() and self.dealer_hand.isBust():
            pay = self.player_bet
            print('Dealer has gone bust and player has not, so player wins!') if verbose else {}
        elif self.player_hand.isBust():
            pay = -self.player_bet
            print('Player has gone bust, so the dealer wins!') if verbose else {}
        elif player_score > dealer_score:
            pay = self.player_bet
            print('Player has a higher hand than the dealer, so the player wins!') if verbose else {}
        elif player_score < dealer_score:
            pay = -self.player_bet
            print('Dealer has a higher hand than the player, so the dealer wins!') if verbose else {}
        elif player_score == dealer_score:
            pay = 0
            print('Dealer and player have the same score, so it\'s a tie!') if verbose else {}
        else:
            raise Exception('Unknown case hit during payout! Check what happened')
        
        self.player_money += pay
        if verbose and pay > 0:
            print(f'Player won €{pay}.')
        elif verbose and pay < 0:
            print(f'Player lost €{pay}.')
        return pay     
    
    def playGameInteractive(self):
        rounds = 1
        while self.player_money > MIN_BET:
            # Round start
            print(f'--------------\nROUND {rounds}\n--------------')

            # Bet placement
            self.player_bet = 0
            while self.player_bet < MIN_BET or self.player_bet > MAX_BET or self.player_bet > self.player_money:
                self.player_bet = int(input(f'Place your bets! (You have €{self.player_money})\n> '))
                if self.player_bet < MIN_BET:
                    print(f'Bet too low! Minimum bet size is {MIN_BET}')
                elif self.player_bet > MAX_BET:
                    print(f'Bet too high! Maximum bet size is {MAX_BET}')
                elif self.player_bet > self.player_money:
                    print(f'You do not have enough money! Please try again.')
            
            # Deal cards
            self.player_hand = Hand([self.drawCard(), self.drawCard()])
            self.dealer_hand = Hand([self.drawCard(), self.drawCard()])
            print(f'Dealer\'s up card: {self.dealer_hand.hand[0]}')
            print(f'Players\'s hand: {str(self.player_hand)}')
            
            # Player plays their round 
            playing = True
            def player_hits():
                drawn = self.drawCard()
                self.player_hand.addCard(drawn)
                print(f'You drew a {drawn}!')
                print(f'Player\'s hand: {self.player_hand} (score: {self.player_hand.scoreHand()})')
                if self.player_hand.isBust():
                    nonlocal playing 
                    playing = False
                    print(f'Your hand is bust!\n')

            def player_stands():
                nonlocal playing
                print(f'Player stands on {self.player_hand.scoreHand()}.\n')
                playing = False

            if self.player_hand.isBlackjack():
                print(f'You have Blackjack!')
                playing = False

            while playing:
                match input(f'Do you want to hit (h) or stand (s)?\n> '):
                    case 'h'|'H': player_hits()
                    case 's'|'S': player_stands()
                    case _      : print('Please input either \'h\' or \'s\'.')
            
            # Dealer plays their round
            playing = True
            print(f'Dealer\'s hand: {self.dealer_hand} (score: {self.dealer_hand.scoreHand()})')
            if self.dealer_hand.isBlackjack():
                print('Dealer has Blackjack!')
            while playing:
                dealer_score = self.dealer_hand.scoreHand()
                if dealer_score <= 16:
                    drawn = self.drawCard()
                    self.dealer_hand.addCard(drawn)
                    print(f'Dealer drew a {drawn}!\nDealer\'s hand: {self.dealer_hand} (score: {self.dealer_hand.scoreHand()})')
                elif dealer_score > 16 and not self.dealer_hand.isBust():
                    print(f'Dealer stands on {dealer_score}!')
                    playing = False
                else:
                    print(f'Dealer is bust!')
                    playing = False
            
            # Payout
            self.payout(verbose=True)
            self.resetRound()
            rounds += 1
            print('')
        print('You ran out of money! Game over...')

    def __str__(self):
        string = "Game state:\n" + str([str(card) for card in self.deck])
        return string
    
class SplitError(Exception):
    def __init__(self, message="Player attempted to split non-splittable hand."):
        super().__init__(message)
    
if __name__ == "__main__":
    state = Blackjack()
    state.playGameInteractive()