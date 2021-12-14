import pygame
from constantes import *
import sys
import time

from Model import Model

v2 = pygame.Vector2
masse = int(input("donner une masse: "))


class Simulation:

    def __init__(self):
        """Initialize variables"""
        pygame.init()
        # Display
        self.display = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption("Simulation")
        # Frames
        self.clock = pygame.time.Clock()
        # Instances
        self.model = Model(masse, v2(250, 50))

    def process(self, dt: float):
        """Backend related events"""
        self.model.process(dt)
        pass

    def render(self):
        """Frontend (render) related events"""
        self.model.render(self.display)

    def launch(self):
        """Launches Simulation"""
        last_time = time.time()
        while True:
            dt, last_time = (time.time() - last_time) * 60, time.time()  # Time derivative

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display.fill(BLACK)

            self.process(dt)
            self.render()

            pygame.display.update()
