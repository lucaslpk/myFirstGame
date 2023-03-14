import pygame
pygame.init()
pygame.display.set_caption("The GAME.")

# All global vars
screen_W = 400
screen_H = 400
win = pygame.display.set_mode((screen_W, screen_H))

x = 40      # initial position (x,y)         (0,0)------->
y = 380     #                                     |      X
h = 20      #                                     |
w = 20      #                                     V Y             
v = 10      # if starting pos(x,y) is not integer-divisble by 'step"' size v, character may partially disappear from screen

run = True
isJump = False
jumpCount = 10    # jump will be animated in 10 frames up and 10 frames back down, if you want to change it the 10 is hardcoded in jump loop too

while run :
    pygame.time.delay(50)

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > 0:
        x -= v        
    if keys[pygame.K_RIGHT] and x < screen_W - w:
        x += v 
    if not isJump :     # up, down and new jump will be suspended while previous jump lasts
        if keys[pygame.K_SPACE] :
            isJump = True
    else :
        if jumpCount >= -10 :
            if jumpCount >= 0 :
                y -= (jumpCount ** 2) * 0.5     # up we go!!
            else :
                y += (jumpCount ** 2) * 0.5     # what goes up - must come down...
            jumpCount -= 1
        else :
            isJump = False
            jumpCount = 10 


    win.fill((0,0,0))
    pygame.draw.rect(win, (255,0,0), (x,y,w,h))
    pygame.display.update()

pygame.quit()