from game_config import *

class Block():
    """ Block der vom Ball oder Laser zerstört werden kann """
    def __init__(self, canvas, x, y, color, hits=1):
        self.canvas = canvas

        # Höhe und Breite der Blöcke
        x1 = x
        y1 = y
        x2 = x + BLOCK_WIDTH
        y2 = y + BLOCK_HEIGHT

        # Blöcke zeichnen
        self.id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        self.hits_required = hits
        self.points = hits * 10

    def hit(self):
        """ Treffer vom Ball oder Laser zieht einen benötigten Treffer ab """
        self.hits_required -= 1

    def is_destroyed(self):
        """ Prüfung ob der Block zerstört wurde """
        if self.hits_required == 0:
            return True
        return False
        
    def destroy(self):
        """ Zerstört einen Block """
        self.canvas.delete(self.id)

    def get_position(self):
        return self.canvas.coords(self.id)