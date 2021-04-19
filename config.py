DISP_TIT = 'BEATGAME'
DISP_ICO = 'assets/images/stand.png'
DISP_WID = 800
DISP_HEI = 500
BASE_FPS = 60.0

FONT_TYPE = 'assets/fonts/8bitOperatorPlus-Bold.ttf'
FONT_SIZE_SMALL     = 32
FONT_SIZE_NORMAL    = 48
FONT_SIZE_BIG       = 64

# Main Menu / Title
GAME_TITLE  = '> B E A T G A M E <'
GAME_AUTHOR = 'bydariogamer'
MENU_BACKGROUND = 'assets/images/title_background.png'

HELP_IMAGE = 'assets/images/help.png'

# Ingame
#   Units:
#   position in pixels 
#   velocity in pixels per second
HEART_ICON = 'assets/images/heart.png'
ECU_ICON   = 'assets/images/ecu.png'
WIN_MESSAGE   = 'YOU WIN'
DEATH_MESSAGE = 'YOU LOSE'
PLAYER_ICONS = {
    'run':      'assets/images/run.png',
    'stand':    'assets/images/stand.png',
    'up':       'assets/images/up.png',
    'down':     'assets/images/down.png',
    'dead':     'assets/images/dead.png',
    'collide':  'assets/images/collide.png'
}
PARTICLE_ICON = 'assets/images/particle.png'
PARTICLES_PER_SECOND = 20
WRONG_SOUND  = 'assets/sounds/wrong.wav'
WRONG_VOLUME = 0.4
STARS_COUNT  = 30
STAR_SIZE    = 2
FLOOR_HEIGHT = 100
PLAYER_POS_X = 70
VELOCITY_X   = 240
VELOCITY_Y_DURING_DAMAGE = 30
VELOCITY_Y_ON_JUMP       = 900
JUMPS_PER_SECOND         = 2
HIGHSCORE_FILENAME = '.score'
SCORE_POINTS_PER_SECOND = 60
SHIELD_MAXIMUM          = 10

# Level generation
BPM_FINDER_SUBSAMPLING = 500
BPM_FINDER_MINIMUM     = 48
BPM_FINDER_MAXIMUM     = 240
BLOCKS_PER_SECOND_AIM  = 4
HEIGHT_LEVELS          = 10
MAP_UPPER_QUANTILE     = 0.95
MAP_LOWER_QUANTILE     = 0.05
RELATIVE_BLOCK_HEIGHT  = 0.45 # Amount of space between ground and top of the screen covered by the biggest obstacles

# Debugging
DEBUG_BPM_FINDER = False
DEBUG_SHOW_LEVEL = False