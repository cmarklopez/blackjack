import random
from art import logo
from typing import Iterable

CARD = """\
┌─────────┐
│{}       │
│         │
│         │
│    {}   │
│         │
│         │
│       {}│
└─────────┘
""".format(
    "{rank: <2}", "{suit: <2}", "{rank: >2}"
)

HIDDEN_CARD = """\
┌─────────┐
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
└─────────┘
"""


class Card:
    suit_conversion = {0: "Spades", 1: "Clubs", 2: "Hearts", 3: "Diamonds"}
    conversion_dict = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}

    def __init__(self, rank: int, suit: int):
        self.rank = rank
        self.suit = suit
        self.rank_name = self._convert_rank()
        self.suit_name = self._convert_suit()
        self.name = f"{self.rank_name} of {self.suit_name}"

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def _convert_rank(self) -> str:
        return self.conversion_dict.get(self.rank, str(self.rank))

    def _convert_suit(self) -> str:
        return self.suit_conversion[self.suit]


class Deck:
    def __init__(self):
        self.cards = self._generate_deck()
        self.drawn = 0
        self.remaining = 52

    def _generate_deck(self) -> list[Card]:
        deck: list[Card] = [
            Card(rank=rank, suit=suit) for suit in range(4) for rank in range(1, 14)
        ]
        return deck

    def draw(self) -> Card:
        if self.remaining == 0:
            raise ZeroCardsRemaining
        else:
            drawn_card = self.cards.pop(random.randint(0, self.remaining - 1))
        self.drawn += 1
        self.remaining -= 1
        return drawn_card


class Hand:
    def __init__(self):
        self.cards: list[Card] = []
        self.value = 0
        self.name = ""

    def __repr__(self) -> str:
        return self.name

    def _calculate_value(self) -> int:
        card_values = {"Ace": 11, "Jack": 10, "Queen": 10, "King": 10}
        hand_value = sum(
            [card_values.get(card.rank_name, card.rank) for card in self.cards]
        )
        if hand_value == 21 and len(self.cards) == 2:
            hand_value = 0
        elif hand_value > 21:
            number_of_aces = 0
            for card in self.cards:
                if card.rank_name == "Ace":
                    number_of_aces += 1
            while number_of_aces > 0 and hand_value > 21:
                hand_value -= 10
                number_of_aces -= 1

        self.value = hand_value
        return hand_value

    def _create_name(self):
        name = ""
        for card in self.cards:
            name = name + str(card) + "\n"
        self.name = name

    def add_card(self, card_to_add: Card) -> None:
        self.cards.append(card_to_add)
        self._calculate_value()
        self._create_name()


class ZeroCardsRemaining(Exception):
    pass


def join_lines(strings: Iterable[str]) -> str:
    """
    Stack strings horizontally.
    This doesn't keep lines aligned unless the preceding lines have the same length.
    :param strings: Strings to stack
    :return: String consisting of the horizontally stacked input
    """
    liness = [string.splitlines() for string in strings]
    return "\n".join("".join(lines) for lines in zip(*liness))


def ascii_version_of_card(cards: list[Card]) -> str:
    """
    Instead of a boring text version of the card we render an ASCII image of the card.
    :param cards: One or more card objects
    :return: A string, the nice ascii version of cards
    """

    # we will use this to prints the appropriate icons for each card
    name_to_symbol = {
        "Spades": "♠",
        "Diamonds": "♦",
        "Hearts": "♥",
        "Clubs": "♣",
    }

    def card_to_string(card: Card) -> str:
        # 10 is the only card with a 2-char rank abbreviation
        rank = card.rank_name if card.rank_name == "10" else card.rank_name[0]

        # add the individual card on a line by line basis
        return CARD.format(rank=rank, suit=name_to_symbol[card.suit_name])

    return join_lines(map(card_to_string, cards))


def ascii_version_of_hidden_card(cards: list[Card]) -> str:
    """
    Essentially the dealers method of print ascii cards. This method
    hides the first card, shows it flipped over
    :param cards: A list of card objects, the first will be hidden
    :return: A string, the nice ascii version of cards
    """

    return join_lines((HIDDEN_CARD, ascii_version_of_card(cards[1:])))


def who_won(player_score: int, dealer_score: int):
    """
    Determines the winner of the game based on the scores passed.
    Note that a 0 represents blackjack.
    :param player_score: the value of the hand of the user player
    :param dealer_score: the value of the hand of the computer player
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


def print_game_state(player_hand, dealer_hand) -> None:
    print("Player hand:\n")
    print(ascii_version_of_card(player_hand.cards))
    print("Dealer hand:\n")
    print(ascii_version_of_hidden_card(dealer_hand.cards))


if __name__ == "__main__":

    def play_game():
        print(chr(27) + "[2J")
        print(logo)

        blackjack_deck = Deck()
        player_hand = Hand()
        dealer_hand = Hand()

        for _ in range(2):
            player_card = blackjack_deck.draw()
            dealer_card = blackjack_deck.draw()
            player_hand.add_card(player_card)
            dealer_hand.add_card(dealer_card)

        print_game_state(player_hand, dealer_hand)

        if player_hand.value != 0 and dealer_hand.value != 0:
            while input("\nType 'y' to get another card, type 'n' to pass: \n") == "y":
                player_hand.add_card(blackjack_deck.draw())
                print(chr(27) + "[2J")
                print(logo)
                print_game_state(player_hand, dealer_hand)
                if player_hand.value > 21:
                    break
            if player_hand.value <= 21:
                while dealer_hand.value < 17:
                    dealer_hand.add_card(blackjack_deck.draw())

        print_game_state(player_hand, dealer_hand)
        print(
            f"\nPlayer score is: {player_hand.value}\nDealer score is: {dealer_hand.value}\n"
        )

        who_won(player_hand.value, dealer_hand.value)

        continue_playing = input(
            "\nDo you want to play a game of Blackjack? Type 'y' or 'n': "
        )

        if continue_playing == "y":
            play_game()
        else:
            print(chr(27) + "[2J")

    print(chr(27) + "[2J")
    continue_playing = input(
        "Do you want to play a game of Blackjack? Type 'y' or 'n': \n"
    )
    if continue_playing == "y":
        play_game()
