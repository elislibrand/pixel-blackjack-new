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
        
    def change_bet(self, amount: int):
        if BET_STEP <= (self.player.bet + amount) <= self.player.chips:
            self.player.bet += amount

    def set_bet(self, bet: int):
        if BET_STEP <= bet <= self.player.chips:
            self.player.bet = bet

    def deal_cards(self, placed_card = None, iteration = 0):
        animations = []

        if iteration % 2 == 0:
            animations.extend(self.take_card(self.player.active_hand, self.player.get_next_card_pos(self.player.active_hand)))
            if placed_card:
                self.dealer.hand.add_card(placed_card)
        else:
            animations.extend(self.take_card(self.dealer.hand, self.dealer.get_next_card_pos(), is_visible = iteration == 1))
            self.player.active_hand.add_card(placed_card)
        
        if iteration == 3:
            animations[-1].on_finish = lambda: self.finish_deal_cards(placed_card = animations[-1].obj)
        else:
            animations[-1].on_finish = lambda: self.deal_cards(placed_card = animations[-1].obj, iteration = iteration + 1)

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
        
        if card.is_cut_card():
            cut_card = PlacedCard(card, D_PLAYING_DECK_POS)
            
            animations.append(
                TranslationAnimation(
                    cut_card,
                    CUT_CARD_POS,
                    on_finish = lambda: self.dealer.set_cut_card(cut_card)
                )
            )

            card = self.dealer.take_card()

        placed_card = PlacedCard(card, D_PLAYING_DECK_POS)
    
        animations.append(TranslationAnimation(placed_card, destination))

        if is_visible or not rotation_z == 0:
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
        animations = self.take_card(self.player.active_hand, self.player.get_next_card_pos(self.player.active_hand))
        
        animations[-1].on_finish = lambda: self.finish_player_hit(animations[-1].obj)
        
        self.animator.add_jobs(animations, asynchronous = True)

    def finish_player_hit(self, placed_card: PlacedCard):
        self.player.active_hand.add_card(placed_card)

        if self.player.active_hand.value >= 21:
            return self.go_to_next_hand()

        self.state = GameState.CHOOSE_ACTION

    def player_stand(self):
        self.go_to_next_hand()

    def player_double_down(self):
        if self.player.chips < self.player.last_bet or len(self.player.active_hand.cards) > 2:
            self.state = GameState.CHOOSE_ACTION
            
            return

        self.player.chips -= self.player.last_bet
        self.player.bet += self.player.last_bet

        animations = self.take_card(self.player.active_hand, self.player.get_next_card_pos(self.player.active_hand, offset = DOUBLE_DOWN_OFFSET), rotation_z = 90)
        animations[-1].on_finish = lambda: self.finish_player_double_down(animations[-1].obj)
        
        self.animator.add_jobs(animations, asynchronous = True)

    def finish_player_double_down(self, placed_card):
        self.player.active_hand.add_card(placed_card)

        self.go_to_next_hand()

    def player_split(self):
        if self.player.chips < self.player.last_bet or (not self.player.active_hand.cards[0].get_value() == self.player.active_hand.cards[1].get_value() or self.player.get_n_active_hands() == len(P_HANDS_POS)):
            self.state = GameState.CHOOSE_ACTION

            return

        self.player.chips -= self.player.last_bet
        self.player.bet += self.player.last_bet

        self.player_split_move_hands()

    def player_split_move_hands(self):
        if self.player.is_next_hand_active():
            self.player.move_hands(self.player.hands[self.player.active_hand_index + 1])
        
        animations = []

        positions = P_HANDS_POS[self.player.get_n_active_hands()]

        for i, hand in enumerate(self.player.hands):
            if not hand.is_active:
                continue

            hand_pos = positions[i]

            dx = hand.cards[0].pos[0] - hand_pos[0] # Get x difference

            for card in hand.cards:
                animations.append(TranslationAnimation(card, (card.pos[0] - dx, card.pos[1]), duration_s = 0.25, should_draw = False))
        
        animations[-1].on_finish = lambda: self.player_split_cards()
        self.animator.add_jobs(animations)
    
    def player_split_cards(self):
        upper_card = self.player.active_hand.cards[1]
        
        destination_hand_index = self.player.active_hand_index + 1

        self.player.active_hand.remove_card(upper_card)
        self.player.activate_hand_with_index(destination_hand_index)
        self.player.active_hand.add_card(upper_card)

        self.animator.add_jobs([
            TranslationAnimation(
                upper_card, 
                P_HANDS_POS[self.player.get_n_active_hands() - 1][destination_hand_index],
                duration_s = 0.25,
                should_draw = False, 
                on_finish = lambda: self.player_split_deal_cards()
            )
        ])

    def player_split_deal_cards(self):
        animations = []

        old_hand = self.player.hands[self.player.active_hand_index - 1]
        new_hand = self.player.hands[self.player.active_hand_index]

        animations.extend(self.take_card(new_hand, self.player.get_next_card_pos(new_hand)))
        animations.extend(self.take_card(old_hand, self.player.get_next_card_pos(old_hand)))

        animations[-1].on_finish = lambda: self.finish_player_split(old_hand, animations[-1].obj)

        self.animator.add_jobs(animations, asynchronous = True)
        
    def finish_player_split(self, hand : Hand,  placed_card: PlacedCard):
        hand.add_card(placed_card)

        self.state = GameState.CHOOSE_ACTION

    def go_to_next_hand(self):
        if self.player.is_on_last_hand():
            return self.dealer_show()

        self.player.go_to_next_hand()
        
        self.state = GameState.CHOOSE_ACTION

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

        if self.dealer.should_take() and not self.player.has_blackjack():
            animations = self.take_card(self.dealer.hand, self.dealer.get_next_card_pos())
            animations[-1].on_finish = lambda: self.dealer_take(animations[-1].obj)
            
            self.animator.add_jobs(animations, asynchronous = True)
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
        print('{:>8}    {:>6}    {:>6}'.format(self.get_winnings(), self.player.hands[0].value, self.dealer.hand.value))
        
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
        
        screen.blit(assets.fonts['standard'].render('Chips: {}        Bet: {}        State: {}'.format(self.player.chips, self.player.bet, self.state.name), False, (255, 255, 255)), (6, 6))