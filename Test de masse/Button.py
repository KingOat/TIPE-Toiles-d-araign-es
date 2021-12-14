import pygame

v2 = pygame.math.Vector2


class Button(pygame.sprite.Sprite):
    """Button Class"""

    def __init__(self, position=v2(0, 0), image=None, scale_size=v2(0, 0), color=None, text=None):
        """Initialize attributes"""
        super().__init__()
        self.position = position
        self.scale_size = scale_size

        if image:
            self.surf = pygame.transform.scale(image, scale_size)
        else:
            self.surf = pygame.Surface(scale_size)
            self.surf.fill(color)
            self.font = pygame.font.SysFont('Bauhuas 93', 30)
            self.text = self.font.render(text, True, [255, 255, 255])
            text_position = [self.surf.get_rect().centerx / 2,
                             self.surf.get_rect().centery / 2]
            self.surf.blit(self.text, text_position)

        self.rect = self.surf.get_rect()

    def draw_button(self, display):
        display.blit(self.surf, [(self.position.x), (self.position.y)])

    def hovering_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        conditions = [mouse_pos[0] in range(int(self.position.x), int(self.position.x + self.scale_size.x)),
                      mouse_pos[1] in range(int(self.position.y), int(self.position.y + self.scale_size.y))]
        if all(conditions):
            return True

    def is_pressed(self):
        pressed = pygame.mouse.get_pressed(3)
        if self.hovering_mouse() and pressed[0]:
            return True
        else:
            return False
