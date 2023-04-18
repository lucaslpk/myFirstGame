import pygame
pygame.init()
pygame.display.set_caption("The GAME.")

# All global vars
screen_W = 850
screen_H = 480
win = pygame.display.set_mode((screen_W, screen_H))
bg = pygame.image.load('sprites/bg.jpg')
clock = pygame.time.Clock()
font1 = pygame.font.SysFont('comicsans', 30, True)
font2 = pygame.font.SysFont('arial', 60, True)
font3 = pygame.font.SysFont('arial', 20, True)


# All Sounds
bulletSound = pygame.mixer.Sound('sounds/Game_bullet.wav')
hitSound = pygame.mixer.Sound('sounds/Game_hit.wav')
punchedSound = pygame.mixer.Sound('sounds/Game_punched.wav')
respawnSound = pygame.mixer.Sound('sounds/Game_respawn.wav')
killedSound = pygame.mixer.Sound('sounds/Game_killed.wav')
music = pygame.mixer.music.load('sounds/Game_music.mp3')
#pygame.mixer.music.play(-1)

# All Classes and Functions - definitions
class player(object) : 
    walkLeft =  [pygame.image.load('sprites/L1.png'),pygame.image.load('sprites/L2.png'),pygame.image.load('sprites/L3.png'),pygame.image.load('sprites/L4.png'),pygame.image.load('sprites/L5.png'),pygame.image.load('sprites/L6.png'),pygame.image.load('sprites/L7.png'),pygame.image.load('sprites/L8.png'),pygame.image.load('sprites/L9.png')]
    walkRight = [pygame.image.load('sprites/R1.png'),pygame.image.load('sprites/R2.png'),pygame.image.load('sprites/R3.png'),pygame.image.load('sprites/R4.png'),pygame.image.load('sprites/R5.png'),pygame.image.load('sprites/R6.png'),pygame.image.load('sprites/R7.png'),pygame.image.load('sprites/R8.png'),pygame.image.load('sprites/R9.png')]
    char = pygame.image.load('sprites/standing.png')

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
        self.hitbox = (self.x+18, self.y+14, 26, 50)    # you can draw hitbox around populated pixels in characters' sprites to visually check how it fits.
        self.punchedCoolOff = 0
        self.punchesTaken = 0
        self.shootingCoolOff = 0

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
                win.blit(self.char,(self.x,self.y))
        self.hitbox = (self.x+18, self.y+14, 26, 50)        # update hitbox's position (as dimension stay the same, 26x50)
        pygame.draw.rect(win, (43,166,57), (self.x+20, self.y+7, 30 - self.punchesTaken*3, 4))
        pygame.draw.rect(win, (210,43,43), (self.x+50 - self.punchesTaken*3, self.y+7, self.punchesTaken*3, 4))
    
    def punched(self) :
        global run
        self.punchesTaken += 1  
        if self.punchesTaken > 10 :
                #self.visible = False   we will see if we disaapear thug after he's killed
                killedSound.play()
                game_over("defeat")
        else :
            punchedSound.play()

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
        self.killed = False
        respawnSound.play()
        self.visible = False
        global ufo 
        ufo = saucer(-330,160)

    def draw(self, win) :
        if not self.killed and self.visible :
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
        if self.y < screen_H - 57 :
            self.y += 2
        else: 
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
            self.killed = True
            killedSound.play()
        else :
            hitSound.play()

class saucer(object) :
    beamOff = pygame.image.load('sprites/Saucer-no-beam320.png')
    beamOn = pygame.image.load('sprites/Saucer320.png')
               
    def __init__(self,x, y) -> None:
        self.x = x     
        self.y = y
        self.v = 20 
        self.beam = False
        self.timer = 4 * 27   # 4s @ 27 FPS, 

    def move(self, ufoLandingX, aliens) :        
        if self.v != 0 :
            self.x += self.v
        if 540 - self.x < 560 and self.v != 0 :   # in order to stop in the right place ufo needs to start slowing down @560 distance, slow down by 0.5 per frame. Exact stopping point also depends on original insertion point (here -330) and integer division by initial velocity
            self.v = self.v - 0.5
        if self.x == ufoLandingX - 160 :
            self.timer -=1
            if self.timer <= 3 * 27 :
                self.beam = True
                aliens[-1].visible = True
            if self.timer < 1 * 27 :
                self.beam = False
            if self.timer < 0 * 27 :
                self.v -= 0.5


    def draw(self, win, ufoLandingX, aliens) :
        self.move(ufoLandingX, aliens)
        if self.beam :
            win.blit(self.beamOn, (self.x,self.y))
        else :
            win.blit(self.beamOff, (self.x,self.y))

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

