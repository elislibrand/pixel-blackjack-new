from src.engine import assets
from src.engine import Screen
from src.objects import Player
from src.objects import Dealer
from src.objects import PlacedCard
from src.enums import GameState
from src.data.constants import *

class Game:
    def __init__(self):
        self.state = GameState.SELECT_BET
        
        self.player = Player()
        self.dealer = Dealer()
        
        self.dealer.shuffle_playing_deck()

        self.new_round()
    
    def new_round(self):
        self.player.reset()
        self.dealer.reset()

        self.state = GameState.SELECT_BET

    def change_bet(self, amount: int):
        if 0 <= (self.player.bet + amount) <= self.player.chips:
            self.player.bet += amount

    def deal_cards(self):
        for i in range(2):
            player_pos = (P_CARD_STARTING_POS[0] + (i * P_CARD_STACK_OFFSET[0]), P_CARD_STARTING_POS[1] + (i * P_CARD_STACK_OFFSET[1]))
            dealer_pos = (D_CARD_STARTING_POS[0] + (i * D_CARD_STACK_OFFSET[0]), D_CARD_STARTING_POS[1] + (i * D_CARD_STACK_OFFSET[1]))

            self.player.hands[0].add_card(PlacedCard(self.dealer.playing_deck.draw_card(), player_pos))
            self.dealer.hand.add_card(PlacedCard(self.dealer.playing_deck.draw_card(), dealer_pos, is_visible = i))
        
        if self.player.has_blackjack() or self.dealer.has_blackjack():
            return self.dealer_show()
            
        self.state = GameState.CHOOSE_ACTION

    def place_bet(self):
        self.player.chips -= self.player.bet

    def hit(self, is_rotated = False):
        n_cards = len(self.player.hands[0].cards)
        player_pos = (P_CARD_STARTING_POS[0] + (n_cards * P_CARD_STACK_OFFSET[0]), P_CARD_STARTING_POS[1] + (n_cards * P_CARD_STACK_OFFSET[1]))

        self.player.hands[0].add_card(PlacedCard(self.dealer.playing_deck.draw_card(), player_pos, is_rotated))

        self.state = GameState.CHOOSE_ACTION

    def stand(self):
        self.dealer_show()

    def double_down(self):
        if self.player.chips < self.player.bet:
            self.state = GameState.CHOOSE_ACTION
            
            return

        self.player.chips -= self.player.bet
        self.player.bet *= 2

        self.hit(is_rotated = True)
        
        self.dealer_show()

    def split(self):
        pass

    def dealer_show(self):
        self.state = GameState.DEALER_SHOW

        self.dealer.hand.cards[0].set_visible()
    
    def get_winnings(self):
        player_value = self.player.hands[0].value
        dealer_value = self.dealer.hand.value

        if self.player.is_blackjack:
            return int(self.player.bet * (1 + BLACKJACK_MULTIPLIER))
        
        if player_value == dealer_value:
            return self.player.bet
        
        if player_value > dealer_value and player_value <= 21:
            return self.player.bet * 2

        return 0
    
    def end_round(self):
        print('Winnings: {}\tPlayer: {}\tDealer: {}'.format(self.get_winnings(), self.player.hands[0].value, self.dealer.hand.value))

        self.player.chips += self.get_winnings()
        
        self.player.reset()
        self.dealer.reset()
        
        self.state = GameState.SELECT_BET

    def draw(self, screen: Screen):
        for card in self.player.hands[0].cards:
            card.draw(screen)
        
        for card in self.dealer.hand.cards:
            card.draw(screen)
        
        #print('Chips: {}\tBet: {}'.format(self.player.chips, self.player.bet))
        screen.blit(assets.fonts['standard'].render('Chips: {}        Bet: {}        State: {}'.format(self.player.chips, self.player.bet, self.state.name), False, (255, 255, 255)), (6, 6))