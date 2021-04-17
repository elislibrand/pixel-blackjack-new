from src.engine import assets
from src.engine import Screen
from src.objects import Dealer
from src.objects import Player
from src.objects import PlacedCard
from src.enums import GameState
from src.data.constants import *

class Game:
    def __init__(self):
        self.state = GameState.SELECT_BET
        
        self.dealer = Dealer()
        self.player = Player()
        
        self.dealer.shuffle_playing_deck()

        self.new_round()
    
    def new_round(self):
        self.dealer.reset()
        self.player.reset()

        self.state = GameState.SELECT_BET

    def change_bet(self, amount: int):
        self.player.bet += amount

    def deal_cards(self):        
        for i in range(2):
            player_pos = (P_CARD_STARTING_POS[0] + (i * P_CARD_STACK_OFFSET[0]), P_CARD_STARTING_POS[1] + (i * P_CARD_STACK_OFFSET[1]))
            dealer_pos = (D_CARD_STARTING_POS[0] + (i * D_CARD_STACK_OFFSET[0]), D_CARD_STARTING_POS[1] + (i * D_CARD_STACK_OFFSET[1]))

            self.player.hands[0].cards.append(PlacedCard(self.dealer.playing_deck.draw_card(), player_pos))
            self.dealer.hand.cards.append(PlacedCard(self.dealer.playing_deck.draw_card(), dealer_pos, i))
        
        self.state = GameState.CHOOSE_ACTION

    def place_bet(self):
        self.player.chips -= self.player.bet

    def hit(self):
        n_cards = len(self.player.hands[0].cards)
        player_pos = (P_CARD_STARTING_POS[0] + (n_cards * P_CARD_STACK_OFFSET[0]), P_CARD_STARTING_POS[1] + (n_cards * P_CARD_STACK_OFFSET[1]))

        self.player.hands[0].cards.append(PlacedCard(self.dealer.playing_deck.draw_card(), player_pos))

        print('hejehej')

    def stand(self):
        pass

    def double_down(self):
        pass

    def split(self):
        pass

    def draw(self, screen: Screen):
        for card in self.player.hands[0].cards:
            card.draw(screen)
        
        for card in self.dealer.hand.cards:
            card.draw(screen)
        
        print('Chips: {}\tBet: {}'.format(self.player.chips, self.player.bet))
        screen.window.blit(assets.fonts['standard'].render('Chips: {}        Bet: {}        State: {}'.format(self.player.chips, self.player.bet, self.state.name), False, (255, 255, 255)), (300, 300))