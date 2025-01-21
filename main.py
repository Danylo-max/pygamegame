import pygame
from map1 import *

pygame.init()

pygame.mixer.music.load('jungles.ogg')
pygame.mixer.music.play(-1)

FPS = 60
clock = pygame.time.Clock()
wind_w, wind_h = 700, 500
window = pygame.display.set_mode((wind_w, wind_h))
pygame.display.set_caption('tikertje')

background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (wind_w, wind_h))

block_img = pygame.image.load('block.jpg')
img_gold = pygame.image.load('treasure.png')
img1 = pygame.image.load('sprite1.png')

font = pygame.font.SysFont('Arial', 80)
button_font = pygame.font.SysFont('Arial', 40)

def draw_button(text, rect, color, text_color):
    pygame.draw.rect(window, color, rect)
    text_surface = button_font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    window.blit(text_surface, text_rect)

class Sprite:
    def __init__(self, x, y, w, h, image):
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.transform.scale(image, (w, h))

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed

    def move(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_d]:
            dx = self.speed
        if keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_w]:
            dy = -self.speed
        if keys[pygame.K_s]:
            dy = self.speed

        self.rect.x += dx
        for block in blocks:
            if self.rect.colliderect(block.rect):
                return "LOSE"

        self.rect.y += dy
        for block in blocks:
            if self.rect.colliderect(block.rect):
                return "LOSE"

        if self.rect.colliderect(treasure.rect):
            return "WIN"

blocks = []
block_size = 25
block_x, block_y = 0, 0

for row in lvl1:
    for tile in row:
        if tile == '1':
            blocks.append(Sprite(block_x, block_y, block_size, block_size, block_img))
        elif tile == '2':
            treasure = Sprite(block_x, block_y, 50, 50, img_gold)
        block_x += block_size
    block_x = 0
    block_y += block_size

def reset_game():
    global player1, blocks
    blocks = []
    block_x, block_y = 0, 0

    for row in lvl1:
        for tile in row:
            if tile == '1':
                blocks.append(Sprite(block_x, block_y, block_size, block_size, block_img))
            elif tile == '2':
                treasure.rect.x, treasure.rect.y = block_x, block_y
            block_x += block_size
        block_x = 0
        block_y += block_size

    player1.rect.x, player1.rect.y = 50, 440

player1 = Player(50, 440, 35, 35, img1, 3)

def end_game(message, color):
    running = True
    button_rect = pygame.Rect(wind_w // 2 - 100, wind_h // 2 + 50, 200, 50)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                reset_game()
                running = False

        window.blit(background, (0, 0))
        for block in blocks:
            block.draw()
        treasure.draw()
        player1.draw()

        text_surface = font.render(message, True, color)
        text_rect = text_surface.get_rect(center=(wind_w // 2, wind_h // 2))
        window.blit(text_surface, text_rect)

        draw_button("Пройти заново", button_rect, (0, 150, 0), (200, 200, 20))
        pygame.display.update()
        clock.tick(FPS)

game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    result = player1.move()
    if result == "LOSE":
        end_game("YOU LOSE", (255, 0, 0))
    elif result == "WIN":
        end_game("YOU WIN", (0, 255, 0))

    window.blit(background, (0, 0))
    player1.draw()
    treasure.draw()
    for block in blocks:
        block.draw()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