class Button : 
    def __init__(self, text, x, y, enabled) -> None:
        self.text = text
        self.x = x
        self.y = y
        self.enabled = enabled
        self.draw(win)

    def draw(self, win) :
        button_text = font3.render(self.text, True, ('black'))
        button_rect = pygame.rect.Rect(self.x, self.y, 150, 50)
        pygame.draw.rect(win, 'gray', button_rect, 0, 5)            # solid grey
        pygame.draw.rect(win, 'black', button_rect, 2, 5)           # edge in black
        win.blit(button_text, (self.x + 75 - button_text.get_width()//2, self.y + 25- button_text.get_height()//2))

    def check_click(self) :
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]  # get_pressed method returns all mouse button presses, [0] index is for left MB
        button_rect = pygame.rect.Rect(self.x, self.y, 150, 50)  # redefining same thing as in draw()?? Not a super elegant solution from tutorial - rethink approach
        if left_click and button_rect.collidepoint(mouse_pos) and self.enabled :
            return True
        else:
            return False

def redrawGameWin(aliens, bullets, thug, ufoLandingX, score) :
    win.blit(bg, (0,0))
    text = font1.render("Score: " + str(score), 1, (0,0,0))
    win.blit(text, (650,25))
    text = font3.render("Left / Right arrows to Move", 1, (255,0,0))
    win.blit(text, (25,25))
    text = font3.render("Up arrow to Jump", 1, (255,0,0))
    win.blit(text, (25,50))
    text = font3.render("Space to Shoot", 1, (255,0,0))
    win.blit(text, (25,75))
    ufo.draw(win, ufoLandingX, aliens)
    for alien in aliens :
        alien.draw(win)
    for bullet in bullets :
        bullet.draw(win)
    thug.draw(win)    

    pygame.display.update()

def main() :
    # Mainloop 
    global run
    # vars to initilize at start    s
    score = 0
    bodyCount = 0
    thug = player(64,64,40,screen_H - 64)
    ufoLandingX = 540
    aliens = []
    aliensLanded = 0
    respawnCoolOff = 0
    bullets = []          # so that multiple objects of projectile class can be on screen at the same time
    run = True

    while run :
        clock.tick(27)    # FPS from clock instance of pygame.time.Clock class 
        if bodyCount == 6 :
            # run = False
            game_over("victory")

        if thug.shootingCoolOff > 0 :
            thug.shootingCoolOff -= 1
        if thug.punchedCoolOff > 0 :
            thug.punchedCoolOff -= 1
        if respawnCoolOff > 0 :
            respawnCoolOff -= 1
        else :
            if len(aliens) < 3 and aliensLanded < 6:
                aliens.append(enemy(64,64,ufoLandingX - 25, screen_H - 140,(50, 736)))   
                respawnCoolOff = 8 * 27 # 8s @ 27 FPS  
                aliensLanded += 1

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False

        for alien in aliens :                                       # if there are no more aliens = no bullet animation = SERIOUS BUG
            if alien.killed :
                aliens.pop(aliens.index(alien))
                respawnCoolOff = 3 * 27
                bodyCount += 1
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

        keys = pygame.key.get_pressed()   # this works different than keys in Sudoku, this returns sth like a dictionary(???) that contains pairs, where key is any of the 106 keys on keybord and value is True/False depending on whether it is pressed or not

        if thug.punchedCoolOff == 0 :
            for alien in aliens :
                if thug.hitbox[1] + thug.hitbox[3] > alien.hitbox[1] + alien.hitbox[3]//2 and thug.hitbox[1] < alien.hitbox[1] + alien.hitbox[3]//2: # vertical collision is when bottom of thug's hitbox is below center af alien's hitbox, which is where his punching hand is and punching hand height is below top of thug hitbox, otherwise it would detect collision with alien stil in the process of landing
                    if thug.hitbox[0] + thug.hitbox[2] > alien.hitbox[0] and thug.hitbox[0] < alien.hitbox[0] :            
                        thug.punchedCoolOff = 27
                        punchedLeft = True
                        thug.punched()
                    elif thug.hitbox[0] < alien.hitbox[0] + alien.hitbox[2] and thug.hitbox[0] > alien.hitbox[0] :
                        thug.punchedCoolOff = 27
                        punchedLeft = False
                        thug.punched()

            if keys[pygame.K_SPACE] and thug.shootingCoolOff == 0 :
                facing = 0                                      # facing was defined in if/elif branches, so if thug was facing forward = error
                if thug.left :
                    facing = -1
                elif thug.right :
                    facing = 1    
                if len(bullets) < 15 and facing in(-1, 1):       # max 15 bullets at the same time and can't shoot if facing forward
                    bullets.append(projectile(round(thug.x + thug.w//2), round(thug.y +thug.h//2), 5, (255,0,0), facing))
                    thug.shootingCoolOff = 9 

            if keys[pygame.K_LEFT] and thug.x > 0 :
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

        else : # here what to do within 1s after punch
                thug.standing = True
                thug.left = False       # with this
                thug.right = False      # and this it should blit standing
                thug.walkCount = 0 
                if punchedLeft and thug.x > 0 :
                    thug.x -= thug.v * 2
                elif not punchedLeft and thug.x < screen_W - thug.w:
                    thug.x += thug.v * 2

        redrawGameWin(aliens, bullets, thug, ufoLandingX, score)

def game_over(result):
    pressed = False 
    button_replay = Button("Play Again", screen_W//2 - screen_W//12 - 100, screen_H//2 + 25, True)
    button_quit = Button("Quit", screen_W//2 + screen_W/12 - 50, screen_H//2 + 25, True)
    while not pressed :
        clock.tick(10)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
        if button_replay.check_click() :
            main()
        if button_quit.check_click() :
            pygame.quit()
        pygame.draw.rect(win, (32,245,246), (screen_W//4, screen_H//4, screen_W//2, screen_H//2), 0, 10)
        text = font1.render("Game over: " + result + "!", 1, (0,0,0))
        win.blit(text, (screen_W//2 - text.get_width()//2, screen_H//2 - 50))
        button_replay.draw(win)
        button_quit.draw(win)

        pygame.display.update()

main()
pygame.quit()