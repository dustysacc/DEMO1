# this file was created by Jack Armanini
# Sources: goo.gl/2KMivS, kids can code (shoutout to that guy), Mr. Cozort: who somehow made it possible for me to understand this crazy stuff

'''
**********Gameplay ideas:
Something like jetpack joyride, or jumpy. I need to do something that is not too difficult for me, as I know that this is thing that I struggle on

**********Cosmetics
Change mobs- add a spring man, but keep the evil flying things, so then we have two mobs, make it harder?
Multiple platform types: The cake bois, coin is a carrot. I know i call it a coin, but carrots are what we are after.
Background is orange = cuz bunnies like carrots

**********Bugs
sometimes jumping on the enemies will jump you up too high
If you fall, you dont actually die, the game continues to run and you cannot do anything except restart: added respawn button to counteract this

I have a really bad problem where the new platforms have a super delayed spawn on the side scroll. 
I have spent hours trying to fix it and a bunch of YT videos but still have not figured it out.
I put in the "respawn" to counteract this, but still, feels bad.


**********Gameplay fixes

Random platform spawn will leave player with nowhere to go. I honestly think my spawning system is messed up, maybe fixed it

Side scrolling will sometimes move character with the scroll, this happens with mobs, powerups, and sometimes the coins

**********Features
Varied powerups: Jump on top of mobs to jump high, there is also one that sends you forward a little. This last one honestly just messes you up more (lol) and makes it hard
Horizontal Scroller: game is very wide, more immersive and expansive than the original vertical game.
Coin/ carrot: the main goal of this game is to get coins, not the amount of distance you cover. These coins move with against you as the gane continues on, making it harder
Respawn button: When you press escape, game resets your position to the middle of the screen, allows you to continue

'''

import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        #init game window
        # initialtion of pygame and game window, where all the magic happens
        pg.init()
        # sound
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Platty ")
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
    def load_data(self):
        print("load data is called...")
        # sets up directory name
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
    
        try:
            with open(path.join(self.dir, "highscore.txt"), 'r') as f:
                self.highscore = int(f.read())
                print(self.highscore)
        except:
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                self.highscore = 0
                print("exception")
        # where image comes in
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))       
        # load sounds
   
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = [pg.mixer.Sound(path.join(self.snd_dir, 'Jump18.wav')),
                            pg.mixer.Sound(path.join(self.snd_dir, 'Jump24.wav'))]
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump29.wav'))

      #game initiation                      
    def new(self):
        self.score = 0
        # add all sprites to the pg group
        self.all_sprites = pg.sprite.LayeredUpdates()
        # creates the platforms 
        self.platforms = pg.sprite.Group()
        # add powerups
        self.powerups = pg.sprite.Group()
        
        self.mob_timer = 0
        self.coin = pg.sprite.Group()
        # add player 
        self.player = Player(self)
        # add mobs
        self.mobs = pg.sprite.Group()
        #add springman
        self.springman = pg.sprite.Group()
        # call new platform 
        for plat in PLATFORM_LIST:
            # no longer need to assign to variable because we're passing self.groups in Sprite library
            Platform(self, *plat)
        # load music
        pg.mixer.music.load(path.join(self.snd_dir, 'happy.ogg'))
        # start running game 
        self.run()
    def run(self):
        # game loop: keeps game going
        # plays music
        pg.mixer.music.play(loops=-1)
        # set boolean playing to true
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(1500)
    def update(self):
        self.all_sprites.update()
        
        # mob spawning method
        now = pg.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)
        # mob hits
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        if mob_hits:
            if self.player.pos.y - 35 < mob_hits[0].rect_top:
                print("hit top")
                print("player is hit at" + str(self.player.pos.y))
                print("mob is " + str(mob_hits[0].rect_top))
                self.player.vel.y = -BOOST_POWER
            else:
                print("player is " + str(self.player.pos.y))
                print("mob is " + str(mob_hits[0].rect_top))
                self.playing = False
        #SPRING BOIS 
        if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            SpringMan(self)
        # mob hits
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        if mob_hits:
            if self.player.pos.y - 35 < mob_hits[0].rect_top:
                print("hit top")
                print("player is hit at" + str(self.player.pos.y))
                print("mob is " + str(mob_hits[0].rect_top))
                self.player.vel.y = -BOOST_POWER
            else:
                print("player is " + str(self.player.pos.y))
                print("mob is " + str(mob_hits[0].rect_top))
                self.playing = False

        # determining whether player can jump 
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                find_lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > find_lowest.rect.bottom:
                        print("hit rect bottom " + str(hit.rect.bottom))
                        find_lowest = hit   
                # fall if center is off platform
                if self.player.pos.x < find_lowest.rect.right + 10 and self.player.pos.x > find_lowest.rect.left - 10:
                    if self.player.pos.y < find_lowest.rect.centery:
                        self.player.pos.y = find_lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
                # scroll platforms 

    #working on making a horizontal scroll: finally got it to work, but had to trouble shoot for days
        if self.player.rect.right >= WIDTH / 1.5:
            # creating a scroll that goes with player when reaches certain x velocity and position
            self.player.pos.x -= max(abs(self.player.vel.x), 2)
            
            for springman in self.springman:
                # create scroll based on x velocity
                springman.rect.x += max(abs(self.player.vel.x), 2)
            for plat in self.platforms:
                # create  scroll based on  x velocity
                plat.rect.x -= max(abs(self.player.vel.x), 1.5)
                if plat.rect.top >= WIDTH + 500:
                    plat.kill()
                    self.score += 10
        # when bunny (player) hits  a powerup 
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.boost_sound.play()
                self.player.vel.x = BOOST_POWER
                self.player.jumping = False
    
        for coin in self.coin:
            coin.rect.x -= max(abs(self.player.vel.x), 2)
        
        # how game ends = death
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 10:
            self.playing = False
        # generate new  platforms as you continue to move
        while len(self.platforms) < 20:
            Platform(self, random.randrange(100,1250), 
                            random.randrange(-1, 1250))
            # width = random.randrange(50, 1000)
            # self.platforms(random.randrange(WIDTH-width, 0)), random.randrange(-75,-30), width, (20)

        "if player hits a coin"
        coin_hits = pg.sprite.spritecollide(self.player, self.coin, True)
        for coin in coin_hits:
            if coin.type == 'coin': 
                self.boost_sound.play()
                #slight jump to signal that the coin is aquired
                self.player.vel.y = -10
                self.player.jumping = False
                self.score += 10
    def events(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.player.jump()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE:
                        # cutting jump
                        self.player.jump_cut()
    def draw(self):
        self.screen.fill(ORANGE)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # double buffering - renders a frame "behind" the displayed frame. Im leaving this comment here for my own understanding.
        pg.display.flip()
    def wait_for_key(self): 
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type ==pg.KEYUP:
                    waiting = False
    #start screen                
    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("WASD to move, Space to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to play...", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text("High score " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()
    def show_go_screen(self):
        if not self.running:
            print("not running...")
            return
        self.screen.fill(BLACK)
        self.draw_text("You lost!", 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("WASD to move, Space to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to play...", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text("High score " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT/2 + 40)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("new high score!", 22, WHITE, WIDTH / 2, HEIGHT/2 + 60)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))

        else:
            self.draw_text("High score " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT/2 + 40)
        pg.display.flip()
        self.wait_for_key()
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect() 
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()

g.show_start_screen()

while g.running:
    g.new()
    try:
        g.show_go_screen()
    except:
        print("can't load...")