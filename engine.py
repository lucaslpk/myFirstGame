import pygame
pygame.init()
pygame.display.set_caption("The GAME.")

# All global vars
screen_W = 850
screen_H = 480
win = pygame.display.set_mode((screen_W, screen_H))
clock = pygame.time.Clock()
bulletSound = pygame.mixer.Sound('sounds/Game_bullet.wav')
hitSound = pygame.mixer.Sound('sounds/Game_hit.wav')
punchedSound = pygame.mixer.Sound('sounds/Game_punched.wav')
respawnSound = pygame.mixer.Sound('sounds/Game_respawn.wav')
killedSound = pygame.mixer.Sound('sounds/Game_killed.wav')
music = pygame.mixer.music.load('sounds/Game_music.mp3')
#pygame.mixer.music.play(-1)
score = 0

bg = pygame.image.load('sprites/bg.jpg')
char =pygame.image.load('sprites/standing.png')


class player(object) : 
    walkLeft =  [pygame.image.load('sprites/L1.png'),pygame.image.load('sprites/L2.png'),pygame.image.load('sprites/L3.png'),pygame.image.load('sprites/L4.png'),pygame.image.load('sprites/L5.png'),pygame.image.load('sprites/L6.png'),pygame.image.load('sprites/L7.png'),pygame.image.load('sprites/L8.png'),pygame.image.load('sprites/L9.png')]
    walkRight = [pygame.image.load('sprites/R1.png'),pygame.image.load('sprites/R2.png'),pygame.image.load('sprites/R3.png'),pygame.image.load('sprites/R4.png'),pygame.image.load('sprites/R5.png'),pygame.image.load('sprites/R6.png'),pygame.image.load('sprites/R7.png'),pygame.image.load('sprites/R8.png'),pygame.image.load('sprites/R9.png')]

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
        self.hitbox = (self.x+18, self.y+14, 26, 50)    # you can draw hitbox around populated pixels in characters' sprites visually check how it fits.

    def draw(self, win) :
        if self.walkCount + 1 >= 27 :        # every 27 steps reset counter or risk index error, as len(self.walkLeft/Right)=9 and img is to change every 3 frames @ 27 fps
            self.walkCount = 0

        if not(self.standing) :
            if self.left :
                win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right :
                win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1

        else :
            self.walkCount = 0      # so that frame No 0 is blit when standing w/o hardcoding 0 in the procedures below
            if self.left :
                win.blit(self.walkLeft[self.walkCount//3],(self.x,self.y))       # same procedures as above, for consistency
            elif self.right :
                win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
            else :              # this will blit our thug facing screen if both self.left/right are false, which is the case only at the beginning of the game, any other time he stops, we will be facing in the last direction that he walked
                win.blit(char,(self.x,self.y))
        self.hitbox = (self.x+18, self.y+14, 26, 50)        # update hitbox's position (as dimension stay the same, 26x50)

class enemy(object) : 
    walkLeft =  [pygame.image.load('sprites/L1E.png'),pygame.image.load('sprites/L2E.png'),pygame.image.load('sprites/L3E.png'),pygame.image.load('sprites/L4E.png'),pygame.image.load('sprites/L5E.png'),pygame.image.load('sprites/L6E.png'),pygame.image.load('sprites/L7E.png'),pygame.image.load('sprites/L8E.png'),pygame.image.load('sprites/L9E.png'),pygame.image.load('sprites/L10E.png'),pygame.image.load('sprites/L11E.png')]
    walkRight = [pygame.image.load('sprites/R1E.png'),pygame.image.load('sprites/R2E.png'),pygame.image.load('sprites/R3E.png'),pygame.image.load('sprites/R4E.png'),pygame.image.load('sprites/R5E.png'),pygame.image.load('sprites/R6E.png'),pygame.image.load('sprites/R7E.png'),pygame.image.load('sprites/R8E.png'),pygame.image.load('sprites/R9E.png'),pygame.image.load('sprites/R10E.png'),pygame.image.load('sprites/R11E.png')]

    def __init__(self, w,h,x,y, range) -> None:
        self.w = w     
        self.h = h     
        self.x = x     
        self.y = y     
        self.v = 3  
        self.start = range[0]
        self.end = range[1]   
        self.path = [self.start, self.end]          # to keep track of where enemy is
        self.walkCount = 0 
        self.hitbox = (self.x+17, self.y+4, 31, 53) # rec (x, y, w, h)
        self.hitsTaken = 0
        self.visible = True
        respawnSound.play()

    def draw(self, win) :
        if self.visible :
            self.move()
            if self.walkCount + 1 >= 33 :        # every 33 steps reset counter because we got set of 22 sprites = 11 in each direction, sprite change every 3 frames
                self.walkCount = 0

            if self.v < 0 :                      # enemy has a velocity negative or positive, so we don't need self.left/right booleans - sprawdź czy da się uprościć playera
                win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            else :
                win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            self.hitbox = (self.x+20, self.y+4, 28, 53)
            pygame.draw.rect(win, (43,166,57), (self.x+20, self.y, 30 - self.hitsTaken, 4))
            pygame.draw.rect(win, (210,43,43), (self.x+50 - self.hitsTaken, self.y, self.hitsTaken, 4))

    def move(self) :
        if self.v > 0 :
            if self.x + self.v < self.path[1] :    # if it's not going to  reach the right end with the next step
                self.x += self.v                   # allow him to take that step
                self.walkCount += 1
            else :                                 # and if it does
                self.v *= -1                       # turn around
                self.walkCount = 0 
        else :
            if self.x + self.v > self.path[0] :    # +self.v because it is negative (or 0)    
                self.x += self.v                   
                self.walkCount += 1
            else :                                
                self.v *= -1                      # powtarzamy tu 2 razy to samo zastanów się czy nie mozna tego skompaktowac
                self.walkCount = 0 

    def hit(self) :
        self.hitsTaken += 1        
        if self.hitsTaken > 30 :
            self.visible = False
            killedSound.play()
        else :
            hitSound.play()

class projectile() :
    def __init__(self,x,y,radius,color, facing) -> None:
        self.radius = radius
        self.x = x
        self.y = y
        self.color = color 
        self.facing = facing    # facing Left/Right will be coded as -1 or 1
        self.v = 15 * facing    # so that the velocity will be a vector and will have and orientation (+/-)
        bulletSound.play()

    def draw(self, win) :
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)   # jedynka jest żeby nie był wypełniony, puste dla pełny - zobaczymy

def redrawGameWin() :
    win.blit(bg, (0,0))
    text = font.render("Score: " + str(score), 1, (0,0,0))
    win.blit(text, (650,25))
    thug.draw(win)
    alien.draw(win)
    for bullet in bullets :
        bullet.draw(win)
    pygame.display.update()

#mainloop 
font = pygame.font.SysFont('comicsans', 30, True)
thug = player(64,64,40,screen_H - 64)
alien = enemy(64,64,540,screen_H - 57,(50, 750))
run = True
bullets = []          # so that multiple objects of projectile class can be on screen at the same time
shootingCoolOff = 0
while run :
    clock.tick(27)    # FPS from clock instance of pygame.time.Clock class 
    if shootingCoolOff > 0 :
        shootingCoolOff -= 1

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            run = False

    for bullet in bullets :                                 # for every bullet in bullets list
        if bullet.y - bullet.radius > alien.hitbox[1] and bullet.y + bullet.radius < alien.hitbox[1] + alien.hitbox[3] : # checks if bulet is vertically within goblin hitbox rec range
            if bullet.x + bullet.radius > alien.hitbox[0] and bullet.x - bullet.radius < alien.hitbox[0] + alien.hitbox[2] : # checks if bullet is horizontally within hitbox
                alien.hit()     # alien is only hit if the full diameter of the bullet is inside his hitbox, in both directions (check 2 above coniditionals carefully)
                score +=1                
                bullets.pop(bullets.index(bullet))          # if bullet hit target remove it from the list
        if bullet.x > 0 and bullet.x < screen_W :           # if the bullet is on screen (only checks horizontal here)
            bullet.x += bullet.v                            # move the bullet one frame every time while mainloop runs
        else:                                               # if off screen
            bullets.pop(bullets.index(bullet))              # remove from list ==> list.pop()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootingCoolOff == 0 :
        facing = 0                                      # facing was defined in if/elif branches, so if thug was facing forward = error
        if thug.left :
            facing = -1
        elif thug.right :
            facing = 1    
        if len(bullets) < 15 and facing in(-1, 1):       # max 15 bullets at the same time and can't shoot if facing forward
            bullets.append(projectile(round(thug.x + thug.w//2), round(thug.y +thug.h//2), 5, (255,0,0), facing))
            shootingCoolOff = 9 
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
        thug.standing = True
        thug.walkCount = 0 
    
    if not thug.isJump :     # up, down and new jump will be suspended while previous jump lasts Edit: up/down was removed, for platform game.
        if keys[pygame.K_UP] :
            thug.isJump = True  # TwTim is adding here left = right = False & reset walk count so the thug doesn't move feet while in the air
    else :
        if thug.jumpCount >= -10 :
            if thug.jumpCount >= 0 :
                thug.y -= (thug.jumpCount ** 2) * 0.25     # up we go!!
            else :
                thug.y += (thug.jumpCount ** 2) * 0.25     # what goes up - must come down...
            thug.jumpCount -= 1
        else :
            thug.isJump = False
            thug.jumpCount = 10 

    redrawGameWin()


pygame.quit()