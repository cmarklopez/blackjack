from blackjack import __version__
from blackjack.blackjack import who_won
import art


def test_version():
    assert __version__ == "0.1.0"
