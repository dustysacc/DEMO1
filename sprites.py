# sprite classes for game, by Jack Armanini 
# from Mr. Cozort and Kids can code.


import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint, randrange, choice
from settings import *

vec = pg.math.Vector2

class Spritesheet:
    # class for loading and parsing sprite sheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        #returns image 
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image

class Player(Sprite):
    def __init__(self, game):
        # allows layering 
        self._layer = PLAYER_LAYER
        # add player to game groups when instantiated. This is what gets called in main, and then is continually used from thereafter.
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT /2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        print("adding vecs " + str(self.vel + self.acc))
    def load_images(self):
        #this is where animation happens 
        self.standing_frames = [self.game.spritesheet.get_image(690, 406, 120, 201),
                                    #this goes back continously, loading images 
                                self.game.spritesheet.get_image(614, 1063, 120, 191)
                                ]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.game.spritesheet.get_image(678, 860, 120, 201),
                                self.game.spritesheet.get_image(692, 1458, 120, 207)
                                ]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frame = self.game.spritesheet.get_image(382, 763, 150, 181)
        self.jump_frame.set_colorkey(BLACK)
    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)

    
    #controls of the game. this is where we define what happens when we press the defined keys
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x =  -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        # set player friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of the motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # jump to other side of screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos
    # cuts the jump short when the space bar is released

    #restart button: kinda works, more like respawn. Score does not reset, since technically still in game. Maybe would add a restart button with some extra time
    #when in game, aggresively holding it down will eventually make the player eventually end up in place where you can continue going. 
    #this was my attempted fix for the spawning problem. I regret not asking for help .
        if keys[pg.K_ESCAPE]:
            self.pos.x = WIDTH / 2
            self.pos.y = HEIGHT / 2
            print("respawm")
    # the starting of the restart button- i could not figure this one out
        # if keys[pg.K_f]:
        #     self.game =   
        #     g.show_go_screen()
        #     print ("restart")

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -5:
                self.vel.y = -5
    def jump(self):
        #make sure you jump 
        print("jump")
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        # adjust based on checked pixel
        self.rect.y -= 2
        # this part makes sure that bunny will not be allowed to jump when player is not on a platform. This makes sure you cannot double jump or cheat.
        if hits and not self.jumping:
            # play sound only when space bar is hit and while not jumping
            self.game.jump_sound[choice([0,1])].play()
            # tell  program that bunny is jumping up 
            self.jumping = True
            self.vel.y = -PLAYER_JUMP
            print(self.acc.y)
    def animate(self):
        # gets time in miliseconds
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # checking on what character is doing if not moving
        if not self.jumping and not self.walking:
            # gets current  time and checks against 200 miliseconds
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

class Platform(Sprite):
    def __init__(self, game, x, y):
        # allows layering in LayeredUpdates sprite group
        self._layer = PLATFORM_LAYER
        #program to spanw in platforms
        self.groups = game.all_sprites, game.platforms
        Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet.get_image(0, 288, 380, 94), 
                  self.game.spritesheet.get_image(213, 1662, 201, 100),
                  self.game.spritesheet.get_image(218, 1456, 201, 100),
                  self.game.spritesheet.get_image(0, 576, 380, 94)]
        self.image = random.choice(images)
        self.image.set_colorkey(BLACK)
 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if random.randrange(1000) < POW_SPAWN_PCT:
            Pow(self.game, self)
        if random.randrange(100) < COIN_SPAWN_PCT:
            Coin(self.game, self)

class Pow(Sprite):
    #this powerup pushes you forward, honestly makes the game harder as it pushes you off the platform.
    def __init__(self, game, plat):
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = random.choice(['boost'])
        self.image = self.game.spritesheet.get_image(820, 1805, 71, 70)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5
    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        #kill if not needed anymore
        if not self.game.platforms.has(self.plat):
            self.kill()

class Coin(Sprite):
    #the coin. the way we score in this game, each is worth 10
    def __init__(self, game, plat):
        # allows layering 
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.coin
        Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = random.choice(['coin'])
        self.image = self.game.spritesheet.get_image(698, 1931, 84, 84)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5
    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        # checks to see if plat is in the game's platforms group so we can kill the coin instance
        if not self.game.platforms.has(self.plat):
            self.kill()

class SpringMan(Sprite):
    def __init__(self, game):
        self._layer = MOB_LAYER
        # add a groups property where we can pass all instances of this object into game groups. (left for my understanding)
        self.groups = game.all_sprites, game.mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = self.game.spritesheet.get_image(801, 609, 110, 141)
        self.image_up.set_colorkey(BLACK)
        self.image_down = self.game.spritesheet.get_image(801, 609, 110, 141)

        self.image_down.set_colorkey(BLACK)
        self.image = self.image_up
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.rect_top = self.rect.top
        self.vx = randrange(1, 6)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = randrange(HEIGHT/2)
        self.vy = 0
        self.dy = 0.5
    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        self.rect_top = self.rect.top
        if self.vy > 4 or  self.vy < -4:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect.center = center
        self.rect_top = self.rect.top
        self.rect.y += self.vy
        #when to kill springman 
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()

class Mob(Sprite):
    def __init__(self, game):
        self._layer = MOB_LAYER
        # add a groups property where we can pass all instances of this object into game groups
        self.groups = game.all_sprites, game.mobs
        Sprite.__init__(self, self.groups)
        self.game = game

        self.image_up = self.game.spritesheet.get_image(566, 510, 122, 139)
        self.image_up.set_colorkey(BLACK)
        self.image_down = self.game.spritesheet.get_image(568, 1534, 122, 135)

        self.image_down.set_colorkey(BLACK)
        self.image = self.image_up
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.rect_top = self.rect.top
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = randrange(HEIGHT/2)
        self.vy = 0
        self.dy = 0.5
    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        self.rect_top = self.rect.top
        if self.vy > 3 or  self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect.center = center
        self.rect_top = self.rect.top
        self.rect.y += self.vy
        #determines when to despawn the mob
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()

# class Cacti(Sprite):
#     def __init__(self, game, plat):
#         # allows layering in LayeredUpdates sprite group
#         self._layer = POW_LAYER
#         # add a groups property where we can pass all instances of this object into game groups
#         self.groups = game.all_sprites, game.cacti
#         Sprite.__init__(self, self.groups)
#         self.game = game
#         self.plat = plat
#         self.type = random.choice(['cacti'])
#         self.image = self.game.spritesheet.get_image(707, 134, 117, 160)
#         self.image.set_colorkey(BLACK)
#         self.rect = self.image.get_rect()
#         self.rect.centerx = self.plat.rect.centerx
#         self.rect.bottom = self.plat.rect.top - 5
#     def update(self):
#         self.rect.bottom = self.plat.rect.top - 5
#         # checks to see if plat is in the game's platforms group so we can kill the powerup instance
#         if not self.game.platforms.has(self.plat):
#             self.kill()