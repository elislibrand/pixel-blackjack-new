import pygame as pg

# Game information
G_TITLE = 'Pixel Blackjack'
G_VERSION = '0.1.0'

G_SIZE = (640, 360)

# Colors
C_BACKGROUND = (48, 102, 60)

# Game
BLACKJACK_MULTIPLIER = (3 / 2)
CARD_SIZE = (33, 49)
BET_STEP = 4

# Player
P_CARD_STARTING_POS = ((G_SIZE[0] / 2) - int(CARD_SIZE[0] / 2), G_SIZE[1] - CARD_SIZE[1] - 10)
P_CARD_STACK_OFFSET = (8, 10)

P_STARTING_CHIPS = 100

# Dealer
D_CARD_STARTING_POS = ((G_SIZE[0] / 2) - CARD_SIZE[0] - 2, 10)
D_CARD_STACK_OFFSET = (CARD_SIZE[0] + 4, 0)

D_PLAYING_DECK_POS = (G_SIZE[0]- CARD_SIZE[0] - 10, 10)