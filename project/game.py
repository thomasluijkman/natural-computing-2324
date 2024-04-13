import random

################################
# SINGLE CARD CLASS DEFINITION #
################################
ACE = 1
JACK = 11
QUEEN = 12
KING = 13

class Card:
    """A card is defined by two numbers: 
    Suit -- 0 = hearts, 1 = diamonds, 2 = clubs, 3 = spades
    Rank -- 1 = ace, 11 = jack, 12 = queen, 13 = king (all other numbers are obvious)
    """
    def __init__(self, suit, rank):
        if rank > 13 or rank < 1:
            raise ValueError(f"Rank value of {rank} is invalid.")
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
    def __init__(self):
        self.hand = []
    
    def addCard(self, card):
        self.hand.append(card)
    
    def aces(self):
        no_aces = 0
        for card in self.hand:
            if card.rank == ACE:
                no_aces += 1
        return no_aces
    
    def scoreHand(self):
        score = 0
        for card in self.hand:
            if card.rank == ACE:
                score += 11
            else:
                score += min(card.rank, 10)
        return score
    
    def isBlackjack(self):
        return self.scoreHand == 21 and len(self.hand) == 2
    
    def isBust(self):
        score = self.scoreHand()
        for _ in range(self.aces(),0,-1):
            if score > 21:
                score -= 10
        return not (score <= 21)


##############################
# BLACKJACK CLASS DEFINITION #
##############################
class Blackjack:
    def __init__(self, no_decks):
        deck = []
        for _ in no_decks:
            deck += self.newDeck()
        self.deck = deck

    def newDeck(self, shuffle=True):
        deck = []
        for suit in range(0,4):
            for rank in range(1,14):
                deck.append(Card(suit, rank))
        return deck
    
    def __str__(self):
        string = "Game state:\n" + str([str(card) for card in self.deck])
        return string

