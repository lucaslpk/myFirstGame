import pygame
pygame.init()
pygame.display.set_caption("The GAME.")

# All global vars
screen_W = 850
screen_H = 480
win = pygame.display.set_mode((screen_W, screen_H))

bg = pygame.image.load('bg.jpg')
char =pygame.image.load('standing.png')
walkLeft =  [pygame.image.load('L1.png'),pygame.image.load('L2.png'),pygame.image.load('L3.png'),pygame.image.load('L4.png'),pygame.image.load('L5.png'),pygame.image.load('L6.png'),pygame.image.load('L7.png'),pygame.image.load('L8.png'),pygame.image.load('L9.png')]
walkRight = [pygame.image.load('R1.png'),pygame.image.load('R2.png'),pygame.image.load('R3.png'),pygame.image.load('R4.png'),pygame.image.load('R5.png'),pygame.image.load('R6.png'),pygame.image.load('R7.png'),pygame.image.load('R8.png'),pygame.image.load('R9.png')]
clock = pygame.time.Clock()

w = 64                # initial position (x,y)         (0,0)------->
h = 64                #                                     |      X
x = 40                #                                     |
y = screen_H - h      #                                     V Y             
v = 3                # if starting pos(x,y) is not integer-divisble by 'step"' size v, character may partially disappear from screen
isJump = False
jumpCount = 10       # jump will be animated in 10 frames up and 10 frames back down, if you want to change it the 10 is hardcoded in jump loop too
left = False         # these 3 vars will keep track of which way and how many steps is the character walking, for accurate image insertions
right = False
walkCount = 0 

def redrawGameWin() :
    global walkCount
    win.blit(bg, (0,0))
    if walkCount + 1 >= 27 :        # every 27 steps need to reset counter or index error, as len(walkLefr/Right)=9 and img is to change every 3 frames @ 27 fps
        walkCount = 0
    if left :
        win.blit(walkLeft[walkCount//3],(x,y))
        walkCount += 1
    elif right :
        win.blit(walkRight[walkCount//3], (x,y))
        walkCount += 1
    else :
        win.blit(char,(x,y))
        walkCount = 0

    pygame.display.update()

#mainloop 
run = True
while run :
    clock.tick(27)    # FPS from clock instance of pygame.time.Clock class 

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > 0:
        x -= v   
        left = True
        right = False     
    elif keys[pygame.K_RIGHT] and x < screen_W - w:
        x += v 
        left = False
        right = True
    else :              # if neither left nor right key pressed - stand still and reset walkCount
        left = False
        right = False
        walkCount = 0 
    if not isJump :     # up, down and new jump will be suspended while previous jump lasts
        if keys[pygame.K_SPACE] :
            isJump = True  # he is adding here keft = right = False & reset walk count
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

    redrawGameWin()


pygame.quit()