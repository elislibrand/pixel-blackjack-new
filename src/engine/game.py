from src.engine import assets
from src.engine import Screen
from src.engine import Animator
from src.objects import Animation
from src.objects import Player
from src.objects import Dealer
from src.objects import Hand
from src.objects import Card
from src.objects import PlacedCard
from src.enums import GameState
from src.data.constants import *

class Game:
    def __init__(self):
        self.state = GameState.SELECT_BET
        
        self.player = Player()
        self.dealer = Dealer()

        self.animator = Animator()

        self.props = []
        
        self.new_round()
    
    def new_round(self):
        self.player.reset()
        self.dealer.reset()

        self.state = GameState.SELECT_BET

    def change_bet(self, amount: int):
        if 0 <= (self.player.bet + amount) <= self.player.chips:
            self.player.bet += amount

    def deal_cards(self):
        animations = []

        for i in range(2):
            animations.extend(self.take_card(self.player.hands[0], self.player.get_next_card_pos()))
            animations.extend(self.take_card(self.dealer.hand, self.dealer.get_next_card_pos(), is_visible = i))
        
        animations[-1].on_finish = self.finish_deal_cards

        self.animator.add_jobs(animations, asynchronous = True)

    def finish_deal_cards(self):
        self.dealer.hand.cards[1].set_visible()

        if self.player.has_blackjack() or self.dealer.has_blackjack():
            return self.dealer_take()

        self.state = GameState.CHOOSE_ACTION

    def place_bet(self):
        self.player.chips -= self.player.bet

    def take_card(self, hand: Hand, destination, is_rotated: bool = False, is_visible: bool = True):
        animations = []

        card = self.dealer.take_card()
        
        if card.is_cut_card():
            self.dealer.should_shuffle = True
            self.dealer.cut_card = PlacedCard(card, D_PLAYING_DECK_POS)
            
            animations.append(Animation(self.dealer.cut_card, (D_PLAYING_DECK_POS[0] - CARD_SIZE[0] * 2, D_PLAYING_DECK_POS[1])))

            card = self.dealer.take_card()

        placed_card = PlacedCard(card, D_PLAYING_DECK_POS, is_rotated, is_visible = False)
        hand.add_card(placed_card)
        
        if is_visible:
            animations.append(Animation(placed_card, destination, on_finish = hand.cards[-1].set_visible))
        else:
            animations.append(Animation(placed_card, destination))

        return animations

    def player_hit(self, is_rotated: bool = False):
        animation = self.take_card(self.player.hands[0], self.player.get_next_card_pos())
        
        self.animator.add_jobs(animation, asynchronous = True)

        self.state = GameState.CHOOSE_ACTION

    def player_stand(self):
        self.dealer_take()

    def player_double_down(self):
        if self.player.chips < self.player.bet:
            self.state = GameState.CHOOSE_ACTION
            
            return

        self.player.chips -= self.player.bet
        self.player.bet *= 2

        self.player_hit(is_rotated = True)
        
        self.dealer_take()

    def player_split(self):
        pass

    def dealer_take(self):
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
        
        self.new_round()

    def update(self):
        self.animator.play()

    def draw(self, screen: Screen):
        for prop in self.props:
            prop.draw(screen)

        self.dealer.draw_deck(screen)
        
        if self.dealer.cut_card is not None:
            self.dealer.cut_card.draw(screen)
            
        self.player.draw_hands(screen)
        self.dealer.draw_hand(screen)
        
        #print('Chips: {}\tBet: {}'.format(self.player.chips, self.player.bet))
        screen.blit(assets.fonts['standard'].render('Chips: {}        Bet: {}        State: {}'.format(self.player.chips, self.player.bet, self.state.name), False, (255, 255, 255)), (6, 6))