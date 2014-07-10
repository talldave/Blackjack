#!/usr/bin/env python

# blackjack.py
### Text-based Blackjack
# David Bianco
# July 2014

import random
import time
#import curses
import os

debug = True
#debug = False
sleep_seconds = 0    # use 1 or 2 for suspense

# # #  BEGIN CLASS # # #

class Player:

    def __init__(self, name=False):
        self.reset()
        if not name:
            self.name = raw_input("\n----> Please enter your name: ")
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


class Deck:
    deck = []

    def __init__(self):
        try:
            deck_count = int(raw_input("\n----> How many decks would you like to play with? (1-8) "))
        except ValueError:
            deck_count = 1

        if not (0 < deck_count < 9):
            deck_count = 1

        if deck_count == 1:
            print "You will be playing with 1 deck."
        else:
            print "You will be playing with %d decks.  Good luck!" % deck_count

        self.num_decks = deck_count
        self.reset()

    def reset(self):
        #ranks = (2,'A','J','J','A') # both dealer and player have blackjack
        #ranks = (2,'A','J','J','8') # only player has blackjack
        ranks = (2,'K','J','J','A') # only dealer has blackjack
        #ranks = (2,3,4,5,6,7,8,9,10,'J','Q','K','A')
        self.deck = list(ranks * 4)
        self.deck *= self.num_decks

        if debug:
            print self.deck

        #self.shuffle()

        if debug:
            print self.deck

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
    print "Blackjack pays 2:1, a win pays 1:1\n"
    print "Hi %s, %s will be your dealer today." % (player1.name, random.choice(('Sam', 'Jim', 'Lucy', 'Sara')))

def play_game():
    ''' Deal first 2 cards.  Player moves, then dealer moves, then compare hands.  '''

    place_bet()

    for i in range(2):
        for player in players:
            player.deal_card()

    for player in players:
        player.show()

    for player in players:
        if player.is_dealer:
            dealer_move()
        else:
            player_move()

    end_hand()
    play_again()

def place_bet(num_response = 0):
    ''' Ask player to place their bet. '''

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

def player_move(num_response = 0):
    ''' Ask player to hit or stand.  Hand is lost if bust. '''

    player1.evaluate_hand()
    if player1.blackjack:
        return

    if num_response > 3:
        print "It seems you don't understand the question.  Let's play again another time."
        exit()

    if len(player1.cards) == 2 and player1.pot >= player1.bet * 2:
        action = raw_input("----> Would you like to (h)it or (s)tand or (d)ouble down: ")
        valid_response = ['h', 'H', 'd', 'D']
    else:
        action = raw_input("----> Would you like to (h)it or (s)tand: ")
        valid_response = ['h', 'H']

    if action in valid_response:
        time.sleep(sleep_seconds)
        if action in ('d','D'):
            player1.bet *= 2
            print "Your bet is now %d." % player1.bet
        player1.deal_card()
        player1.show()
        player1.evaluate_hand()
        if player1.bust:
            print "\n\n#*#*# BUST! Dealer wins. #*#*#\n"
            player1.pot -= player1.bet
            player1.num_losses += 1
            play_again()
        elif action in ('h','H'):
            player_move()
    elif action not in ('s', 'S'):
        num_response += 1
        print "'%s' is not a valid response." % action
        player_move(num_response)

def dealer_move():
    ''' Dealer < 17, hit. 16 < Dealer < 22, stay. Dealer > 21, bust. '''

    dealer.show()
    dealer.evaluate_hand()
    if dealer.blackjack or player1.blackjack:
        return
    print "Dealer has %s." % dealer.hand,

    if dealer.bust:
        print "\n\n#*#*# BUST!!!! You win. #*#*#\n"
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

def end_hand():
    ''' Compare player hand to dealer hand, and do bet math. '''

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
        end_game()
    else:
        print "You have %d chips remaining." % player1.pot
        play_again = raw_input("----> Would you like to play again? (y/n) ")

        if play_again in ('y', 'Y'):
            os.system('clear') # clear screen. 'cls' for windows
            for player in players:
                player.reset()
            if deck.num_cards() < 15:
                deck.reset()
            play_game()
        else:
            end_game()

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

player1 = Player()
dealer = Player('Dealer')
players = [player1, dealer]

welcome()
deck = Deck()

play_game()


