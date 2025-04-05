import pygame
from map1 import * 

pygame.init()

WHITE = (255, 255, 255)  
BLACK = (0, 0, 0)  

FPS = 60
clock = pygame.time.Clock()
wind_w, wind_h = 700, 500
window = pygame.display.set_mode((wind_w, wind_h))
pygame.display.set_caption('Tikertje')

background = pygame.image.load('devetashka_wide.jpg')
background = pygame.transform.scale(background, (wind_w, wind_h))

block_img = pygame.image.load('block.jpg')
img_gold = pygame.image.load('snap.png')
man1 = pygame.image.load('man1.png')
man2 = pygame.image.load('man2.png')
man3 = pygame.image.load('man3.png')
man4 = pygame.image.load('man4.png')
man5 = pygame.image.load('man5.png')
man6 = pygame.image.load('man6.png')
man7 = pygame.image.load('man7.png')
man8 = pygame.image.load('man8.png')
man9 = pygame.image.load('man9.png')
man10 = pygame.image.load('man10.png')
man11 = pygame.image.load('man11.png')
man12 = pygame.image.load('man12.png')
man13 = pygame.image.load('man13.png')
man14 = pygame.image.load('man14.png')
man15 = pygame.image.load('man15.png')
man16 = pygame.image.load('man16.png')

img_s = [man1, man2, man3, man4]
img_w = [man5, man6, man7, man8]
img_a = [man9, man10, man11, man12]
img_d = [man13, man14, man15, man16]

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

class Enemy(Sprite):
    def __init__(self, x, y, w, h, image, speed, x2, direction='right'):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        self.x1 = x
        self.x2 = x2
        self.direction = direction
        self.original_image = self.image  

    def move(self):
        if self.rect.x >= self.x2 and self.direction != 'left':
            self.direction = 'left'
            self.image = pygame.transform.flip(self.original_image, True, False)  

        elif self.rect.x <= self.x1 and self.direction != 'right':
            self.direction = 'right'
            self.image = pygame.transform.flip(self.original_image, True, False)  

        if self.direction == 'right':
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

class Player(Sprite):
    def __init__(self, x, y, w, h, speed, img_s, img_w, img_a, img_d):
        super().__init__(x, y, w, h, img_s[0]) 
        self.speed = speed
        
        self.image_index = 0  
        self.img_s = [pygame.transform.scale(i, (w, h)) for i in img_s]
        self.img_w = [pygame.transform.scale(i, (w, h)) for i in img_w]
        self.img_a = [pygame.transform.scale(i, (w, h)) for i in img_a]
        self.img_d = [pygame.transform.scale(i, (w, h)) for i in img_d]
        self.images = img_s 
        self.anim = False
        self.animation_time = 0
    
    def move(self, blocks, treasure):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_d]:
            dx = self.speed
            self.images = self.img_d

        if keys[pygame.K_a]:
            dx = -self.speed
            self.images = self.img_a

        if keys[pygame.K_w]:  
            dy = -self.speed
            self.images = self.img_w

        if keys[pygame.K_s]:
            dy = self.speed
            self.images = self.img_s

        self.rect.x += dx
        self.rect.y += dy
        for block in blocks:
            if self.rect.colliderect(block.rect):
                return "LOSE"
            
        if treasure and self.rect.colliderect(treasure.rect):
            return "WIN"

        if keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w]:
            self.anim = True
    
    def animate(self):
        self.animation_time += 1  
        if self.animation_time > 10:  
            self.animation_time = 0 
            if not self.anim: 
                self.image_index = 0
            else:
                self.image_index += 1
                if self.image_index > 3:
                    self.image_index = 0
            self.image = self.images[self.image_index]


def load_level(level_data):
    blocks = []
    block_size = 25
    block_x, block_y = 0, 0
    treasure = None 
    
    for row in level_data:
        for tile in row:
            if tile == '1':
                blocks.append(Sprite(block_x, block_y, block_size, block_size, block_img))
            elif tile == '2':  
                treasure = Sprite(block_x, block_y, 50, 50, img_gold)
            block_x += block_size
        block_x = 0
        block_y += block_size

    return blocks, treasure

def reset_game(level_data):
    global player, blocks, treasure
    blocks, treasure = load_level(level_data)
    player.rect.x, player.rect.y = 50, 440

levels = [lvl1, lvl2, lvl3]
current_level = 0

blocks, treasure = load_level(levels[current_level])

player = Player(50, 440, 30, 30, 3, img_s, img_w, img_a, img_d)
enemy1 = Enemy(320, 430, 50, 50, pygame.image.load('enamy.png'), 3, 650)
enemies = [enemy1]

def main_menu():
    running = True
    while running:
        window.fill(WHITE)  
        text_surface = font.render("Главное меню", True, BLACK)
        text_rect = text_surface.get_rect(center=(wind_w // 2, wind_h // 4))
        window.blit(text_surface, text_rect)

        button_rect_1 = pygame.Rect(wind_w // 2 - 100, wind_h // 2 - 50, 200, 50)
        draw_button("Начать игру", button_rect_1, (0, 150, 0), (200, 200, 20))

        button_rect_2 = pygame.Rect(wind_w // 2 - 100, wind_h // 2 + 50, 200, 50)
        draw_button("Выход", button_rect_2, (150, 0, 0), (200, 200, 20))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect_1.collidepoint(event.pos):
                    running = False 
                elif button_rect_2.collidepoint(event.pos):
                    pygame.quit()  
                    exit()

def game_loop():
    global current_level

    game = True
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False

        result = player.move(blocks, treasure)
        player.animate()

        if result == "LOSE":
            end_game("YOU LOSE", (255, 0, 0), lambda: reset_game(levels[current_level]))
        elif result == "WIN":
            current_level += 1
            if current_level < len(levels):
                end_game("YOU WIN", (0, 255, 0), lambda: reset_game(levels[current_level]), is_win=True)
            else:
                end_game("YOU WON ALL LEVELS!", (0, 255, 0), lambda: pygame.quit())

        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                end_game("YOU LOSE", (255, 0, 0), lambda: reset_game(levels[current_level]))

        window.blit(background, (0, 0))
        player.draw()
        if treasure:
            treasure.draw()
        for enemy in enemies:
            enemy.draw()
            enemy.move()
        for block in blocks:
            block.draw()

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

def end_game(message, color, next_level=None, is_win=False):
    running = True
    button_rect = pygame.Rect(wind_w // 2 - 100, wind_h // 2 + 50, 200, 50)
    if is_win:
        next_level_button_rect = pygame.Rect(wind_w // 2 - 100, wind_h // 2 + 150, 200, 50)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    next_level()  
                    running = False
                if is_win and next_level_button_rect.collidepoint(event.pos):
                    if next_level:
                        next_level()  
                        running = False

        window.blit(background, (0, 0))
        for block in blocks:
            block.draw()
        if treasure:
            treasure.draw()
        player.draw()

        text_surface = font.render(message, True, color)
        text_rect = text_surface.get_rect(center=(wind_w // 2, wind_h // 2))
        window.blit(text_surface, text_rect)

        draw_button("Пройти заново", button_rect, (0, 150, 0), (200, 200, 20))

        if is_win:
            draw_button("Next Level", next_level_button_rect, (0, 0, 150), (255, 255, 255))

        pygame.display.update()
        clock.tick(FPS)



main_menu()
game_loop()

pygame.quit()
