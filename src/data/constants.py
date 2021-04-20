import pygame as pg

# Game information
G_TITLE = 'Pixel Blackjack'
G_VERSION = '0.1.0'

G_SIZE = (640, 360)

# Colors
C_BACKGROUND = (48, 102, 60)

# Player
P_CARD_STARTING_POS = ((G_SIZE[0] / 2) - int(33 / 2), G_SIZE[1] - 49)
P_CARD_STACK_OFFSET = (8, -10)

# Dealer
D_CARD_STARTING_POS = ((G_SIZE[0] / 2) + 2, 0)
D_CARD_STACK_OFFSET = (-(33 + 4), 0)

D_PLAYING_DECK_POS = (597, 10)

# Other
BLACKJACK_MULTIPLIER = (3 / 2)