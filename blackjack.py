#!/usr/bin/env python

# Text-based Blackjack
# David Bianco
# July 2014

import random

player = []
hand = []
#debug = True
debug = False

class Player:

    def __init__(self, name, pot):
        self.name = name
        self.pot = pot
        self.bet = 0
        self.hand = 0
        self.cards = []
        self.action = ""
        self.num_wins = 0
        self.num_losses = 0
        self.num_pushes = 0
        self.total_games = 0
        self.is_dealer = False

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
        debug = False
        if debug:
            ranks = (2,'A','A','A','A','J','J',6,'A',6,'A',8,6,6)
            self.deck = list(ranks * 4)
        else:
            debug = True
            ranks = (2,3,4,5,6,7,8,9,10,'J','Q','K','A')
            self.deck = list(ranks * 4)
            self.deck *= total_deck_count
            if debug: print self.deck
            self.shuffle()
            #random.shuffle(self.deck)
            self.deck.pop(0) # burn card
        #self.cards_in_deck = len(self.deck)
        if debug: print self.deck

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
        if debug: print "%s's card: %s" % (player[i].name, dealt_card)

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
        self.show_first = False

    def evaluate(self):
        #hand = hand[i].value
        #cards = hand[i].cards
        if debug: print "curr value %s" % self.value
        if debug: print self.cards
        if self.value >= 22:
            #while card in self.cards:
            for i, card in enumerate(self.cards):
                if debug: print "card %d: %s" % (i,card)
                if card == 'A':
                   self.value -= 10
                   self.cards[i] = 'a'
                   if debug: print self.cards
                   if debug: print "new value %s" % self.value
                   if self.value <= 21: break
                #self.evaluate()
            if self.value >= 22:
                print "BUST!"
                play_again()
        elif ((len(self.cards) == 2) and (self.aces == 1) and (self.ten == 1)):
            print "BLACKJACK!"
            play_again()
        elif ((len(self.cards) == 2) and (self.cards[0] == self.cards[1])):
            self.pair = 1
        return self.value

    def show(self, i):
        print "\n%s's cards: " % player[i].name,
        #for card in self.cards:
        for a, card in enumerate(self.cards):
            if a == 0:
                if player[i].is_dealer and self.show_first == False:
                    print "X",
                    self.show_first = True
                else:
                    print "%s" % str(card).upper(),
            else:
                print "- %s" % str(card).upper(),
        print


def rules():
    print "\nWELCOME TO BLACKJACK!"
    print "Dealer must hit at 16 and below."
    print "Blackjack pays 2:1, a win pays 1:1\n"

def play_game():
    place_bet()
    for i in range(0,2):
        print
        for j in range(2):
            #player[j].hand += dealt_card_value
            deck.deal_card(j)
            #player[j].hand += dealt_card_value
            #print "%s's card: %s" % (player[j].name, dealt_card)


    print
    for i in range(2):
        hand[i].show(i)

    for i in range(2):
        if debug: print "%s's hand: %d" % (player[i].name, hand[i].value)
        if i == len(player)-1:
            dealer_move(i)
        else:
            player_move(i)
    end_game()
    play_again()

def end_game():
    if hand[0].value == hand[1].value:
        print "PUSH"
        player[0].num_pushes += 1
    elif hand[0].value < hand[1].value:
        print "Dealer wins."
        player[0].pot -= player[0].bet
        player[0].num_losses += 1
    elif hand[0].value > hand[1].value:
        print "You win!"
        player[0].pot += player[0].bet
        player[0].num_wins += 1

def player_move(i):
    question = "Would you like to (h)it or (s)tand: "
    action = raw_input(question)
    if action in ('h', 'H'):
        deck.deal_card(i)
        hand[i].show(i)
        hand[i].evaluate()
        player_move(i)
    elif action in ('s', 'S'):
        print
        pass
    else:
        print "'%s' is not valid" % action
        player_move(i)

def dealer_move(d):
    #d = len(player)
    dealer_hand = hand[d].evaluate()
    #dealer_hand = hand[d].value
    hand[d].show(d)
    print "Dealer has %s." % dealer_hand
    if dealer_hand < 17:
        print "Dealer must hit."
        deck.deal_card(d)
        #hand[d].show(d)
        hand[d].evaluate()
        dealer_move(d)
    elif dealer_hand < 22:
        print "Dealer stays."
        pass
    elif dealer_hand >= 22:
        print "BUST!!!!"

def play_again():
    ''' Current hand just ended, ask if player would like to continue '''
    if debug:
        print "%d cards left in the deck" % deck.count()

    if player[0].pot == 0:
        print "Sorry, but you have no chips left."
        exit()

    question = "Would you like to play again? (y/n) "
    play_again = raw_input(question)

    if play_again in ('y', 'Y'):
        for i in range(2):
            hand[i].reset()
        if deck.count() < 15:
            deck.reset()
        play_game()
    else:
        total_games = player[0].num_wins + player[0].num_losses + player[0].num_pushes
        print "You played %d games.\nWon: %d - Push: %d - Lost: %d" % (total_games, player[0].num_wins, player[0].num_losses, player[0].num_pushes)
        print "Thank you for playing!"
        exit()


def place_bet():
    q = 0
    invalid_response = False

    try:
        question = "How many chips would you like to bet? (1-%d) " % player[0].pot
        player[0].bet = int(raw_input(question))
    except ValueError:
        invalid_response = True

    if q > 3:
        print "It's obvious you don't understand the question.  Let's play again another time."
        exit()

    if not (1 <= player[0].bet <= player[0].pot):
        invalid_response = True

    if (invalid_response):
        q += 1
        print "Invalid bet."
        place_bet()

    q = 0

def init_player():
    ''' init Player '''
    question = "Please enter your name: "
    name = raw_input(question)
    initial_pot = 100
    player.append(Player(name, initial_pot))
    hand.append(Hand())

def init_dealer():
    ''' init Dealer '''
    player.append(Player('Dealer', 1000000))
    player[1].is_dealer = True
    hand.append(Hand())
    return random.choice(('Sam', 'Jim', 'Lucy', 'Sara'))

#init_deck()
rules()
deck = Deck()
init_player()
dealer_name = init_dealer()
print "Hi %s, %s will be your dealer today." % (player[0].name, dealer_name)

play_game()

