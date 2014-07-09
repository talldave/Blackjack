#!/usr/bin/env python

# blackjack.py
### Text-based Blackjack
# David Bianco
# July 2014

import random
import time
#import curses
import os

#debug = True
debug = False
sleep_seconds = 2

# # #  BEGIN CLASS # # #

class Player:

    def __init__(self, name=False):
        self.reset()
        if not name:
            self.name = raw_input("----> Please enter your name: ")
            self.pot = 100
            self.bet = 0
            self.num_wins = 0
            self.num_losses = 0
            self.num_pushes = 0
            self.is_dealer = False
        else:
            self.name = name
            self.is_dealer = True

    def reset(self):
        self.hand = 0
        self.cards = []
        self.blackjack = False
        self.bust = False
        self.show_first = False

    def deal_card(self):
        dealt_card = deck.deck.pop(0)

        if dealt_card < 11:
            dealt_card_value = dealt_card
        elif dealt_card == 'A':
            dealt_card_value = 11
        else:
            dealt_card_value = 10

        self.cards.append(dealt_card)
        self.hand += dealt_card_value

        if debug: print "%s's card: %s" % (self.name, dealt_card)

    def show(self):
        print "\n%s's cards: " % self.name,

        for i, card in enumerate(self.cards):
            if i == 0:
                if self.is_dealer and self.show_first == False:
                    print "X",
                    self.show_first = True
                else:
                    print "%s" % str(card).upper(),
            else:
                print "- %s" % str(card).upper(),
        print

    def evaluate_hand(self):
        if debug: print "curr value %s" % self.value
        if debug: print self.cards
        if self.hand >= 22:
            for i, card in enumerate(self.cards):
                if debug: print "card %d: %s" % (i,card)
                if card == 'A':
                   self.hand -= 10
                   self.cards[i] = 'a'
                   if debug: print self.cards
                   if debug: print "new value %s" % self.hand
                   if self.hand <= 21: break
            if self.hand >= 22:
                self.bust = True
        elif ((len(self.cards) == 2) and (self.hand == 21)):
            self.blackjack = True
        elif ((len(self.cards) == 2) and (self.cards[0] == self.cards[1])):
            self.pair = True


class Deck:
    deck = []

    def __init__(self):
        try:
            deck_count = int(raw_input("\n----> How many decks would you like to play with today? (1-8) "))
        except ValueError:
            deck_count = 1
        if not (0 < deck_count < 9):
            deck_count = 1
        if deck_count == 1:
            print "You will be playing with 1 deck today."
        else:
            print "You will be playing with %d decks today.  Good luck!" % deck_count
        wait = raw_input("Press any key to start playing.")
        self.num_decks = deck_count
        self.reset()

    def reset(self):
        ranks = (2,3,4,5,6,7,8,9,10,'J','Q','K','A')
        #ranks = (2,'A','A','A','A','J','J',6,'A',6,'A',8,6,6) # test
        #ranks = (2,'A',10,10,10,9,'A',10,10,'A',10,'A') #test
        self.deck = list(ranks * 4)
        self.deck *= self.num_decks
        if debug: print self.deck
        self.shuffle()
        self.deck.pop(0) # burn card
        if debug: print self.deck

    def shuffle(self):
        random.shuffle(self.deck)
        print "The deck has been shuffled."

    def num_cards(self):
        return len(self.deck)

# # #  END CLASS # # #

# # #  BEGIN FUNCTIONS # # #

def rules():
    print "\nWELCOME TO BLACKJACK!"
    print "Dealer must hit at 16 and below."
    print "Blackjack pays 2:1, a win pays 1:1\n"

def play_game():
    os.system('clear') # clear screen
    place_bet()

    for i in range(2):
        print
        for player in players:
            player.deal_card()

    print
    for player in players:
        player.show()

    for player in players:
        if debug:
            print "%s's hand: %d" % (player.name, player.hand)
        if player.is_dealer:
            dealer_move()
        else:
            player_move()

    end_game()
    play_again()

def place_bet(num_response = 0):
    invalid_response = False

    try:
        question = "\n----> How many chips would you like to bet? (1-%d) " % player1.pot
        player1.bet = int(raw_input(question))
    except ValueError:
        invalid_response = True

    if num_response > 3:
        print "It seems you don't understand the question.  Let's play again another time."
        exit()

    if not (1 <= player1.bet <= player1.pot):
        invalid_response = True

    if invalid_response:
        num_response += 1
        print "Invalid bet."
        place_bet(num_response)

def player_move():
    player1.evaluate_hand()
    if player1.blackjack: return
    action = raw_input("----> Would you like to (h)it or (s)tand: ")
    if action in ('h', 'H'):
        time.sleep(sleep_seconds)
        player1.deal_card()
        player1.show()
        player1.evaluate_hand()
        if player1.bust:
            print "\n\n#*#*# BUST! Dealer wins. #*#*#\n"
            player1.pot -= player1.bet
            player1.num_losses += 1
            play_again()
        else:
            player_move()
    elif action in ('s', 'S'):
        print
    else:
        print "'%s' is not valid" % action
        player_move()

def dealer_move():
    dealer.show()
    dealer.evaluate_hand()
    if dealer.blackjack: return
    print "Dealer has %s." % dealer.hand,

    if dealer.bust:
        print "\n\n#*#*#*# BUST!!!! You win. #*#*#\n"
        player1.num_wins += 1
        player1.pot += player1.bet
        play_again()

    if dealer.hand < 17:
        print "Dealer must hit."
        time.sleep(sleep_seconds)
        dealer.deal_card()
        dealer_move()
    elif dealer.hand < 22:
        print "Dealer stays."

def end_game():
    print "\n#*#*#",
    if dealer.blackjack and player1.blackjack:
        print "Both you and the dealer have Blackjack.  Push.",
        player1.num_pushes += 1
    elif dealer.blackjack and not player1.blackjack:
        print "Dealer has blackjack!",
        player1.num_losses += 1
        player1.pot -= player1.bet
    elif not dealer.blackjack and player1.blackjack:
        print "You have blackjack!!",
        player1.pot += player1.bet * 2
        player1.num_wins += 1
    elif player1.hand == dealer.hand:
        print "PUSH",
        player1.num_pushes += 1
    elif player1.hand < dealer.hand:
        print "Dealer wins.",
        player1.pot -= player1.bet
        player1.num_losses += 1
    elif player1.hand > dealer.hand:
        print "You win!",
        player1.pot += player1.bet
        player1.num_wins += 1
    print "#*#*#\n"

def play_again():
    ''' Current hand has just ended, ask if player would like to continue '''
    if debug:
        print "%d cards left in the deck" % deck.num_cards()

    if player1.pot == 0:
        print "Sorry, but you have no chips left."
    else:
        play_again = raw_input("----> Would you like to play again? (y/n) ")

        if play_again in ('y', 'Y'):
            for player in players:
                player.reset()
            if deck.num_cards() < 15:
                deck.reset()
            play_game()

    total_games = player1.num_wins + player1.num_losses + player1.num_pushes
    print "\nYou played %d games." % total_games
    print "Won: %d | Lost: %d | Push: %d" % (player1.num_wins, player1.num_losses, player1.num_pushes)
    print "You have %d chips left." % player1.pot
    print "Thank you for playing!"
    exit()

# # #  END FUNCTIONS # # #

player1 = Player()
dealer = Player('Dealer')
players = [player1, dealer]

rules()
print "Hi %s, %s will be your dealer today." % (player1.name, random.choice(('Sam', 'Jim', 'Lucy', 'Sara')))
deck = Deck()

play_game()


