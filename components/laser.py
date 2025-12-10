from game_config import *

class Laser():
    """ Laser der in eine Richtung fliegt und Blöcke zerstört """
    def __init__(self, canvas, x, y, direction):
        self.canvas = canvas
        self.direction = direction
        self.speed = LASER_SPEED

        # Koordinaten festlegen
        x1 = x
        y1 = y
        x2 = x + LASER_WIDTH
        y2 = y + LASER_HEIGHT

        self.id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=LASER_COL)

    def move(self):
        """ Bewegt die Laser in alle vier Richtungen - (oben, unten, links, rechts) """
        if self.direction == "up":
            self.canvas.move(self.id, 0, -self.speed)
        elif self.direction == "down":
            self.canvas.move(self.id, 0, self.speed)
        elif self.direction == "left":
            self.canvas.move(self.id, -self.speed, 0)
        elif self.direction == "right":
            self.canvas.move(self.id, self.speed, 0)

    def get_position(self):
        return self.canvas.coords(self.id)
    
    def destroy(self):
        """ Zerstört die Laser """
        self.canvas.delete(self.id)