import random
from art import logo
import os


class Card:
    def __init__(self, rank: int, suit: int):
        self.rank = rank
        self.suit = suit
        self.rank_name = self.__convert_rank()
        self.suit_name = self.__convert_suit()
        self.name = f"{self.rank} of {self.suit_name}"

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def __convert_rank(self) -> str:
        conversion_dict = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}
        return conversion_dict.get(self.rank, str(self.rank))

    def __convert_suit(self) -> str:
        suit_conversion = {0: "Spades", 1: "Clubs", 2: "Hearts", 3: "Diamonds"}
        return suit_conversion[self.suit]


class Deck:
    def __init__(self):
        self.cards = self.__generate_deck()
        self.drawn = 0
        self.remaining = 52

    def __generate_deck(self) -> list[Card]:
        deck: list[Card] = []
        for suit in range(4):
            deck.extend(Card(rank=rank, suit=suit) for rank in range(1, 14))
        return deck

    def draw(self) -> Card:
        if self.remaining == 0:
            raise (ZeroCardsRemaining)
        else:
            drawn_card = random.choice(self.cards)
        self.drawn += 1
        self.remaining -= 1
        return drawn_card


class Hand:
    def __init__(self):
        self.cards: list[Card] = []
        self.value = 0

    def calculate_value(self) -> int:
        card_values = {"Ace": 11, "Jack": 10, "Queen": 10, "King": 10}
        hand_value = sum(
            [card_values.get(card.rank_name, card.rank) for card in self.cards]
        )
        number_of_aces = 0
        if hand_value > 21:
            for card in self.cards:
                if card.rank_name == "Ace":
                    number_of_aces += 1
        while number_of_aces > 0 and hand_value > 21:
            hand_value -= 10
            number_of_aces -= 1

        self.value = hand_value
        return hand_value

    def add_card(self, card_to_add: Card) -> None:
        self.cards.append(card_to_add)
        self.calculate_value()


class ZeroCardsRemaining(Exception):
    pass


def play_game():
    os.system("clear")
    print(logo)

    blackjack_deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()

    for _ in range(2):
        player_card = blackjack_deck.draw()
        dealer_card = blackjack_deck.draw()
        player_hand.add_card(player_card)
        dealer_hand.add_card(dealer_card)

    print(player_hand.value, " ", dealer_hand.value)
    print(blackjack_deck.drawn)
    print(blackjack_deck.remaining)

    continue_playing = input(
        "\nDo you want to play a game of Blackjack? Type 'y' or 'n': "
    )
    if continue_playing == "y":
        play_game()


continue_playing = input("Do you want to play a game of Blackjack? Type 'y' or 'n': ")
if continue_playing == "y":
    play_game()
