from enum import Enum
import random

class Suit(Enum):
    club = 0
    diamond = 1
    heart = 2
    spade = 3

class Rank(Enum):
    ace = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    jack = 11
    king = 12
    queen = 13

class Card:
    def __init__(self, id, suit, rank, value):
        self.id = id
        self.suit = suit
        self.rank = rank
        self.value = value

def get_deck(suits:Suit, ranks:Rank) -> list[Card]:
    #Constructs a list of Card which contains every rank in every suit
    deck = []
    for s in suits:
        for r in ranks:
            #For ranks 1-9 the value and id is just the rank
            value = int(r.value)
            id = '' + str(r.value)
            match r:
                #Case of picture card
                case Rank.jack | Rank.king | Rank.queen:
                    value = 10
                    id = id[:-2] #Remove the value from id
                    id += r.name.upper()[0] #ID as the first letter of the rank (upper case)
                #Case of ace
                case Rank.ace:
                    value = 1 #Default value of 1
                    id = id[:-1] #Remove value from id
                    id += 'A'
            
            id += s.name.upper()[0] #Add suit to id
            
            deck.append(Card(id, s, r, value))
    return deck

def shuffle_deck(deck:list): #Included this so that random module is not needed to import, only this module
    random.shuffle(deck)
    return deck

def print_deck(deck):
    for card in deck:
        print(f'{card.suit.name} {card.rank.name}: {card.id}')


suits = [Suit.club, Suit.diamond, Suit.heart, Suit.spade]
ranks = [Rank.ace, Rank.two, Rank.three, Rank.four, Rank.five, Rank.six, Rank.seven, Rank.eight, Rank.nine, Rank.ten, Rank.jack, Rank.king, Rank.queen]

deck = get_deck(suits, ranks)