# game/game_loop.py
from .input_handler import handle_events
from .board_render import render
import pygame

# 게임 루프
def run(state):
    clock = pygame.time.Clock()
    running = True

    while running:
        running = handle_events(state)

        render(state)

        pygame.display.flip()
        clock.tick(60)