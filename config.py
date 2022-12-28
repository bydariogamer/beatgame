# Display configuration
from pygame import USEREVENT

DISP_TIT = "BEATGAME"
DISP_ICO = "assets/images/stand.png"
DISP_WID = 800
DISP_HEI = 500
BASE_FPS = 60

# Font configuration
FONT_TYPE = "assets/fonts/dogica.ttf"
FONT_SIZE_SMALL = 32
FONT_SIZE_NORMAL = 48
FONT_SIZE_BIG = 64

# Resize factor
resize = None

# Main Menu / Title
GAME_TITLE = ">BEATGAME<"
GAME_AUTHOR = "bydariogamer"
GAME_AUTHOR2 = "Sogolumbo"
MENU_BACKGROUND = "assets/images/title_background.png"

HELP_IMAGE = "assets/images/help.png"

# Ingame
#   Units:
#   position in pixels
#   velocity in pixels per second
HEART_ICON = "assets/images/heart.png"
SHIELD_ICON = "assets/images/shield.png"
WIN_MESSAGE = "YOU WIN"
DEATH_MESSAGE = "YOU LOSE"
PLAYER_ICONS = {
    "run": "assets/images/run.png",
    "stand": "assets/images/stand.png",
    "up": "assets/images/up.png",
    "down": "assets/images/down.png",
    "dead": "assets/images/dead.png",
    "collide": "assets/images/collide.png",
}
PARTICLE_ICON = "assets/images/particle.png"
PARTICLES_PER_SECOND = 20
HEALTH_DAMAGE_SOUND = "assets/sounds/aztec_death_whistle.wav"
HEALTH_DAMAGE_VOLUME = 0.5
SHIELD_DAMAGE_SOUND = "assets/sounds/wrong.wav"
SHIELD_DAMAGE_VOLUME = 0.5
SHIELD_REGENERATION_SOUND = "assets/sounds/shield_regeneration.wav"
SHIELD_REGENERATION_VOLUME = 0.5
STARS_COUNT = 30
STAR_SIZE = 2
FLOOR_HEIGHT = 100
PLAYER_POS_X = 70
VELOCITY_X = 240
VELOCITY_Y_DURING_DAMAGE = 30
JUMP_LENGTH = 1.6  # unit: blocks
JUMP_HEIGHT = 6.25  # unit: height levels
HIGHSCORE_FILENAME = ".score"
SCORE_POINTS_PER_SECOND = 60
SHIELD_MAXIMUM = 4
HEALTH_POINTS_PER_OBSTACLE = 0.09
SONG_ENDEVENT = USEREVENT + 1

# Level generation
BPM_FINDER_SUBSAMPLING = 500
BPM_FINDER_MINIMUM = 48
BPM_FINDER_MAXIMUM = 240
BLOCKS_PER_SECOND_AIM = 4
HEIGHT_LEVELS = 10
MAP_UPPER_QUANTILE = 0.95
MAP_LOWER_QUANTILE = 0.05
RELATIVE_BLOCK_HEIGHT = 0.45  # Amount of space between ground and top of the screen covered by the biggest obstacles

# Debugging
DEBUG_BPM_FINDER = False
DEBUG_SHOW_LEVEL = False
