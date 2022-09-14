import pygame
import random

pygame.init()
pygame.font.init()

pygame.font.get_init()

pygame.display.set_caption("Racing Game")

font = pygame.font.SysFont(pygame.font.get_default_font(), 40)

screen_dimensions = [840, 650]
screen = pygame.display.set_mode(screen_dimensions)

entities = []

bg = pygame.image.load("bg.png")
bg_rect = bg.get_rect()

bg_y = bg_rect.height / 2

player_spr = pygame.image.load("player.png")
enemy_spr = pygame.image.load("enemy.png")

player_speed = 5
player = None

time_count = 0
time_spawn = 50

enemy_speed = 2

time_sec = 0
time_min = 0

count = 0

class Entity:
    def __init__(self, x, y, spr):
        self.x = x
        self.y = y
        
        self.spr_rect = spr.get_rect()
        
        self.spr = pygame.transform.scale(spr, (self.spr_rect.width * 2, self.spr_rect.height * 2))
        self.spr_rect = self.spr.get_rect()
    
    # it's made for you to override it
    def tick(self):
        pass
    
    def render(self):
        screen.blit(self.spr, (self.x, self.y))

class Car(Entity):
    def __init__(self, x, y, spr):
        Entity.__init__(self, x, y, spr)

class Enemy(Entity):
    def __init__(self, x, y, spr):
        Entity.__init__(self, x, y, spr)
    
    # Overrides Entity.tick(self)
    def tick(self):
        self.y += enemy_speed
        
        if self.y > screen_dimensions[1]:
            entities.remove(self)
        
        if collide(pygame.Rect(self.x, self.y, self.spr_rect.width, self.spr_rect.height), pygame.Rect(player.x, player.y, self.spr_rect.width, self.spr_rect.height)):
            game_over()

def game_over():
    global entities
    
    entities.clear()
    init()

def collide(r1, r2):
    return r1.left < r2.left + r2.width and r1.left + r1.width > r2.left and r1.top < r2.top + r2.height and r1.top + r1.height > r2.top

def init():
    global player, count, time_sec, time_min
    
    time_sec = 0
    time_min = 0
    
    count = 0
    
    player = Car(screen_dimensions[0] / 2, screen_dimensions[1] / 2, player_spr)
    
    entities.append(player)

def tick():
    global bg_y, time_count, time_spawn, count, time_sec, time_min
    
    for e in entities:
        e.tick()
    
    if bg_y > 0:
        bg_y -= 10
    else:
        bg_y = bg_rect.height / 2
    
    if player.x < 150:
        player.x = 150
    elif player.x > 650:
        player.x = 650
    
    if player.y < 0:
        player.y = 0
    elif player.y > screen_dimensions[1] - player.spr_rect.height:
        player.y = screen_dimensions[1] - player.spr_rect.height
    
    count += 1
    
    if count >= 60:
        count = 0
        
        time_sec += 1
        
        if time_sec >= 60:
            time_sec = 0
            
            time_min += 1
    
    time_count += 1
    
    if time_count >= time_spawn:
        time_count = 0
        
        entities.append(Enemy(random.randint(150, 650), 0 - enemy_spr.get_rect().height, enemy_spr))

def render():
    # Draw bg
    screen.blit(bg, pygame.Rect(0, 0 - bg_y, bg_rect.width, bg_rect.height))
    
    for e in entities:
        e.render()
    
    font_img = font.render("Time: " + ("0" if time_min < 10 else "") + str(time_min) + ":" + ("0" if time_sec < 10 else "") + str(time_sec), True, (255, 255, 255))
    
    screen.blit(font_img, (10, 10))

init()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    state = pygame.key.get_pressed()
    
    if state[pygame.K_w]:
        player.y -= player_speed
    elif state[pygame.K_s]:
        player.y += player_speed
    elif state[pygame.K_a]:
        player.x -= player_speed
    elif state[pygame.K_d]:
        player.x += player_speed
    
    # Fill bg
    screen.fill((0, 0, 0))
    
    tick()
    render()
    
    pygame.display.flip()

pygame.quit()
