import tkinter as tk
from game_config import *
from components.paddle import Paddle
from components.ball import Ball
from components.powerup import PowerUp
from managers.level_manager import LevelManager
from managers.collision_manager import CollisionManager
from managers.game_manager import GameManager
from managers.ui_manager import UIManager

import random


class Game():
    def __init__(self):

        self.root = tk.Tk()
        self.root.title(TITLE)

        self.canvas = tk.Canvas(self.root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=BG)
        self.canvas.pack()

        steuerung_text = "Steuerung ←/→ oder Maus = Bewegen | Leertaste/Rechtsklick = Ball starten | P/ESC = Pause | R = Neustart | M = Menü"
        self.info_label = tk.Label(self.root,
                                   text=steuerung_text,
                                   bg='#1a1a2e',
                                   fg='gray',
                                   font=("Arial", 10))
        
        self.info_label.pack()

        self.level_manager = LevelManager(self.canvas)
        self.powerups = []
        self.menu_visible = True
        self.game_paused = False
        self.spawn_timer = None
        self.level_timer = None
        self.game_loop_timer = None

        # Paddle einfügen
        self.paddle = Paddle(self.canvas, CANVAS_WIDTH // 2, CANVAS_HEIGHT - 30)

        # Blockreihen einfügen
        self.blocks = []

        # Laser
        self.lasers = []

        # Ball
        self.balls = []

        self.collision_manager = CollisionManager()
        self.game_manager = GameManager(self.canvas, self.paddle, self.balls, self.lasers)
        self.ui_manager = UIManager(self.canvas, self.game_manager)
    
        # Events Binden
        self.root.bind("<Left>", self.paddle.move_left)
        self.root.bind("<Right>", self.paddle.move_right)
        self.root.bind("<B1-Motion>", self.paddle.follow_mouse)
        self.root.bind("<space>", self.launch_ball)
        self.root.bind("<Button-3>", self.launch_ball)
        self.root.bind("<r>", self.restart_game)
        self.root.bind("<Button-1>", self.on_click)
        self.root.bind("<p>", self.toggle_pause)
        self.root.bind("<Escape>", self.toggle_pause)
        self.root.bind("<m>", self.return_to_menu)
        self.root.bind("<Motion>", self.handle_motion)

        self.ui_manager.show_main_menu()

    def run(self):
        self.root.mainloop()

    def game_loop(self):
        # Wenn Spiel pausiert - Pause
        if self.game_paused == True:
            return
        
        # Wenn game Over - stoppen
        if self.game_manager.game_over:
            return
    
        
        # Alle Bälle bewegen
        for ball in self.balls:
            if ball.attached:
                ball.follow_paddle(self.paddle)
            else:
                ball.move()

        # Paddle Kollision
        for ball in self.balls:
            self.collision_manager.check_paddle_collision(ball, self.paddle)

        # Block Kollision prüfen, punkte hinzufügen und entfernen zerstörter Blöcke
        for ball in self.balls:
            destroyed = self.collision_manager.check_block_collision(ball, self.blocks)
            for block in destroyed:
                self.game_manager.add_score(block.points)
                position = block.get_position()

                number = random.random()
                if number < POWERUP_CHANCE:
                    power_type = random.choice(["longer_paddle", "multi_ball", "laser", "extra_life", "fireball"])
                    power_up = PowerUp(self.canvas, position[0], position[1], power_type)
                    self.powerups.append(power_up)

                block.destroy()
                self.blocks.remove(block)
        if self.game_manager.current_mode == "levels":
            if self.game_manager.check_level_complete(self.blocks) and not self.game_manager.level_complete:
                self.game_manager.level_complete = True
                self.ui_manager.show_level_complete()
                self.level_timer = self.root.after(2000, self.load_next_level)


        # Alle Powerups bewegen
        for powerup in self.powerups:
            powerup.move()
            powerup.pulse()

        gesammelt = self.collision_manager.check_powerup_collision(self.powerups, self.paddle)
        for powerup in gesammelt:
            self.game_manager.activate_powerup(powerup.type)
            powerup.destroy()
            self.powerups.remove(powerup)

        # Prüfen ob der letzte Ball raus ist
        for ball in self.balls[:]:
            if ball.is_out():
                ball.destroy()
                self.balls.remove(ball)

        # Wenn keine Bälle mehr vorhanden, leben verlieren und neuen Ball ins Spiel geben.
        if len(self.balls) == 0:
            self.game_manager.lose_life()
            if self.game_manager.game_over:
                print("Game Over")
                return
            self.reset_ball()

        # Laser bewegen
        for laser in self.lasers:
            laser.move()

        # Wenn Laser raus - entfernen
        for laser in self.lasers[:]:
            laser_pos = laser.get_position()
            if laser_pos[0] > CANVAS_WIDTH or laser_pos[1] > CANVAS_HEIGHT or laser_pos[2] < 0 or laser_pos[3] < 0:
                laser.destroy()
                self.lasers.remove(laser)

        getroffene_laser, destroyed_blocks = self.collision_manager.check_laser_collision(self.lasers, self.blocks)
        for laser in getroffene_laser:
            laser.destroy()
            self.lasers.remove(laser)
        
        for block in destroyed_blocks:
            self.game_manager.add_score(block.points)
            block.destroy()
            self.blocks.remove(block)

        # Game Over in Endlos modus prüfen
        if self.game_manager.current_mode == "endless":
            for block in self.blocks:
                block_pos = block.get_position()
                if block_pos[3] > DEATH_ZONE:
                    self.game_manager.game_over = True
                    print("Game Over")
                    break


        self.ui_manager.update_display()

        self.game_loop_timer = self.root.after(FRAMERATE, self.game_loop)

    def reset_ball(self):
        """ Neuen ball erstellen und zur Liste hinzufügen"""
        x = CANVAS_WIDTH // 2
        y = CANVAS_HEIGHT - 30
        self.ball = Ball(self.canvas, x, y)
        self.balls.append(self.ball)

    def spawn_new_row(self):
        if self.game_manager.game_over:
            return
        
        self.game_manager.update_difficulty()
        self.level_manager.move_blocks_down(self.blocks)
        new_row = self.level_manager.create_row(50, self.game_manager.difficulty)
        self.blocks.extend(new_row)

        # Intervall mit steigender Geschwindigkeit erhöhren
        neues_intervall = max(3000, ROW_SPAWN_INTERVAL - (self.game_manager.difficulty * 500))
        self.spawn_timer = self.root.after(neues_intervall, self.spawn_new_row)

    def launch_ball(self, event):
        for ball in self.balls:
            ball.launch()

    def load_next_level(self):
        """ Nächstes Level laden oder Gewinn Nachricht anzeigen"""
        # Wenn im Menü, nicht laden
        if self.menu_visible:
            return
        
        # Alle Bälle vom Canvas entfernen:
        for ball in self.balls:
            ball.destroy()
        # alte ball Liste löschen
        self.balls.clear()

        # neuen Ball ins spiel bringen:
        self.ball = Ball(self.canvas, CANVAS_WIDTH // 2, CANVAS_HEIGHT - 50)
        self.balls.append(self.ball)

        if self.game_manager.next_level():
            current_level = self.game_manager.current_level
            level = LEVEL_ORDER[current_level - 1]
            self.blocks = self.level_manager.create_level(level)
        else:
            self.ui_manager.game_won()

    def restart_game(self, event):
        """ Startet das Spiel neu"""
        if self.game_loop_timer:
            self.root.after_cancel(self.game_loop_timer)
            self.game_loop_timer = None


        self.game_manager.reset_game()
        for block in self.blocks:
            block.destroy()
        self.blocks.clear()

        for ball in self.balls:
            ball.destroy()
        self.balls.clear()

        for powerup in self.powerups:
            powerup.destroy()
        self.powerups.clear()

        for laser in self.lasers:
            laser.destroy()
        self.lasers.clear()

        self.ui_manager.hide_game_over()

        for row in range(5):
            y_position = 50 + row * (BLOCK_HEIGHT + BLOCK_SPACES)
            new_blocks = self.level_manager.create_row(y_position)
            self.blocks.extend(new_blocks)

        # Ball einfügen
        self.ball = Ball(self.canvas, CANVAS_WIDTH // 2, CANVAS_HEIGHT - 50)
        self.balls.append(self.ball)

        self.game_loop()

    def on_click(self, event):
        if not self.menu_visible:
            return None

        x = event.x
        y = event.y
        result = self.ui_manager.check_menu_click(x, y)

        if result == "endless":
            self.start_game("endless")
        elif result == "levels":
            self.start_game("levels")
        elif result == "quit":
            self.root.quit()

    def start_game(self, mode):
        # Menü verstecken
        self.ui_manager.hide_main_menu()
        self.menu_visible = False
        self.game_manager.current_mode = mode

        if mode == "endless":
            # Death-Line erstellen:
            self.death_line = self.canvas.create_line(0, DEATH_ZONE, CANVAS_WIDTH, DEATH_ZONE, fill="red", width=2)
            # Reihen erstellen
            for row in range(5):
                y_position = 50 + row * (BLOCK_HEIGHT + BLOCK_SPACES)
                new_blocks = self.level_manager.create_row(y_position)
                self.blocks.extend(new_blocks)
            # Neue Reihen spawnen
            self.spawn_timer = self.root.after(ROW_SPAWN_INTERVAL, self.spawn_new_row)
        elif mode == "levels":
            level = LEVEL_ORDER[0]
            self.blocks = self.level_manager.create_level(level)

        # Ball setzen
        x = CANVAS_WIDTH // 2
        y = CANVAS_HEIGHT - 30
        self.ball = Ball(self.canvas, x, y)
        self.balls.append(self.ball)

        # game loop starten:
        self.game_loop()
        
    def toggle_pause(self, event):
        if self.menu_visible:
            return
        
        if self.game_paused == False:
            # Pausieren und Pause-Text anzeigen
            self.game_paused = True
            self.ui_manager.show_pause()
        else:
            # Fortsetzen und Pause-Text entfernen und Loop wieder starten
            self.game_paused = False
            self.ui_manager.hide_pause()
            self.game_loop()
    
    def return_to_menu(self, event):
        """ Zurück zum Menü """
        if self.menu_visible:
            return
        
        # Als erstes : Game Loop Stoppen
        self.game_manager.game_over = True

        # Falls Spiel pausiert, Pause beenden
        if self.game_paused:
            self.game_paused = False
            self.ui_manager.hide_pause()

        # Timer abbrechen
        if self.spawn_timer:
            self.root.after_cancel(self.spawn_timer)
            self.spawn_timer = None
        if self.level_timer:
            self.root.after_cancel(self.level_timer)
            self.level_timer = None
        if self.game_loop_timer:
            self.root.after_cancel(self.game_loop_timer)
            self.game_loop_timer = None

        # Alle Objekte entfernen
        for ball in self.balls[:]:
            ball.destroy()
 
        self.balls.clear()
        
        for block in self.blocks[:]:
            block.destroy()

        self.blocks.clear()

        for laser in self.lasers[:]:
            laser.destroy()
        
        self.lasers.clear()

        for powerup in self.powerups[:]:
            powerup.destroy()

        self.powerups.clear()


        # Death-Line entfernen (falls vorhanden)
        if hasattr(self, 'death_line') and self.death_line:
            self.canvas.delete(self.death_line)
            self.death_line = None

        # Game-Over Text entfernen falls vorhanden
        try:
            self.ui_manager.hide_game_over()
        
        except:
            pass

        try:
            self.ui_manager.hide_level_complete()
        
        except:
            pass

        # GameManager zurücksetzen
        self.game_manager.reset_game()

        # Menü anzeigen
        self.menu_visible = True
        self.ui_manager.show_main_menu()

    def handle_motion(self, event):
        if self.menu_visible:
            self.ui_manager.handle_hover(event)