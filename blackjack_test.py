#!/usr/bin/env python

import blackjack

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

    if not player.bust:
        blackjack.end_hand(player1, dealer)

    blackjack.play_again(player1, players, deck)

def main():

    player1 = blackjack.Player()
    dealer = blackjack.Player('Dealer')
    players = [player1, dealer]

    blackjack.welcome(player1)
    deck = blackjack.Deck()

    test_game(players, deck)


##

if __name__ == '__main__':
    main()

