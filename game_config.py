from utils.shapes import * 
# Constants

# Hauptfenster
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
TITLE = "Breakout"
BG = '#1a1a2e'

# Schläger Einstellungen
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_COL = '#FFFFFF'
SPEED = 40

# Ball Einstellungen
RADIUS = 10
BALL_COL = "#FFEE00"
DX = 5
DY = 5

# Block Einstellungen
BLOCK_WIDTH = 70
BLOCK_HEIGHT = 20
BLOCK_SPACES = 2
BLOCK_COLORS = ["#0400FF", "#00AEFF", "#760492", "#07FC44", "#FF0000", "#FD8F00", "#1D6E48", "#9B053E", "#470AB8", "#EE14A5"]

# Spiel Einstellungen
LIVES = 3
FRAMERATE = 20

# Schrift Einstellung
FONTTYPE = "Arial"
FONTSIZE = 14
FONT_COL = '#FFFFFF'

# Power Ups:
POWER_WIDTH = 30
POWER_HEIGHT = 15
FALL_SPEED = 3
POWERUP_DURATION = 5000

# Power-UP Typen:
POWER_COLORS = {
    "longer_paddle": "green",
    "multi_ball": "blue",
    "laser": "red",
    "extra_life": "magenta",
    "fireball": '#FF4500'
}

# Power up Chance
POWERUP_CHANCE = 0.3

LASER_WIDTH = 4
LASER_HEIGHT = 15
LASER_SPEED = 8
LASER_INTERVAL = 200
LASER_COL = "#EEFF00"

# Endlos Mode:
ROW_SPAWN_INTERVAL = 10000
DEATH_ZONE = CANVAS_HEIGHT - 100

# Level Modus:
LEVEL_ORDER = [digit_0, digit_1, digit_2, digit_3, digit_4, digit_5, digit_6, digit_7, digit_8, digit_9, spirale,
               herz, letter_a, letter_b, letter_c, letter_d, letter_e, letter_f, letter_g, letter_h, letter_i, letter_j, smiley,
               stern, letter_k, letter_l, letter_m, letter_n , letter_o, letter_p, letter_q, letter_r, letter_s, letter_t, regenbogen,
               pyramide, letter_u, letter_v, letter_w, letter_x, letter_y, letter_z, rechteck]