TITLE = "Fatty Platty"
# screen dimension. Changed to accomodate horizontal idea
WIDTH = 1500
HEIGHT = 1000
# frames per second
FPS = 60
# colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
REDDISH = (240,55,66)
#changed color to orange
ORANGE = (255, 116, 0)
#changed the font
FONT_NAME = 'calibri'
SPRITESHEET = "spritesheet_jumper.png"
# data files
HS_FILE = "highscore.txt"
# player settings
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.5
PLAYER_JUMP = 20
# game settings
BOOST_POWER = 20
POW_SPAWN_PCT = 8
COIN_SPAWN_PCT = 11
MOB_FREQ = 5000
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2


PLATFORM_LIST = [(0, HEIGHT - 40),
                 (65, HEIGHT - 300),
                 (20, HEIGHT - 350),
                 (200, HEIGHT - 150),
                 (250, HEIGHT - 450)]
