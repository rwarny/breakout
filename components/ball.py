from game_config import *

class Ball():
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.attached = True

        # Berechnen der Koordinaten für den ball
        x1 = x - RADIUS
        y1 = y - RADIUS
        x2 = x + RADIUS
        y2 = y + RADIUS

        # Schatten zeichnen
        self.shadow_id = self.canvas.create_oval(x1+4, y1+4, x2+4, y2+4, fill="#555555")

        # Ball zeichnen
        self.id = self.canvas.create_oval(x1, y1, x2, y2, fill=BALL_COL)

        # Geschwindigkeit
        self.dx = DX
        self.dy = DY

        self.is_fireball = False

    def move(self):
        """ Ball bewegen """
        if self.attached == True:
            return
        self.canvas.move(self.id, self.dx, self.dy)
        self.canvas.move(self.shadow_id, self.dx, self.dy)
        self.check_wall_collision()

    def check_wall_collision(self):
        """ Prüfung ob der Ball mit der oberen, rechten oder linken Wand kollidiert - Wenn ja Ball umkehren"""
        position = self.canvas.coords(self.id)

        if position[0] <= 0:
            self.dx = -self.dx

        if position[1] <= 0:
            self.dy = -self.dy
        
        if position[2] >= CANVAS_WIDTH:
            self.dx = -self.dx
        
    def get_position(self):
        """ Position des Balles ermitteln """
        return self.canvas.coords(self.id)
    
    def is_out(self):
        """ Prüfung ob der Ball nach unten aus dem Canvas gefallen ist"""
        position = self.canvas.coords(self.id)
        if position[1] > CANVAS_HEIGHT:
            return True
        return False
    
    def destroy(self):
        """ Der ball wird gelöscht """
        self.canvas.delete(self.id)
        self.canvas.delete(self.shadow_id)

    def activate_fireball(self):
        """ Feuerball wird aktiviert """
        farbe = '#FF4500'
        self.is_fireball = True
        self.canvas.itemconfig(self.id, fill=farbe)

    def deactivate_fireball(self):
        """ Feuerball wird deaktiviert """
        self.is_fireball = False
        self.canvas.itemconfig(self.id, fill=BALL_COL)

    def launch(self):
        """ Ball wird vom Paddle gelöst"""
        self.attached = False

    def follow_paddle(self, paddle):
        """ Ball klebt mitt am Paddle """
        paddle_pos = paddle.get_position()

        # Mitte des Paddles berechnen:
        paddle_mitte_x = (paddle_pos[0] + paddle_pos[2]) // 2

        # Ball-Koordinaten: zentriert über dem Paddle
        x1 = paddle_mitte_x - RADIUS
        y1 = paddle_pos[1] - RADIUS * 2 - 5
        x2 = paddle_mitte_x + RADIUS
        y2 = paddle_pos[1] - 5

        # Ball auf neue Position setzen
        self.canvas.coords(self.shadow_id, x1+4, y1+4, x2+4, y2+4)
        self.canvas.coords(self.id, x1, y1, x2, y2)

        
