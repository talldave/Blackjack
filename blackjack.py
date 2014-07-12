#!/usr/bin/env python

# blackjack.py
### Text-based Blackjack
# David Bianco
# July 2014

import random
import time
import os
#import curses

debug = False
#debug = True

VERSION = 1.0

# # #  BEGIN CLASS # # #

class Player:

    def __init__(self, name=False):
        self.reset()

        if not name:
            self.name = require_input('name')
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
        self.pair = False
        self.bust = False
        self.show_first_card = False

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

        if debug:
            print "(debug) Dealt card: %s" % dealt_card
            print "(debug) Dealt card value: %d" % dealt_card_value

    def show(self):
        print "\n%s's cards: " % self.name,

        for i, card in enumerate(self.cards):
            if i == 0:
                if self.is_dealer and self.show_first_card == False:
                    print "X",
                    self.show_first_card = True
                else:
                    print "%s" % str(card).upper(),
            else:
                print "- %s" % str(card).upper(),
        print

    def evaluate_hand(self):
        if self.hand > 21:
            for i, card in enumerate(self.cards):
                if card == 'A':
                   self.hand -= 10
                   self.cards[i] = 'a'
                   if self.hand <= 21:
                       break
            if self.hand > 21:
                self.bust = True
        elif ((len(self.cards) == 2) and (self.hand == 21)):
            self.blackjack = True
        elif ((len(self.cards) == 2) and (self.cards[0] == self.cards[1])):
            self.pair = True

        if debug:
            print "(debug) Evaluate hand: %d" % self.hand
            print "(debug) BUST: %s | BJ: %s | PAIR: %s" % (self.bust, self.blackjack, self.pair)


class Deck:

    def __init__(self, ranks = (2,3,4,5,6,7,8,9,10,'J','Q','K','A'), shuffle = True):
        try:
            deck_count = int(require_input('num_decks'))
        except ValueError:
            deck_count = 1

        if not (0 < deck_count < 9):
            deck_count = 1

        if deck_count == 1:
            print "You will be playing with 1 deck."
        else:
            print "You will be playing with %d decks.  Good luck!" % deck_count

        self.suspense = 2  # number of seconds to sleep before card is dealt. try 0, 1 or 2
        self.num_decks = deck_count
        self.reset(ranks, shuffle)

    def reset(self, ranks = (2,3,4,5,6,7,8,9,10,'J','Q','K','A'), shuffle = True):
        self.deck = list(ranks * 4)
        self.deck *= self.num_decks

        if debug:
            print "(debug) " + str(self.deck)

        if shuffle:
            self.shuffle()
            if debug:
                print "(debug) " + str(self.deck)

        self.deck.pop(0) # burn card

    def shuffle(self):
        random.shuffle(self.deck)
        print "The deck has been shuffled."

    def num_cards(self):
        return len(self.deck)

# # #  END CLASS # # #

# # #  BEGIN FUNCTIONS # # #

def welcome():
    ''' print welcome message '''

    print r"""
 ____  _            _    _            _
|  _ \| |          | |  (_)          | |
| |_) | | __ _  ___| | ___  __ _  ___| | __
|  _ <| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
| |_) | | (_| | (__|   <| | (_| | (__|   <
|____/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\
                       _/ |
                      |__/
    """

    print "\nWELCOME TO BLACKJACK!"
    print "Dealer must hit at 16 and below."
    print "Double Down only on first 2 cards."
    print "Blackjack pays 2:1, a win pays 1:1\n"
    print "Hi %s, %s will be your dealer today." % (player1.name, random.choice(('Sam', 'Jim', 'Lucy', 'Sara')))

def place_bet(test_response = [], num_response = 0):
    ''' Ask player to place their bet. '''

    invalid_response = False
    if debug:
        print "(debug) Expected bet: %s " % str(test_response)
    if test_response:
        test_resp = test_response.pop(0)
    else:
        test_resp = False

    try:
        response = require_input('bet', test_resp)
        player1.bet = int(response)
    except ValueError:
        invalid_response = True

    if num_response > 3:
        print "It seems you don't understand the question.  Let's play again another time."
        end_game()

    if not (1 <= player1.bet <= player1.pot):
        invalid_response = True

    if invalid_response:
        num_response += 1
        print "Invalid bet."
        place_bet(test_response, num_response)

def play_game():
    ''' Deal first 2 cards.  Player moves, then dealer moves, then compare hands.  '''

    place_bet()

    for i in range(2):
        for player in players:
            player.deal_card()

    for player in players:
        player.show()
        player.evaluate_hand()

    if dealer.blackjack:
        dealer.show()

    if not player1.blackjack and not dealer.blackjack:
        for player in players:
            if player.is_dealer:
                dealer_move()
            else:
                player_move()

            if player.bust:
                break

    end_hand()

    if play_again():
        play_game()
    else:
        end_game()

