from src.engine import assets
from src.engine import Screen
from src.engine import Animator
from src.animations import TranslationAnimation
from src.animations import RotationAnimation
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

        # TESTING
        self.testing_card = PlacedCard(self.dealer.take_card(), (100, 100), (0, 0, 0))
        self.animator.add_jobs([RotationAnimation(self.testing_card, (0, 500, 200), duration_s = 3)], asynchronous = False)

    def change_bet(self, amount: int):
        if BET_STEP <= (self.player.bet + amount) <= self.player.chips:
            self.player.bet += amount

    def deal_cards(self):
        animations = []

        for i in range(2):
            animations.extend(self.take_card(self.player.hands[0], self.player.get_next_card_pos()))
            animations.extend(self.take_card(self.dealer.hand, self.dealer.get_next_card_pos(), is_visible = not i))
        
        animations[-1].on_finish = lambda: self.finish_deal_cards(animations[-1].obj)

        self.animator.add_jobs(animations, asynchronous = True)

    def finish_deal_cards(self, placed_card: PlacedCard):
        self.dealer.hand.add_card(placed_card)

        if self.player.has_blackjack() or self.dealer.has_blackjack():
            return self.dealer_show()

        self.state = GameState.CHOOSE_ACTION

    def place_bet(self):        
        self.player.chips -= self.player.bet
        
        self.player.last_bet = self.player.bet

    def take_card(self, hand: Hand, destination, rotation_z: int = 0, is_visible: bool = True):
        animations = []

        card = self.dealer.take_card()

        hand.increment_n_cards()
        
        if card.is_cut_card():
            self.dealer.should_shuffle = True
            self.dealer.cut_card = PlacedCard(card, D_PLAYING_DECK_POS)
            
            animations.append(TranslationAnimation(self.dealer.cut_card, (D_PLAYING_DECK_POS[0] - (CARD_SIZE[0] * 2), D_PLAYING_DECK_POS[1])))

            card = self.dealer.take_card()

        placed_card = PlacedCard(card, D_PLAYING_DECK_POS)
    
        animations.append(TranslationAnimation(placed_card, destination))

        if is_visible or rotation_z != 0:
            animations.append(
                RotationAnimation(
                    placed_card, 
                    (0, 180 if is_visible else 0, rotation_z), 
                    on_finish = lambda: self.finish_take_card(hand, placed_card)
                )
            )

        return animations
        
    def finish_take_card(self, hand: Hand, placed_card: PlacedCard):
        hand.add_card(placed_card)

    def player_hit(self):
        animation = self.take_card(self.player.hands[0], self.player.get_next_card_pos())
        
        animation[-1].on_finish = lambda: self.finish_player_hit(animation[-1].obj)
        
        self.animator.add_jobs(animation, asynchronous = True)

    def finish_player_hit(self, placed_card: PlacedCard):
        self.player.hands[0].add_card(placed_card)

        if self.player.hands[0].value >= 21:
            return self.dealer_show()

        self.state = GameState.CHOOSE_ACTION

    def player_stand(self):
        self.dealer_show()

    def player_double_down(self):
        if self.player.chips < self.player.bet or len(self.player.hands[0].cards) > 2:
            self.state = GameState.CHOOSE_ACTION
            
            return

        self.player.chips -= self.player.bet
        self.player.bet *= 2

        animation = self.take_card(self.player.hands[0], self.player.get_next_card_pos(), rotation_z = 90)
        animation[-1].on_finish = lambda: self.finish_player_double_down(animation[-1].obj)
        
        self.animator.add_jobs(animation, asynchronous = True)

    def finish_player_double_down(self, placed_card):
        self.player.hands[0].add_card(placed_card)

        self.dealer_show()

    def player_split(self):
        pass

    def dealer_show(self):
        self.state = GameState.IDLING

        
        self.animator.add_jobs(
            [RotationAnimation(
                self.dealer.hand.cards[1], 
                (0, 180, 0), 
                on_finish = lambda: self.dealer_take()
            )]
        )

    def dealer_take(self, placed_card = None):
        if placed_card is not None:
            self.dealer.hand.add_card(placed_card)

        if self.dealer.should_take():
            animation = self.take_card(self.dealer.hand, self.dealer.get_next_card_pos())
            animation[-1].on_finish = lambda: self.dealer_take(animation[-1].obj)
            
            self.animator.add_jobs(animation, asynchronous = True)
        else:
            self.finish_dealer_take()

    def finish_dealer_take(self):
        self.state = GameState.POST_ROUND
    
    def get_winnings(self):
        player_value = self.player.hands[0].value
        dealer_value = self.dealer.hand.value

        if self.player.has_blackjack() and not self.dealer.has_blackjack(): # Blackjack
            return int(self.player.bet * (1 + BLACKJACK_MULTIPLIER))
        
        if player_value == dealer_value: # Push
            return self.player.bet
        
        if (player_value > dealer_value or dealer_value > 21) and player_value <= 21: # Player better value and not bust OR dealer bust and not player
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

        self.animator.draw(screen)

        # TESTING
        if self.testing_card:
            self.testing_card.draw(screen)
        
        #print('Chips: {}\tBet: {}'.format(self.player.chips, self.player.bet))
        screen.blit(assets.fonts['standard'].render('Chips: {}        Bet: {}        State: {}'.format(self.player.chips, self.player.bet, self.state.name), False, (255, 255, 255)), (6, 6))