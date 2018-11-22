# game options/settings
TITLE = "FLAPPY MAN!"
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = "arial"

#Player Property
PLAYER_ACC = 0.3
PLAYER_ACCC = 0
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 10
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"

# Starting Platforms
PLATFORM_LIST = [(230,-100,0,0),
                 (230,-100,0,0)]

REDLINE_LIST = [(125,20, 0, 0)]

FLATPLAT_LIST = [(0,0,0,0)]

CLOUD_LIST = [(WIDTH/2,HEIGHT/2, 0, 150)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0,155,155)
LIGHTGREEN = (0,255, 0)
BGCOLOR = LIGHTBLUE