def require_input(ask, response = False):
    ''' Function to ask for player input.  Also allows for passed-in response for testing '''

    if ask == 'play_again':
        question = "----> Would you like to play again? (y/n) "
    elif ask == 'hit_stand_double':
        question = "----> Would you like to (h)it or (s)tand or (d)ouble down: "
    elif ask == 'hit_stand':
        question = "----> Would you like to (h)it or (s)tand: "
    elif ask == 'name':
        question = "\n----> Please enter your name: "
    elif ask == 'bet':
        question = "\n----> How many chips would you like to bet? (1-%d) " % player1.pot
    elif ask == 'num_decks':
        question = "\n----> How many decks would you like to play with? (1-8) "

    if response:
        print question + str(response)
        return response
    else:
        return raw_input(question)

def player_move(test_response = False, invalid_response = 0):
    ''' Ask player to hit, stand, or double-down.  Hand is lost if bust. '''

    if debug:
        print "(debug) Expected play: %s" % str(test_response)

    if test_response:
        test_resp = test_response.pop(0)
    else:
        test_resp = False

    if invalid_response > 3:
        print "It seems you don't understand the question.  Let's play again another time."
        end_game()

    if len(player1.cards) == 2 and player1.pot >= player1.bet * 2:
        action = require_input('hit_stand_double', test_resp)
        valid_response = ['h', 'H', 'd', 'D']
    else:
        action = require_input('hit_stand', test_resp)
        valid_response = ['h', 'H']

    if action in valid_response:
        if action in ('d', 'D'):
            player1.bet *= 2
            print "Your bet is now %d." % player1.bet

        time.sleep(deck.suspense)
        player1.deal_card()
        player1.show()
        player1.evaluate_hand()

        if player1.bust:
            return
        elif action in ('h', 'H'):
            player_move(test_response)

    elif action not in ('s', 'S'):
        invalid_response += 1
        print "'%s' is not a valid response." % action
        player_move(test_response, invalid_response)

def dealer_move():
    ''' Dealer < 17, hit. 16 < Dealer < 22, stay. Dealer > 21, bust. '''

    dealer.show()
    print "Dealer has %s." % dealer.hand,

    if dealer.hand < 17:
        print "Dealer must hit."
        time.sleep(deck.suspense)
        dealer.deal_card()
        dealer.evaluate_hand()
        dealer_move()
    elif dealer.hand < 22:
        print "Dealer stays."
    else:
        print

def end_hand():
    ''' Compare player hand to dealer hand, and do bet math. '''

    print "\n#*#*#",

    if player1.bust:
        print "BUST! Dealer wins.",
        player1.pot -= player1.bet
        player1.num_losses += 1
    elif dealer.bust:
        print "BUST!!!! You win.",
        player1.pot += player1.bet
        player1.num_wins += 1
    elif dealer.blackjack and player1.blackjack:
        print "Both you and the dealer have Blackjack.  Push.",
        player1.num_pushes += 1
    elif dealer.blackjack and not player1.blackjack:
        print "Dealer has blackjack!",
        player1.pot -= player1.bet
        player1.num_losses += 1
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

def play_again(test_response = False):
    ''' Current hand has just ended, ask if player would like to continue '''

    if debug:
        print "(debug) %d cards left in the deck" % deck.num_cards()

    if player1.pot == 0:
        print "Sorry, but you have no chips left."
        return False
    else:
        print "You have %d chips remaining." % player1.pot
        play_again = require_input('play_again', test_response)

        if play_again in ('y', 'Y'):
            if not debug:
                os.system('clear') # clear screen. 'cls' for windows
            else:
                print 80*'~'

            for player in players:
                player.reset()

            if deck.num_cards() < 15:
                deck.reset()

            return True
        else:
            return False

def end_game():
    ''' Tally wins/losses.  Exit game. '''

    total_games = player1.num_wins + player1.num_losses + player1.num_pushes

    if total_games == 1:
        game_word = "game"
    else:
        game_word = "games"

    print "\nYou played %d %s." % (total_games, game_word)
    print "Won: %d | Lost: %d | Push: %d" % (player1.num_wins, player1.num_losses, player1.num_pushes)
    print "You have %d chips left." % player1.pot
    print "Thank you for playing!"
    exit()


# # #  END FUNCTIONS # # #

if __name__ == '__main__':
    player1 = Player()
    dealer = Player('Dealer')
    players = [player1, dealer]

    welcome()
    deck = Deck()

    play_game()

