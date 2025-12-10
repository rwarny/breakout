from game_config import *
from components.ball import Ball
from components.laser import Laser
import random

class GameManager():
    """ Verwaltet Spiellogik, Score, Leben und Schwierigkeit """
    def __init__(self, canvas, paddle, balls, lasers):
        self.canvas = canvas
        self.paddle = paddle
        self.balls = balls
        self.lasers = lasers
        self.lives = LIVES
        self.score = 0
        self.game_over = False
        self.current_mode = "endless"
        self.laser_active = False
        self.difficulty = 1
        self.level_complete = False
        self.current_level = 1

    def lose_life(self):
        """ Zieht ein Leben ab und prüft auf Game Over """
        self.lives -= 1

        if self.lives == 0:
            self.game_over = True

    def add_score(self, points):
        """ Fügt Punkte zum Score hinzu """
        self.score += points

    def activate_powerup(self, power_type):
        """ Aktiviert den Effekt eines Powerups """

        if power_type == "extra_life":
            self.lives += 1

        elif power_type == "multi_ball":
            zahl = random.randint(1, 10)

            # Position vom originalen Ball holen
            if len(self.balls) > 0:
                position = self.balls[0].get_position()
                x = (position[0] + position[2]) // 2
                y = (position[1] + position[3]) // 2
            else:
                position = self.paddle.get_position()
                x = (position[0] + position[2]) // 2
                y = (position[1] - 20)

            for i in range(zahl):
                # neuen Ball erstellen auf zufälliger Position erstellen
                neuer_ball = Ball(self.canvas, x, y)
                neuer_ball.dx = random.choice([-4, -3, 3, 4])
                neuer_ball.dy = random.choice([-4, -3, 3, 4])
                self.balls.append(neuer_ball)

        elif power_type == "longer_paddle":
            self.paddle.make_longer()
            self.canvas.after(POWERUP_DURATION, self.paddle.reset_size)

        elif power_type == "laser":
            # Position vom ersten ball holen
            self.laser_active = True
            self.shoot_lasers()
            self.canvas.after(POWERUP_DURATION, self.stop_laser)

        elif power_type == "fireball":
            for ball in self.balls:
                ball.activate_fireball()

            self.canvas.after(POWERUP_DURATION, self.stop_fireball)
            
    def shoot_lasers(self):
        if len(self.balls) < 1:
            return
        
        if self.laser_active == False:
            return
        try:

            # Position vom ersten Ball holen
            if len(self.balls) > 0:
                position = self.balls[0].get_position()
                x = (position[0] + position[2]) // 2
                y = (position[1] + position[3]) // 2
            else:
                position = self.paddle.get_position()
                x = (position[0] + position[2]) // 2
                y = position[1] - 20

            richtungen = ["up", "down", "left", "right"]
            for richtung in richtungen:
                neuer_laser = Laser(self.canvas, x, y, richtung)
                self.lasers.append(neuer_laser)
            self.canvas.after(LASER_INTERVAL, self.shoot_lasers)

        except:
            pass

    def stop_laser(self):
        self.laser_active = False
    
    def stop_fireball(self):
        for ball in self.balls:
            ball.deactivate_fireball()

    def update_difficulty(self):
        """ Erhöht die Schwierigkeit basierend auf Score """
        # Level 1: 0 Punkte, Level 2: 500 Punkte, Level 3: 1500 Punkte, Level 4: 3000 u.s.w.
        punkte_fuer_level = self.difficulty * 500
        neue_difficulty = self.difficulty

        if self.score >= punkte_fuer_level:
            neue_difficulty = self.difficulty + 1

        # Nur wenn Schwierigkeit wirklich gestiegen ist:
        if neue_difficulty > self.difficulty:
            self.difficulty = neue_difficulty

            # Ball geschwindigkeit erhöhren (max 9)
            for ball in self.balls:
                if abs(ball.dx) < 8:
                    ball.dx = ball.dx + (1 if ball.dx > 0 else -1)
                    ball.dy = ball.dy + (1 if ball.dy > 0 else -1)
    
    def check_level_complete(self, blocks):
        """ Prüft ob ein Level beendet wurde """
        if len(blocks) == 0:
            return True
        return False
    
    def next_level(self):
        """ geht zum nächsten Level weiter """
        self.current_level += 1
        self.level_complete = False
        if self.current_level > len(LEVEL_ORDER):
            return False
        else:
            return True
        
    def reset_game(self):
        """ Setzt alle Werte auf Anfang zurück """
        self.lives = LIVES
        self.score = 0
        self.game_over = False
        self.level_complete = False
        self.current_level = 1
        self.difficulty = 1

