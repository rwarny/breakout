from game_config import *

class PowerUp():
    """
    Power-Up das vom Spieler eingesammelt werden kann.
    
    Typen: extra_life, longer_paddle, multi_ball, laser, fireball
    """
    def __init__(self, canvas, x, y, power_type):
        self.canvas = canvas
        self.type = power_type
        self.speed = FALL_SPEED
        self.pulse_grow = True
        self.pulse_amount = 0
    

        # Höhe und Breite der Power-Ups
        x1 = x
        y1 = y
        x2 = x + POWER_WIDTH
        y2 = y + POWER_HEIGHT

        self.id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=POWER_COLORS[self.type])

    def move(self):
        """ Bewegt das Power-Up nach unten"""
        self.canvas.move(self.id, 0, self.speed)

    def get_position(self):
        return self.canvas.coords(self.id)
    
    def destroy(self):
        """ Entfernt das Power-Up"""
        self.canvas.delete(self.id)
    
    def pulse(self):
        """ Lässt das Power-Up pulsieren (größer/kleiner werden) """

        position = self.get_position()
        x1 = position[0]
        y1 = position[1]
        x2 = position[2]
        y2 = position[3]

        if self.pulse_grow:
            self.canvas.coords(self.id, x1-1, y1-1, x2+1, y2+1)
            self.pulse_amount += 1
        else:
            self.canvas.coords(self.id, x1+1, y1+1, x2-1, y2-1)
            self.pulse_amount -= 1

        if self.pulse_amount >= 3:
            self.pulse_grow = False
        if self.pulse_amount <= 0:
            self.pulse_grow = True