import pygame
import os
pygame.font.init()
pygame.mixer.init()

# iklj      wsda



WIDTH, HEIGHT          = 900, 500
WIN                    = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE                  = (255,255,255)
BLACK                  = (0,0,0)
RED                    = (255,0,0)
YELLOW                 = (255,255,0)
FPS                    = 60
VEL                    = 3
BULLET_VEL             = 7
BORDER                 = pygame.Rect(WIDTH//2  - 5, 0, 10, HEIGHT)
MAX_BULLETS            = 5
YELLOW_HIT             = pygame.USEREVENT + 1
RED_HIT                = pygame.USEREVENT + 2
SPACE                  = pygame.transform.scale(
    pygame.image.load(os.path.join('templets', 'space.png')), (WIDTH, HEIGHT))
HEALTH_FONT            = pygame.font.SysFont('comicsans', 40)
WINNER_FONT            = pygame.font.SysFont('comicsans', 60)
BULLET_HIT_SOUND       = pygame.mixer.Sound(os.path.join('templets', 'hurt.wav'))
BULLET_FIRE_SOUND      = pygame.mixer.Sound(os.path.join('templets', 'Gun+Silencer.mp3'))


ship_width             = 55
ship_height            = 40
spaceship_scale        = (ship_width,ship_height)
#Yellow space ship
Yellow_spaceship_image = pygame.image.load(
    os.path.join('templets' , 'spaceship_yellow.png'))
Yellow_pos             = (300,100)
Yellow_spaceship_size  = pygame.transform.rotate(pygame.transform.scale(Yellow_spaceship_image ,spaceship_scale),90)
yellow_bullets = []

#Red space ship
Red_spaceship_image    = pygame.image.load(
    os.path.join('templets' , 'spaceship_red.png'))
Red_spaceship_size     = pygame.transform.rotate(pygame.transform.scale(Red_spaceship_image, spaceship_scale),270)
Red_pos = (700, 100)
red_bullets = []
pygame.display.set_caption('Space game')
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 -draw_text.get_width()/2, HEIGHT/2 -draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def Yellow_movment(keys_pressed, yellow):
    if keys_pressed[pygame.K_d] and (yellow.x + VEL) <= (BORDER.x -45): #yellow right
        yellow.x += VEL
    if keys_pressed[pygame.K_a] and (yellow.x - VEL)  >= 0: #yellow left
        yellow.x -= VEL
    if keys_pressed[pygame.K_w] and (yellow.y - VEL) >= (0):#yellow up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and (yellow.y + VEL)  <= (HEIGHT - 55 ) : #yellow down
        yellow.y += VEL

def Red_movment(keys_pressed, red):
    if keys_pressed[pygame.K_l]  and  (red.x + VEL) <= (WIDTH - 45)  : #red right
        red.x += VEL
    if keys_pressed[pygame.K_j]  and  (red.x - VEL)  > (BORDER.x + 5): #red left
        red.x -= VEL
    if keys_pressed[pygame.K_i]  and (red.y - VEL) >= (0) : #red up
        red.y -= VEL
    if keys_pressed[pygame.K_k]  and (red.y + VEL)  <= (HEIGHT - 55 ): #red down
        red.y += VEL


def draw_window( red, yellow, red_bullets, yellow_bullets , red_health, yellow_health):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN,  BLACK, BORDER )
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width()-10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(Red_spaceship_size, (red.x, red.y))
    WIN.blit(Yellow_spaceship_size, (yellow.x, yellow.y))
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)



    pygame.display.update()

def  gameplay():
    red                    = pygame.Rect(700,300,ship_width, ship_height)
    yellow                 = pygame.Rect(100,300,ship_width, ship_height)
    Clock                  = pygame.time.Clock()
    run                    = True
    Winner_text            =""
    red_health             = 10
    YELLOW_health          = 10
    while run:
        Clock.tick(FPS)
        for event in pygame.event.get():
            if event.type  == pygame.QUIT:
                run        = False
                pygame.quit()
            
            if event.type  == pygame.KEYDOWN:
                
                
                if event.key == pygame.K_LCTRL and len(yellow_bullets)  < MAX_BULLETS:
                    bullet = pygame.Rect(
                        (yellow.x + yellow.width) , (yellow.y + yellow.height//2 +4), 10,5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                
                
                if event.key == pygame.K_RCTRL and len(red_bullets)  < MAX_BULLETS:
                    bullet = pygame.Rect(
                        (red.x ) , (red.y +red.height//2+4 ), 10,5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            
            
            
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                YELLOW_health -= 1
                BULLET_HIT_SOUND.play()
        if red_health <=0 :
            Winner_text = 'Yellow wins!!'
        if YELLOW_health <=0 :
            Winner_text = 'Red wins!!'
        if Winner_text != "":
            draw_winner(Winner_text)#someone won!
            break

        # print(len(red_bullets ), len(yellow_bullets))
        keys_pressed = pygame.key.get_pressed()
        Yellow_movment(keys_pressed, yellow)
        Red_movment(keys_pressed, red)
        draw_window(red, yellow, red_bullets, yellow_bullets ,red_health, YELLOW_health)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
    gameplay()

if __name__ == "__main__":
    gameplay()
