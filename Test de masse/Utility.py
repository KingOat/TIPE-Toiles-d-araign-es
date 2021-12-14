
def draw_text(display, text, font, color, pos):
    img = font.render(text, True, color)
    display.blit(img, pos)