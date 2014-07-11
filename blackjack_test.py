#!/usr/bin/env python

import blackjack
blackjack.debug = True

def test_game(players, deck):
    ''' Deal first 2 cards.  Player moves, then dealer moves, then compare hands.  '''

    (player1, dealer) = players
    blackjack.place_bet(player1)

    for i in range(2):
        for player in players:
            player.deal_card(deck)

    for player in players:
        player.show()

    for player in players:
        if player.is_dealer:
            blackjack.dealer_move(dealer, player1, deck)
        else:
            blackjack.player_move(player, deck)

        if player.bust:
            break

    if not player1.bust and not dealer.bust:
        blackjack.end_hand(player1, dealer)

    if blackjack.play_again(player1, players, deck, 'y'):
        test_game(players, deck)
    else:
        blackjack.end_game(player1)



def main():

    player1 = blackjack.Player()
    dealer = blackjack.Player('Dealer')
    players = [player1, dealer]

    blackjack.welcome(player1)

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

    test_game(players, deck)


##

if __name__ == '__main__':
    main()

