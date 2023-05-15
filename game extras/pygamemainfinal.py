import pygame 
from pygame.locals import *
import os
pygame.font.init()
pygame.mixer.init()


width, height = 1200, 750
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Best Game You Will Ever Play!')


pink = (255, 200, 200) # pink background
black = (100, 100, 100) 
orange_color = (245, 132, 66)
blue_color = (66, 139, 245)
yellow = (245, 230, 66)

border = pygame.Rect(0, width//3.5, width, 12) # horizontal border ratios

bullet_hit_sound = pygame.mixer.Sound('extras/bullet_impact.mp3')
bullet_fire_sound = pygame.mixer.Sound('extras/sniper.mp3')

font = pygame.font.SysFont('bold', 55)
winner_font = pygame.font.SysFont('bold', 120)

time = 50 

velocity = 8

bullet_velocity = 12

max_bullets = 5

ufo_width, ufo_height = 85, 70

orange_hit = pygame.USEREVENT + 1
blue_hit = pygame.USEREVENT + 2

blue_ufo_image = pygame.image.load (os.path.join('extras','ufoblue.png'))
blue_ufo = pygame.transform.scale(blue_ufo_image, (ufo_width, ufo_height))

orange_ufo_image = pygame.image.load (os.path.join('extras','ufoorange.png'))
orange_ufo = pygame.transform.rotate(pygame.transform.scale(orange_ufo_image, (ufo_width, ufo_height)), 5)

space = pygame.transform.scale(pygame.image.load(os.path.join('extras', 'space.png')),(width, height))

def draw_window(blue, orange, orange_bullets, blue_bullets, orange_health, blue_health):
    window.blit(space, (0, 0))
    pygame.draw.rect(window, black, border)
    
    orange_health_text = font.render('Mars UFO HP: ' + str(orange_health), 1, orange_color)
    blue_health_text = font.render('Neptune UFO HP: ' + str(blue_health), 1, blue_color)
    
    window.blit(orange_health_text, (10, 10))
    window.blit(blue_health_text, (10, height//2 + 330))
    window.blit(blue_ufo, (blue.x , blue.y))
    window.blit(orange_ufo, (orange.x , orange.y))
    
    for bullet in orange_bullets:
        pygame.draw.rect(window, orange_color, bullet)
        
    for bullet in blue_bullets:
        pygame.draw.rect(window, blue_color, bullet)
    
    pygame.display.update()

    
def orange_movement(keys, orange): # different movement keys for orange player. (d,g,r,f)
    if keys[pygame.K_d] and orange.x - velocity > 0: # moves to the left
        orange.x -= velocity
    if keys[pygame.K_g] and orange.x + velocity + orange.width < width: # moves to the right
        orange.x += velocity
    if keys[pygame.K_r] and orange.y - velocity > 0: # moves up
        orange.y -= velocity
    if keys[pygame.K_f] and orange.y + velocity + orange.height < height/2.3 + 10 : # moves down
        orange.y += velocity
        
def blue_movement(keys, blue):  # different movement keys for blue player. (h,k,u,j)
    if keys[pygame.K_h] and blue.x - velocity > 0: # moves to the left
        blue.x -= velocity
    if keys[pygame.K_k] and blue.x + velocity + blue.width < width : # moves to the right
        blue.x += velocity
    if keys[pygame.K_u] and blue.y + velocity > height/2: # moves up
        blue.y -= velocity
    if keys[pygame.K_j]  and blue.y + velocity + blue.height < width/1.6 - 10: # moves down
        blue.y += velocity

def handle_bullets(orange_bullets, blue_bullets, orange, blue):
    for bullet in orange_bullets:
        bullet.y += bullet_velocity
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(blue_hit))
            orange_bullets.remove(bullet)
        elif bullet.y > height:
            orange_bullets.remove(bullet)
            
    for bullet in blue_bullets:
        bullet.y -= bullet_velocity
        if orange.colliderect(bullet):
            pygame.event.post(pygame.event.Event(orange_hit))
            blue_bullets.remove(bullet)
        elif bullet.y < 0:
            blue_bullets.remove(bullet)

def draw_winner(text):
    draw_text = winner_font.render(text, 1, yellow)
    window.blit(draw_text, (width//2 - draw_text.get_width()/2, height/2 - draw_text.get_height()/2))
    
    pygame.display.update()
    pygame.time.delay(6000)
    
def main():
    blue = pygame.Rect(700, 300, ufo_width, ufo_height)
    orange = pygame.Rect(100, 300, ufo_width, ufo_height)
    
    blue_bullets = []
    orange_bullets = []
    
    orange_health = 15
    blue_health = 15
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(time)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(orange_bullets) < max_bullets:
                    bullet = pygame.Rect(
                        orange.x + orange.width//2 + 2, orange.y, 10, 5
                        )
                    orange_bullets.append(bullet)
                    bullet_fire_sound.play()
                    
                if event.key == pygame.K_RSHIFT and len(blue_bullets) < max_bullets:
                    bullet = pygame.Rect(
                        blue.x + blue.width//2 + 2, blue.y + blue.height//2, 10, 5
                        )
                    blue_bullets.append(bullet)
                    bullet_fire_sound.play()
    
            if event.type == orange_hit:
                orange_health -= 1 
                bullet_hit_sound.play()
                
            if event.type == blue_hit:
                blue_health -= 1
                bullet_hit_sound.play()
                
        winner_text = ''
        if orange_health <= 0:
            winner_text = 'UFO from Mars won!'
            
        if blue_health <= 0:
            winner_text = 'UFO from Neptune won!'
            
        if winner_text != '':
            draw_winner(winner_text)
            break
    
        keys = pygame.key.get_pressed()
        orange_movement(keys, orange)
        blue_movement(keys, blue)
        
        handle_bullets(orange_bullets, blue_bullets, orange, blue)
        
        draw_window(blue, orange, orange_bullets, blue_bullets, orange_health, blue_health)
        
        
    main()
    


if __name__ == '__main__':
    main()