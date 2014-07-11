#!/usr/bin/env python

import blackjack
blackjack.debug = True

def test_game():
    ''' Deal first 2 cards.  Player moves, then dealer moves, then compare hands.  '''

    responses = ['j',-4,20]
    blackjack.place_bet([20])

    for i in range(2):
        for player in players:
            player.deal_card()

    for player in players:
        player.show()

    for player in players:
        if player.is_dealer:
            blackjack.dealer_move()
        else:
            blackjack.player_move(['h','h','s'])

        if player.bust:
            break

    if not player1.bust and not dealer.bust:
        blackjack.end_hand()

    if blackjack.play_again('y'):
        test_game()
    else:
        blackjack.end_game()



if __name__ == '__main__':

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

    deck = blackjack.Deck(ranks,shuffle)
    deck.suspense = 0
    blackjack.deck = deck

    test_game()


##


