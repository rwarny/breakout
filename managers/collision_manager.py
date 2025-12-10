
class CollisionManager():
    """ Verwaltet die Kollisionsprüfungen im Spiel """
    def __init__(self):
        pass

    def check_rectangle_collision(self, rect1, rect2):
        """ Prüft ob zwei Rechtecke sich überlappen"""
        if rect1[2] < rect2[0] or rect1[0] > rect2[2] or rect1[3] < rect2[1] or rect1[1] > rect2[3]:
            return False
        return True
    
    def check_paddle_collision(self, ball, paddle):
        """ Prüft Kollision Ball und Paddle"""

        # Positionen von Ball und Paddle holen
        ball_pos = ball.get_position()
        paddle_pos = paddle.get_position()

        # Prüfen ob sie sich überlappen
        collision = self.check_rectangle_collision(ball_pos, paddle_pos)

        # Falls ja, Richtun gdes Balles umkehren
        if collision:
            ball.dy = -ball.dy
            return True
        # sont ball weiter fliegen lassen
        return False
    
    def check_block_collision(self, ball, blocks):
        """ Prüft Kollision zwischen Ball und Blöcken """
        destroyed_blocks = []
        ball_pos = ball.get_position()

        if ball.is_fireball == True:
            for block in blocks:
                block_pos = block.get_position()
                if self.check_rectangle_collision(ball_pos, block_pos):
                    block.hits_required = 0
                    if block.is_destroyed():
                        destroyed_blocks.append(block)

        else:
            for block in blocks:
                block_pos = block.get_position()
                if self.check_rectangle_collision(ball_pos, block_pos):
                    block.hit()
                    ball.dy = -ball.dy
                    if block.is_destroyed():
                        destroyed_blocks.append(block)
                    break
        
        return destroyed_blocks
    
    def check_powerup_collision(self, powerups, paddle):
        """ Prüft ob das Paddle ein Powerup eingesammelt """
        eingesammelt = []

        paddle_pos = paddle.get_position()

        for powerup in powerups:
            power_pos = powerup.get_position()
            if self.check_rectangle_collision(power_pos, paddle_pos):
                eingesammelt.append(powerup)

        return eingesammelt
    
    def check_laser_collision(self, lasers, blocks):
        """ Prüft Kollision zwischen Lasern und Blöcken """
        getroffene_laser = []
        destroyed_blocks = []

        for laser in lasers:
            laser_pos = laser.get_position()
            for block in blocks:
                block_pos = block.get_position()
                if self.check_rectangle_collision(laser_pos, block_pos):
                    block.hit()
                    getroffene_laser.append(laser)
                    if block.is_destroyed():
                        destroyed_blocks.append(block)
                    break

        return getroffene_laser, destroyed_blocks
