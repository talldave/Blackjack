#!/usr/bin/env python

import random

total_player_count = 2    # includes Dealer
total_deck_count = 1
player = []
deck = []

class Player:

    position = -1

    def __init__(self, name, pot):
        self.name = name
        Player.position += 1
        self.pot = pot
        self.bet = 0
        self.hand = 0
        self.action = ""

    def __getitem__(self, key):
        return self.data[key]

class Deck:
    deck = []
    def __init__(self):
        self.reset()

    def reset(self):
        ranks = (2,3,4,5,6,7,8,9,10,'J','Q','K','A')
        self.deck = list(ranks * 4)
        self.deck *= total_deck_count
        print self.deck
        self.shuffle()
        random.shuffle(self.deck)
        print self.deck
        self.deck.pop(0) # burn card
        self.cards_in_deck = len(self.deck)

    def shuffle(self):
        random.shuffle(self.deck)
        print "The deck has been shuffled."

    def count(self):
        return len(self.deck)

    def deal_card(self):
        dealt_card = self.deck.pop(0)
        if dealt_card < 11:
            dealt_card_value = dealt_card
        elif dealt_card == 'A':
            dealt_card_value = 11
        else:
            dealt_card_value = 10

        return (dealt_card, dealt_card_value)

class Card:
    def __init__(self, suit, face, value, color):
        self.suit = suit
        self.face = face
        self.value = value
        self.color = color
        self.visible = True


def play_game():
    for i in range(0,2):
        print
        for j in range(0, total_player_count):
            #player[j].hand += dealt_card_value
            dealt_card, dealt_card_value = deck.deal_card()
            player[j].hand += dealt_card_value
            print "%s's card: %s" % (player[j].name, dealt_card)

    print
    for i in range(0, total_player_count):
        print "%s's hand: %d" % (player[i].name, player[i].hand)

#question = "Would you like to (h)it or (s)tand: "
#action = raw_input(question)
#if action == 'h':
    #deal_card()


    print "%d cards left in the deck" % deck.count()
    question = "Would you like to play again? (y/n) "
    play_again = raw_input(question)
    if (play_again == 'y'):
        for i in range(0, total_player_count):
            player[i].hand = 0
        if deck.count() < 15:
            deck.reset()
        play_game()



def init_deck():
    ''' init deck '''
    ranks = (2,3,4,5,6,7,8,9,10,'J','Q','K','A')
    deck = list(ranks * 4)
    print deck
    random.shuffle(deck)
    print deck
    deck.pop(0) # burn card
#print "Card: %s" % deck[22]
#colors = ['Red','Black']
#suits = ['Hearts', 'Spades', 'Diamonds', 'Clubs']
#for a in range(0, total_deck_count):
        #for f in faces:
            #for s in suits:
                #deck.append(Card(s, f, v, c))


def init_player():
    ''' init Player(s) '''
    for i in range(1, total_player_count):
        question = "Enter the name of Player #%d: " % i
        name = raw_input(question)
        initial_pot = 100
        player.append(Player(name, initial_pot))

def init_dealer():
    ''' init Dealer '''
    player.append(Player('Dealer', 1000000))
    return random.choice(('Sam', 'Jim', 'Lucy', 'Sara'))

#init_deck()
deck = Deck()
init_player()
dealer_name = init_dealer()
print "Hi %s, %s will be your dealer today." % (player[0].name, dealer_name)
play_game()

