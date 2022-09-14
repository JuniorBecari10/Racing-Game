import pygame
pygame.init()

screen_dimensions = [840, 650]
screen = pygame.display.set_mode(screen_dimensions)

entities = []

bg = pygame.image.load("bg.png")
bg_rect = bg.get_rect()

bg_y = bg_rect.height / 2

player_spr = pygame.image.load("player.png")
player_speed = 5
player = None

enemy_speed = 2

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
        self.y -= enemy_speed

def init():
    global player
    
    player = Car(screen_dimensions[0] / 2, screen_dimensions[1] / 2, player_spr)
    
    entities.append(player)

def tick():
    global bg_y
    
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

def render():
    # Draw bg
    screen.blit(bg, pygame.Rect(0, 0 - bg_y, bg_rect.width, bg_rect.height))
    
    for e in entities:
        e.render()

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
