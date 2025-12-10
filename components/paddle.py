from game_config import *

class Paddle():
    """ Schläger den der Spieler mit der Maus oder Tastatur steuert """
    def __init__(self, canvas, x, y):
        self.canvas = canvas

        # Höhe und Breite des Paddle: 
        x1 = x - (PADDLE_WIDTH // 2)
        y1 = y - (PADDLE_HEIGHT // 2)
        x2 = x + (PADDLE_WIDTH // 2)
        y2 = y + (PADDLE_HEIGHT // 2)

        self.id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=PADDLE_COL)

    def move_left(self, event):
        """ Der Schläger wird nach Links bewegt """
        # canvas.move(id, dx, dy) - dx negativ = nach links
        position = self.canvas.coords(self.id)

        if position[0] > 0:
            self.canvas.move(self.id, -SPEED, 0)

    def move_right(self, event):
        """ Der Schläger wird nach Rechts bewegt """
        # dx positiv = nach rechts
        position = self.canvas.coords(self.id)

        if position[2] < CANVAS_WIDTH:
            self.canvas.move(self.id, SPEED, 0)

    def follow_mouse(self, event):
        """ Bewegt den Schläger mit der Maus"""
        position = self.canvas.coords(self.id)
        aktuelle_breite = position[2] - position[0]

        # Maus Position holen
        mouse_x = event.x

        # Neue Koordinaten berechnen (Schläger zentriert um Maus)
        x1 = mouse_x - (aktuelle_breite // 2)
        x2 = mouse_x + (aktuelle_breite // 2)

        if x1 < 0:
            x1 = 0
            x2 = aktuelle_breite

        if x2 > CANVAS_WIDTH:
            x2 = CANVAS_WIDTH
            x1 = CANVAS_WIDTH - aktuelle_breite


        # Y-Position bleibt immer gleich!!
        y1 = CANVAS_HEIGHT - 30 - (PADDLE_HEIGHT // 2)
        y2 = CANVAS_HEIGHT - 30 + (PADDLE_HEIGHT // 2)

        # Schläger auf neue Position setzen
        self.canvas.coords(self.id, x1, y1, x2, y2)

    def get_position(self):
        return self.canvas.coords(self.id)
    
    def make_longer(self):
        """ Macht den Schläger nach Links und Rechts doppelt so lang """
        position = self.canvas.coords(self.id)

        mitte = (position[0] + position[2]) // 2
        x1 = mitte - PADDLE_WIDTH
        x2 = mitte + PADDLE_WIDTH

        new_position = self.canvas.coords(self.id, x1, position[1], x2, position[3])
    
    def reset_size(self):
        """ Setzt die Länge zurück """
        position = self.canvas.coords(self.id)

        mitte = (position[0] + position[2]) // 2
        x1 = mitte - PADDLE_WIDTH // 2
        x2 = mitte + PADDLE_WIDTH // 2

        new_position = self.canvas.coords(self.id, x1, position[1], x2, position[3])
    