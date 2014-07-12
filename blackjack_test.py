#!/usr/bin/env python

import blackjack
import pdb
blackjack.debug = True

def test_game(round = 0):
    ''' Deal first 2 cards.  Player moves, then dealer moves, then compare hands.  '''

    responses = [5]
    #responses = ['k',-3,435,'foo','0',888,-8,-9] # too many bad responses
    blackjack.place_bet(responses)

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
                responses = ['h','h','s']
                responses = ['s']
                #responses = ['k',-3,435,'foo','0',888,-8,-9] # too many bad responses
                blackjack.player_move(responses)

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

# normal
    ranks = (2,3,4,5,6,7,8,9,10,'J','Q','K','A')
    shuffle = True
# player has blackjack
    #ranks = (2,'J','K','A',9,8,8,8,8,8,8,8,8)
    #shuffle = False
# dealer has blackjack
    #ranks = (2,'K','Q',9,'A',8,8,8,8,8,8,8,8)
    #shuffle = False
# both player and dealer have blackjack
    ranks = (2,'K','Q','A','A',8,8,8,8,8,8,8,8)
    shuffle = False

    deck = blackjack.Deck(ranks,shuffle)
    deck.suspense = 0
    blackjack.deck = deck

    test_game()


##


