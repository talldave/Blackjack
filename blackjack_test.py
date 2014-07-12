#!/usr/bin/env python

# blackjack_test.py
# David Bianco - JULY 2014
# used to automate test of blackjack.py

import blackjack
import pdb
blackjack.debug = True

# VALIDATION
#
# name: all input accepted
# num_decks: must be integer in range 1-8.  Invalid defaults to 1.
# bet: must be integer in range 1-Size_of_Pot.  More than 4 invalid responses, then quit.
# player move: must be 'h' or 's' (or 'd' on first move). More than 4 invalid responses, then quit.
# play_again: must be 'y'.  Otherwise defaults to 'n'

def test_game(round = 0):
    ''' Deal first 2 cards.  Player moves, then dealer moves, then compare hands.  '''

    print "(debug) ROUND: %d" % round
    bet_resp = [5]
    player_resp = ['s']

    if round == 0:
        print "(debug)", 40*"*"
        print "(debug) *** TEST: Player has blackjack"
        print "(debug)", 40*"*"
        ranks = (2,'J','K','A',9,8,8,8,8,8,8,8,8)
        shuffle = False
        blackjack.deck.reset(ranks,shuffle)
    elif round == 1:
        print "(debug)", 40*"*"
        print "(debug) *** TEST: Dealer has blackjack"
        print "(debug)", 40*"*"
        ranks = (2,'K','Q',9,'A',8,8,8,8,8,8,8,8)
        shuffle = False
        blackjack.deck.reset(ranks,shuffle)
    elif round == 2:
        print "(debug)", 40*"*"
        print "(debug) *** TEST: Both player and dealer have blackjack"
        print "(debug)", 40*"*"
        ranks = (2,'K','Q','A','A',8,8,8,8,8,8,8,8)
        shuffle = False
        blackjack.deck.reset(ranks,shuffle)
    elif round == 3:
        print "(debug)", 40*"*"
        print "(debug) *** TEST: Player bust"
        print "(debug)", 40*"*"
        player_resp = ['h']
        ranks = (2,8,8,8,8,8,8,8,8,8,8,8,8)
        shuffle = False
        blackjack.deck.reset(ranks,shuffle)
    elif round == 4:
        print "(debug)", 40*"*"
        print "(debug) *** TEST: Dealer bust"
        print "(debug)", 40*"*"
        player_resp = ['s']
        ranks = (2,8,8,8,8,8,8,8,8,8,8,8,8)
        shuffle = False
        blackjack.deck.reset(ranks,shuffle)
    elif round == 5:
        print "(debug)", 40*"*"
        print "(debug) *** TEST: push"
        print "(debug)", 40*"*"
        player_resp = ['s']
        ranks = (2,8,8,9,9,8,8,8,8,8,8,8,8)
        shuffle = False
        blackjack.deck.reset(ranks,shuffle)
    elif round == 6:
        print "(debug)", 40*"*"
        print "(debug) *** TEST: Player double-down BUST"
        print "(debug)", 40*"*"
        player_resp = ['d']
        ranks = (2,8,8,9,9,8,8,8,8,8,8,8,8)
        shuffle = False
        blackjack.deck.reset(ranks,shuffle)
    elif round == 7:
        print "(debug)", 40*"*"
        print "(debug) *** TEST: Player double-down Win"
        print "(debug)", 40*"*"
        player_resp = ['d']
        ranks = (2,8,8,9,9,3,8,8,8,8,8,8,8)
        shuffle = False
        blackjack.deck.reset(ranks,shuffle)
    elif round == 8:
        print "(debug)", 40*"*"
        print "(debug) *** TEST: Player double-down Push"
        print "(debug)", 40*"*"
        player_resp = ['d']
        ranks = (2,8,8,9,8,3,4,8,8,8,8,8,8)
        shuffle = False
        blackjack.deck.reset(ranks,shuffle)
    elif round > 20:
        player_resp = False
        bet_resp = False


    #bet_resp = ['k',-3,435,'foo','0',888,-8,-9] # too many bad responses
    blackjack.place_bet(bet_resp)

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
                blackjack.dealer_move()
            else:
                #player_resp = ['k',-3,101,'foo','0',8808,-8,-9] # too many bad responses
                blackjack.player_move(player_resp)

            if player.bust:
                break

    blackjack.end_hand()

    if blackjack.play_again():
        round += 1
        test_game(round)
    else:
        blackjack.end_game()

if __name__ == '__main__':

    #pdb.set_trace()

    player1 = blackjack.Player()
    dealer = blackjack.Player('Dealer')
    players = [player1, dealer]

    blackjack.player1 = player1
    blackjack.dealer = dealer
    blackjack.players = players

    blackjack.welcome()

    blackjack.deck = blackjack.Deck()
    blackjack.deck.suspense = 0

    test_game()

