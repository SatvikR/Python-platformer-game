import pygame

class Button:
    def __init__(self, rect, default_color, hover_color, text, text_color, font):
        self.rect = rect
        self.default_color = default_color
        self.hover_color = hover_color
        self.color = self.default_color
        self.text = text
        self.text_color = text_color
        self.font = font
    
    def check_pos(self): # Returns true if mouse position is on button
        x, y = pygame.mouse.get_pos()

        if self.rect.x < x < (self.rect.x + self.rect.width) and self.rect.y < y < (self.rect.y + self.rect.height):
            return True
        return False
        
    def change_color(self): # Changes color based on mouse position
        if self.check_pos():
            self.color = self.hover_color
        else:
            self.color = self.default_color
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def draw_text(self, screen): # Draws text centered on the button
        x_mid = (2 * (self.rect.x) + self.rect.width) / 2
        y_mid = (2 * (self.rect.y) + self.rect.height) / 2
        prompt = self.font.render(self.text, True, self.text_color)
        screen.blit(prompt, (x_mid - prompt.get_width() / 2, y_mid - prompt.get_height() / 2))