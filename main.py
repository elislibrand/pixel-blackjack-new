from src.engine import Card
from src.engine import Deck
from src.engine import Hand
from src.enums import HandState
from src.enums import Rank
from src.enums import Suit

deck = Deck()

deck.create()
deck.shuffle()

print(''.join(['{}{} '.format(card.suit.value, card.rank.value) for card in deck.cards]))

hand = Hand()

while True:
    try:
        hand.add_card(Card(Suit.CLUBS, Rank(input('Enter rank: '))))

        print('{}\t[{}] ({})'.format(hand.value, ' '.join(['{}{}'.format(card.suit.value, card.rank.value) for card in hand.cards]), hand.state.name))
    except KeyboardInterrupt:
        break