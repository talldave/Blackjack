#!/usr/bin/env python

# Text-based Blackjack
# David Bianco
# July 2014

#from __future__ import print_function
import random

total_player_count = 2    # includes Dealer
player = []
hand = []
debug = False #True

class Player:
    position = -1

    def __init__(self, name, pot):
        self.name = name
        Player.position += 1
        self.pot = pot
        self.bet = 0
        self.hand = 0
        self.cards = []
        self.action = ""

    def __getitem__(self, key):
        return self.data[key]

    def reset(self):
        self.hand = 0
        self.cards = []

class Deck:
    deck = []
    def __init__(self):
        self.reset()

    def reset(self, total_deck_count=1):
        ranks = (2,3,4,5,6,7,8,9,10,'J','Q','K','A')
        self.deck = list(ranks * 4)
        self.deck *= total_deck_count
        if (debug): print self.deck
        self.shuffle()
        #random.shuffle(self.deck)
        if (debug): print self.deck
        self.deck.pop(0) # burn card
        #self.cards_in_deck = len(self.deck)

    def shuffle(self):
        random.shuffle(self.deck)
        print "The deck has been shuffled."

    def count(self):
        return len(self.deck)

    def deal_card(self, i):
        dealt_card = self.deck.pop(0)

        if dealt_card < 11:
            dealt_card_value = dealt_card
        elif dealt_card == 'A':
            dealt_card_value = 11
        else:
            dealt_card_value = 10

        #player[i].cards.append(dealt_card)
        #player[i].hand += dealt_card_value
        hand[i].cards.append(dealt_card)
        hand[i].value += dealt_card_value
        if (debug): print "%s's card: %s" % (player[i].name, dealt_card)

        return (dealt_card, dealt_card_value)

class Hand:

    def __init__(self):
        self.reset()

    def reset(self):
        self.value = 0
        self.cards = []
        self.aces = 0
        self.ten = 0
        self.pair = 0

    def evaluate(self):
        #hand = hand[i].value
        #cards = hand[i].cards
        if self.value >= 22:
            #while card in self.cards:
            for card in self.cards:
                if card == 'A':
                   self.value -= 10
                   if self.value <= 21: break
                #self.evaluate()
            if self.value >= 22:
                print "BUST!"
        elif ((len(self.cards) == 2) and (self.aces == 1) and (self.ten == 1)):
            print "BLACKJACK!"
        elif ((len(self.cards) == 2) and (self.cards[0] == self.cards[1])):
            self.pair = 1

    def show(self, i):
        print "%s's cards: " % player[i].name,
        #for card in self.cards:
        for a, card in enumerate(self.cards):
            if a == 0 and len(self.cards) < 3:
                if i == len(player)-1:
                    print "X",
                else:
                    print "%s" % card,
            else:
                print "- %s" % card,
        print

class Card:
    def __init__(self, suit, face, value, color):
        self.suit = suit
        self.face = face
        self.value = value
        self.color = color
        self.visible = True


def rules():
    print "WELCOME TO BLACKJACK!"
    print "Dealer must hit at 16 and below."
    print "Blackjack pays 2:1, a win pays 1:1"

def play_game():
    for i in range(0,2):
        print
        for j in range(0, total_player_count):
            #player[j].hand += dealt_card_value
            deck.deal_card(j)
            #player[j].hand += dealt_card_value
            #print "%s's card: %s" % (player[j].name, dealt_card)


    print
    for i in range(0, total_player_count):
        hand[i].show(i)

    for i in range(0, total_player_count):
        if (debug): print "%s's hand: %d" % (player[i].name, hand[i].value)
        if i == len(player)-1:
            dealer_move(i)
        else:
            player_move(i)
    play_again()

def player_move(i):
    question = "Would you like to (h)it or (s)tand: "
    action = raw_input(question)
    if action in ('h', 'H'):
        deck.deal_card(i)
        hand[i].show(i)
        hand[i].evaluate()
        player_move(i)
    elif action in ('s', 'S'):
        pass
    else:
        print "'%s' is not valid" % action
        player_move(i)

def dealer_move(d):
    #d = len(player)
    dealer_hand = hand[d].value
    if (debug): print "Dealer has %d." % dealer_hand
    if dealer_hand < 17:
        print "Dealer must hit."
        deck.deal_card(d)
        hand[d].show(d)
        hand[d].evaluate()
        dealer_move(d)
    elif dealer_hand < 21:
        print "Dealer stays."
        pass
    elif dealer_hand >= 22:
        print "BUST!!!!"

def evaluate_hand(i):
    hand = hand[i].value
    cards = hand[i].cards
    if hand >= 22:
        if 'A' in cards:
            player[i].hand -= 10
            evaluate_hand(i)
        else:
            print "BUST!"
    elif ((len(cards) == 2) and ('A' in cards) and ('J' in cards)):
        pass


def play_again():
    if (debug): print "%d cards left in the deck" % deck.count()
    question = "Would you like to play again? (y/n) "
    play_again = raw_input(question)
    if play_again in ('y', 'Y'):
        for i in range(0, total_player_count):
            hand[i].reset()
        if deck.count() < 15:
            deck.reset()
        play_game()
    else:
        print "Thank you for playing!"
        exit()


def place_bet(i):
    question = "How many chips would you like to bet? (1-%d) " % player[i].pot
    player[i].bet = int(raw_input(question))
    if player[i].bet < 1 or player[i].bet > player[i].pot:
        print "Invalid bet."
        place_bet()

def init_player():
    ''' init Player(s) '''
    for i in range(1, total_player_count):
        question = "Enter the name of Player #%d: " % i
        name = raw_input(question)
        initial_pot = 100
        player.append(Player(name, initial_pot))
        hand.append(Hand())

def init_dealer():
    ''' init Dealer '''
    player.append(Player('Dealer', 1000000))
    hand.append(Hand())
    return random.choice(('Sam', 'Jim', 'Lucy', 'Sara'))

#init_deck()
rules()
deck = Deck()
init_player()
dealer_name = init_dealer()
print "Hi %s, %s will be your dealer today." % (player[0].name, dealer_name)
place_bet(0)

play_game()

