import pygame 
import os
pygame.init()

WHITE = 250 , 250 ,250 
WIDTH , HEIGHT = 800,700
RED_x = 50
RED_y = 50
YELLOW_x = 650
YELLOW_y = 50
FPS = 60
VEL = 3
SPACESHIP_WIDTH = 50
SPACESHIP_HEIGHT = 60
BLACK = 0, 0, 0
MAX_BULLETS = 3
BULLET_VEL = 7
RED = (255,0,0)
YELLOW = 255,255,0

# Fonts used in game
HEALTH_FONT = pygame.font.SysFont("Arial" , 40)
TEXT_FONT = pygame.font.SysFont("Arial" , 100)

BORDER = pygame.Rect(WIDTH/2 - 5 , 0, 10, HEIGHT)

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(("My First Game"))

# Events Trigger by user
RED_HIT = pygame.USEREVENT +1
YELLOW_HIT = pygame.USEREVENT +2


#importing required images in the game
RED_SPACESHIP = pygame.image.load(
    os.path.join('Assets','spaceship_red.png'))

RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP , (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)) 
RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP , 90)


YELLOW_SPACESHIP = pygame.image.load(
    os.path.join('Assets','spaceship_yellow.png')
)
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP , (SPACESHIP_WIDTH , SPACESHIP_HEIGHT)) , 270
    )

SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join('Assets', 'space.png')),(WIDTH,HEIGHT)
    )


# importing sound 
FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','Gun pistol Fire.mp3'))
COLLISION_SOUND = pygame.mixer.Sound(os.path.join('Assets','grenade.mp3'))

# This function responsible for controls the things which we want to display in the game window
def draw_window(red, yellow, red_bullets , yellow_bullets, RED_HEALTH, YELLOW_HEALTH):
    WIN.blit(SPACE , (0 ,0))
    pygame.draw.rect(WIN ,BLACK, BORDER )

    red_text = HEALTH_FONT.render("Health: " + str(RED_HEALTH), 1 , WHITE)
    yellow_text = HEALTH_FONT.render("Health: " + str(YELLOW_HEALTH), 1 , WHITE)

    WIN.blit(red_text, (10 , 10))
    WIN.blit(yellow_text,(WIDTH - yellow_text.get_width(),10))

    WIN.blit(RED_SPACESHIP,(red.x , red.y))
    WIN.blit(YELLOW_SPACESHIP,(yellow.x, yellow.y) )

    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)

    pygame.display.update()

# controlling the controles of the red spaceship
def red_directions(key_pressed, red):
    if key_pressed[pygame.K_d] and red.x + VEL + red.width < BORDER.x -7:
        red.x += VEL
    if key_pressed[pygame.K_a] and red.x - VEL >0:
        red.x -= VEL
    if key_pressed[pygame.K_w] and red.y - VEL >0 :
        red.y -= VEL
    if key_pressed[pygame.K_s] and red.y + red.height +VEL < HEIGHT:
        red.y += VEL

# controlling the controls of the yellow spaceship
def yellow_directions(key_pressed, yellow):
    if key_pressed[pygame.K_RIGHT] and yellow.x + yellow.width + 5 < WIDTH:
        yellow.x += VEL
    if key_pressed[pygame.K_LEFT] and BORDER.x+ BORDER.width < yellow.x :
        yellow.x -= VEL
    if key_pressed[pygame.K_UP] and yellow.y - VEL > 0 :
        yellow.y -= VEL
    if key_pressed[pygame.K_DOWN] and yellow.y + yellow.height< HEIGHT:
        yellow.y += VEL

# This controles the bullets
def handle_bullets(red_bullets , yellow_bullets , red , yellow):
    for bullet in red_bullets:
        bullet.x += BULLET_VEL                                                              
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)

    for bullet in yellow_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)



def handle_winner(text):
    winner_text = TEXT_FONT.render(text, 1 ,WHITE)
    WIN.blit(
        winner_text , (WIDTH/2 - winner_text.get_width()/2 , HEIGHT/2 - winner_text.get_height()/   2))
    pygame.display.update()
    pygame.time.delay(3000)


# This controls the functioning of the game

def main():
    
    clock = pygame.time.Clock() # this helps in controling the the speed of the game
    red_bullets = []
    yellow_bullets = []
    red = pygame.Rect(RED_x,RED_y, SPACESHIP_WIDTH , SPACESHIP_HEIGHT)
    yellow = pygame.Rect(YELLOW_x,YELLOW_y,SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    RED_HEALTH = 10
    YELLOW_HEALTH = 10

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run == False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullets)<MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x + red.width, red.y + red.height/2-2.5, 10, 5)
                    red_bullets.append(bullet)
                    FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(yellow_bullets)<MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x, yellow.y + yellow.height/2-2.5, 10, 5)
                    yellow_bullets.append(bullet)  
                    FIRE_SOUND.play()
                
            if event.type == RED_HIT:
                RED_HEALTH -=1


            if event.type == YELLOW_HIT:
                YELLOW_HEALTH -=1

        if RED_HEALTH <= 0 :
            COLLISION_SOUND.play()
            handle_winner("Yellow Wins")
            break

        if YELLOW_HEALTH <= 0:
            COLLISION_SOUND.play()
            handle_winner("Red Wins")
            break



        key_pressed = pygame.key.get_pressed()
   
        red_directions(key_pressed,red)
        yellow_directions(key_pressed,yellow)
        draw_window(red,yellow, red_bullets, yellow_bullets, RED_HEALTH , YELLOW_HEALTH)
        handle_bullets(red_bullets, yellow_bullets, red, yellow)
    main()


if __name__ == "__main__":
    main() 