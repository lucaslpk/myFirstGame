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

class player(object) : # need to read more and understand why is there an object argument here?
    def __init__(self, w,h,x,y) -> None:
        self.w = w      # initial position (x,y)         (0,0)------->
        self.h = h      #                                     |      X
        self.x = x      #                                     |
        self.y = y      #                                     V Y  
        self.v = 3                # if starting pos(x,y) is not integer-divisble by "step's" size v, character may partially disappear from screen
        self.isJump = False
        self.jumpCount = 10       # jump will be animated in 10 frames up and 10 frames back down, if you want to change it the 10 is hardcoded in jump loop too
        self.left = False         # these 3 vars will keep track of which way and how many steps is the character walking, for accurate image insertions
        self.right = False
        self.walkCount = 0 
        self.standing = True

    def draw(self, win) :
        if self.walkCount + 1 >= 27 :        # every 27 steps reset counter or risk index error, as len(walkLeft/Right)=9 and img is to change every 3 frames @ 27 fps
            self.walkCount = 0

        if not(self.standing) :
            if self.left :
                win.blit(walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount += 1
            elif self.right :
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1

        else :
            self.walkCount = 0      # so that fram No 0 is blit when standing w/o hardcoding 0 in the procedures below
            if self.left :
                win.blit(walkLeft[self.walkCount//3],(self.x,self.y))       # same procedures as above, for consistency
            elif self.right :
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
            else :              # this wil blit our thug facing screen if both self.left/right are false, which is the case only at the beginning of the game, any other time he stops, we will be facing in the last direction that he walked
                win.blit(char,(self.x,self.y))

class projectile() :
    def __init__(self,x,y,radius,color, facing) -> None:
        self.radius = radius
        self.x = x
        self.y = y
        self.color = color 
        self.facing = facing    # facing Left/Right will be coded as 1 or -1
        self.v = 15 * facing    # so that the velocity will be a vector and will have and orientation (+/-)

    def draw(self, win) :
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius, 1)   # jedynka jst żeby nie był wypełniony, puste dla pełny - zobaczymy

def redrawGameWin() :
    win.blit(bg, (0,0))
    thug.draw(win)

    pygame.display.update()

#mainloop 
thug = player(64,64,40,screen_H - 64)
run = True
while run :
    clock.tick(27)    # FPS from clock instance of pygame.time.Clock class 

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and thug.x > 0:
        thug.x -= thug.v   
        thug.left = True
        thug.right = False  
        thug.standing = False   
    elif keys[pygame.K_RIGHT] and thug.x < screen_W - thug.w:
        thug.x += thug.v 
        thug.left = False
        thug.right = True
        thug.standing = False
    else :              # if neither left nor right key pressed - stand still and reset walkCount 
        thug.walkCount = 0 
    if not thug.isJump :     # up, down and new jump will be suspended while previous jump lasts Edit: up/down was removed, for platform game.
        if keys[pygame.K_UP] :
            thug.isJump = True  # TwTim is adding here left = right = False & reset walk count so the thug doesn't move feet while in the air
    else :
        if thug.jumpCount >= -10 :
            if thug.jumpCount >= 0 :
                thug.y -= (thug.jumpCount ** 2) * 0.5     # up we go!!
            else :
                thug.y += (thug.jumpCount ** 2) * 0.5     # what goes up - must come down...
            thug.jumpCount -= 1
        else :
            thug.isJump = False
            thug.jumpCount = 10 

    redrawGameWin()


pygame.quit()