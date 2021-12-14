import pygame
from constantes import *
from math import cos, pi, sqrt, log, e
from Utility import draw_text
from Button import Button

pygame.font.init()

v2 = pygame.Vector2
debug_font = pygame.font.SysFont('Bauhuas 93', 30)


class Circle:
    """Circle class"""

    def __init__(self, radius, position):
        """Initializes attributes"""
        self.radius = radius
        self.pos = position

    # Setter and getter for radius
    def get_radius(self):
        return self.radius

    def set_radius(self, r):
        self.radius = r

    # Setter and getter for position
    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos


class Model(pygame.sprite.Sprite):
    """Model"""

    def __init__(self, masse=5, position=v2(0, 0), color=BLACK):
        """Initializes attributes"""
        super().__init__()
        # Visual
        self.color = color
        self.circle = Circle(masse // 10, position)
        # Physiques Oscillation
        self.k = 200
        self.masse = masse
        self.init_pos = v2(self.circle.get_pos().x, self.circle.get_pos().y)
        self.pulsation = sqrt(self.k / self.masse)
        self.max_amplitude = 50
        self.time = 0
        self.time_prime = 0
        self.phi = 3 * pi / 2
        # Physiques falling
        self.gravity = 0

        # State machine
        self.is_falling = True
        self.time_swap = False
        self.is_launched = False

        # GUI
        self.button = Button(v2(350, 50), scale_size=v2(135, 45), text="Launch", color=DARK_GRAY)

    def falling(self, dt):
        self.gravity += GRAVITY * dt * 0.075
        y = self.gravity/2 * self.time **2
        self.circle.set_pos(v2(self.init_pos.x, self.init_pos.y + y))

    def oscillating(self, dt):

        y = self.max_amplitude * log(self.masse * 0.01 + e) * cos(self.pulsation * self.time_prime + self.phi)

        self.circle.set_pos((v2(self.init_pos.x, self.init_pos.y + y)))

        self.max_amplitude -= 0.01
        self.max_amplitude = max(0, self.max_amplitude)

    def process(self, dt):
        if self.button.is_pressed():
            self.is_launched = True

        if self.is_launched:
            if not self.time_swap:
                self.time += dt * .1
                self.time_prime = 0
            else:
                self.time_prime += dt * .1
                self.time = 0

            if self.circle.get_pos().y + self.circle.get_radius() >= 250:
                self.is_falling = False
                self.init_pos = v2(self.circle.get_pos().x, 250 * log(self.masse * 0.001 + e))
                self.time_swap = True

            if not self.is_falling:
                self.oscillating(dt)
            else:
                self.falling(dt)

    def coordinates(self, display):
        """Coordinates system"""
        # Axis
        cte = 30
        pygame.draw.line(display, DARK_GRAY, v2(30, cte), v2(495, cte), 2)
        pygame.draw.line(display, DARK_GRAY, v2(cte, 31), v2(cte, 495), 2)

        for n in range(10):
            if n != 0:
                draw_text(display, str(n), debug_font, DARK_GRAY, v2((n + 1) * 45 - 25, cte - 20))
                draw_text(display, str(n), debug_font, DARK_GRAY, v2(cte - 20, (n + 1) * 45 - 25))
            else:
                draw_text(display, "0", debug_font, DARK_GRAY, v2(15, 15))

        # Limit
        pygame.draw.line(display, DARK_GRAY, v2(30, self.circle.get_pos().y + self.circle.get_radius()),
                                            v2(495, self.circle.get_pos().y + self.circle.get_radius()), 1)

    def debug(self, display):
        # Limit
        pygame.draw.line(display, DARK_GRAY, v2(30, self.circle.get_pos().y + self.circle.get_radius()),
                                            v2(495, self.circle.get_pos().y + self.circle.get_radius()), 1)

        text = str(self.circle.get_pos().y * 5.25 / 250)[:5] if self.max_amplitude > 0.01 else str(self.circle.get_pos().y * 5.25 / 250)[:5] + " - 5 = " + str(self.circle.get_pos().y * 5.25 / 250 - 5)[:5]
        draw_text(display, text, debug_font, DARK_GRAY, v2(35, self.circle.get_pos().y + 25))

        # GUI
        self.button.draw_button(display)

    def render(self, display):
        # Axis
        self.coordinates(display)
        self.debug(display)
        # System
        pygame.draw.circle(display, WHITE, self.circle.get_pos(), self.circle.get_radius())
        if not self.is_falling:
            pygame.draw.line(display, WHITE, v2(45, 250), v2(self.circle.get_pos().x, self.circle.get_pos().y + self.circle.radius), 2)
            pygame.draw.line(display, WHITE, v2(self.circle.get_pos().x, self.circle.get_pos().y + self.circle.radius), v2(455, 250), 2)
        else:
            pygame.draw.line(display, WHITE, v2(45, 250), v2(455, 250), 2)
