import random
from art import logo
import os


def deal_card() -> int:
    """Returns a random card from the deck."""
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return random.choice(cards)


def check_score(current_cards: list[int]) -> int:
    """
    Determines the score from a list of cards representing
    the hand of a player.
    """
    current_score = sum(current_cards)
    if current_score == 21 and len(current_cards) == 2:
        return 0
    if current_score > 21 and 11 in current_cards:
        ace = current_cards.index(11)
        current_cards[ace] = 1
        current_score = sum(current_cards)
    return current_score


def who_won(player_score: int, dealer_score: int):
    """
    Determines the winner of the game based on the scores passed.
    Note that a 0 represents blackjack.
    """
    if player_score == dealer_score:
        print("It is a draw \U0001FAE4.")
    elif dealer_score == 0:
        print("Dealer blackjack. You lose \U0001F641.")
    elif player_score == 0:
        print("Blackjack! You win \U0001f600.")
    elif player_score > 21:
        print("You busted. You lose \U0001F641.")
    elif dealer_score > 21:
        print("The dealer busted. You win \U0001f600.")
    elif player_score > dealer_score:
        print("You win \U0001f600.")
    else:
        print("You lose \U0001F641.")


def play_game():
    os.system("clear")
    print(logo)

    player_cards: list[int] = []
    dealer_cards: list[int] = []

    for _ in range(2):
        player_cards.append(deal_card())
        dealer_cards.append(deal_card())

    player_score = check_score(player_cards)
    dealer_score = check_score(dealer_cards)

    print(f"Your cards: {player_cards}, current score: {player_score}")
    print(f"Dealer's first card: {dealer_cards[0]}")

    if player_score != 0 and dealer_score != 0:
        while input("\nType 'y' to get another card, type 'n' to pass: ") == "y":
            player_cards.append(deal_card())
            player_score = check_score(player_cards)
            print(f"Your cards: {player_cards}, current score: {player_score}")
            print(f"Dealer's first card: {dealer_cards[0]}")
            if player_score > 21:
                break
        if player_score <= 21:
            while dealer_score < 17:
                dealer_cards.append(deal_card())
                dealer_score = check_score(dealer_cards)

    print(f"\nYour final hand: {player_cards}, final score: {player_score}")
    print(f"Dealer's final hand: {dealer_cards}, final score: {dealer_score}\n")

    who_won(player_score, dealer_score)

    continue_playing = input(
        "\nDo you want to play a game of Blackjack? Type 'y' or 'n': "
    )
    if continue_playing == "y":
        play_game()


continue_playing = input("Do you want to play a game of Blackjack? Type 'y' or 'n': ")
if continue_playing == "y":
    play_game()
