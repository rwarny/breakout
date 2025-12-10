from game_config import *

class UIManager():
    """ Verwaltet UI-Elemente wie Score, Leben, Menü und Pause """
    def __init__(self, canvas, game_manager):
        self.canvas = canvas
        self.game_manager = game_manager

        # Game Over IDs
        self.show_game_over_id = None
        self.show_score_id = None
        self.show_info_id = None

        # Text Elemente einbauen:
        self.score_id = self.canvas.create_text(
            60, 20,
            text=f"Score: {self.game_manager.score}",
            fill=FONT_COL,
            font=(FONTTYPE, FONTSIZE)
            )
        
        self.live_id = self.canvas.create_text(
            CANVAS_WIDTH-60, 20,
            text=f"Lives: {self.game_manager.lives}",
            fill=FONT_COL,
            font=(FONTTYPE, FONTSIZE)
        )

        self.difficulty_id = self.canvas.create_text(
            CANVAS_WIDTH // 2, 20,
            text=f"Level: {self.game_manager.difficulty}",
            fill=FONT_COL,
            font=(FONTTYPE, FONTSIZE)
        )

        self.balls_id = self.canvas.create_text(
            CANVAS_WIDTH - 60, 40,
            text=f"Balls: {len(self.game_manager.balls)}",
            fill=FONT_COL,
            font=(FONTTYPE, FONTSIZE)
        )

    def update_display(self):
        """ Aktualisiert die Anzeige von Score, Leben und Bällen """
        self.canvas.itemconfig(self.score_id, text=f"Score: {self.game_manager.score}")
        self.canvas.itemconfig(self.live_id, text=f"Lives: {self.game_manager.lives}")
        self.canvas.itemconfig(self.difficulty_id, text=f"Level: {self.game_manager.difficulty}")
        self.canvas.itemconfig(self.balls_id, text=f"Balls: {len(self.game_manager.balls)}")

    def show_level_complete(self):
        """ Zeigt den Level Abgeschlossen Text an """
        self.level_complete_id = self.canvas.create_text(
            CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2,
            text="LEVEL GESCHAFFT",
            fill="yellow",
            font=(FONTTYPE, 40, 'bold')
        )

        self.level_complete_timer = self.canvas.after(5000, lambda: self.canvas.delete(self.level_complete_id))

    def game_won(self):
        """ zeigt den Spiel Gewonnen Text an """
        self.game_won_id = self.canvas.create_text(
            CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2,
            text="SPIEL GEWONNEN",
            fill="yellow",
            font=(FONTTYPE, 40, 'bold')
        )

    def show_game_over(self):
        """ Zeigt den Game Over Text mit Punkten und Info-Nachricht an """
        self.show_game_over_id = self.canvas.create_text(
            CANVAS_WIDTH // 2, (CANVAS_HEIGHT // 2) - 50,
            text=f"GAME OVER",
            fill="red",
            font=(FONTTYPE, 50, 'bold')
        )
        
        self.show_score_id = self.canvas.create_text(
            CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2,
            text=f"Punkte: {self.game_manager.score}",
            fill="yellow",
            font=(FONTTYPE, 24)
        )

        self.show_info_id = self.canvas.create_text(
            CANVAS_WIDTH // 2, (CANVAS_HEIGHT // 2) + 50,
            text="Drücke R für Neustart\nDrücke M um zum Menü zurück zu kehren",
            fill="gray",
            font=(FONTTYPE, 16)
        )

    def hide_game_over(self):
        """ Versteckt den Game Over Text"""
        if self.show_game_over_id:
            self.canvas.delete(self.show_game_over_id)
            self.show_game_over_id = None
        if self.show_score_id:
            self.canvas.delete(self.show_score_id)
            self.show_score_id = None
        if self.show_info_id:
            self.canvas.delete(self.show_info_id)
            self.show_info_id = None

    def show_main_menu(self):
        """ Zeigt das Hauptmenü an """
        self.menu_items = []

        # Titel
        self.title_id = self.canvas.create_text(
            CANVAS_WIDTH // 2, (CANVAS_HEIGHT // 2) - 150,
            text="BREAKOUT", 
            fill="white",
            font=(FONTTYPE, 36, 'bold')
        )
        self.menu_items.append(self.title_id)

        # Position für Button berechnen
        # button 1 Endlos Modus
        x1 = (CANVAS_WIDTH // 2) - 100
        x2 = (CANVAS_WIDTH // 2) + 100
        y1 = (CANVAS_HEIGHT // 2) - 100
        y2 = (CANVAS_HEIGHT // 2) - 50

        # button 2 Level Modus ( unter Button 1, x1 und x2 bleiben)
        y3 = (CANVAS_HEIGHT // 2)
        y4 = (CANVAS_HEIGHT // 2) + 50

        # Button 3 (beenden Button)
        y5 = y4 + 50
        y6 = y5 + 50

        # Buttons:
        self.button_endlos = self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue")
        self.button_level_modus = self.canvas.create_rectangle(x1, y3, x2, y4, fill="purple")
        self.button_beenden = self.canvas.create_rectangle(x1, y5, x2, y6, fill="red")
        self.menu_items.append(self.button_endlos)
        self.menu_items.append(self.button_level_modus)
        self.menu_items.append(self.button_beenden)
        

        # Position für Button Texte
        # button 1
        bx = (CANVAS_WIDTH // 2)
        by1 = (CANVAS_HEIGHT // 2) - 75

        # button 2
        by2 = (CANVAS_HEIGHT // 2) + 25

        # button 3
        by3 = (CANVAS_HEIGHT // 2) + 125

        # Texte 
        self.button_endlos_text = self.canvas.create_text(bx, by1, text="Endlos-Modus", fill="white")
        self.button_level_modus_text = self.canvas.create_text(bx, by2, text="Level-Modus", fill="white")
        self.button_beenden_text = self.canvas.create_text(bx, by3, text="Beenden", fill="white")
        self.menu_items.append(self.button_endlos_text)
        self.menu_items.append(self.button_level_modus_text)
        self.menu_items.append(self.button_beenden_text)

    def hide_main_menu(self):
        """ Versteckt das Hauptmenü """
        for item in self.menu_items:
            self.canvas.delete(item)
        self.menu_items.clear()

    def check_menu_click(self, x, y):
        """ Prüft ob ein Menü Button geklickt wurde """
        if not self.menu_items:
            return None
        
        # Hole Button - Koordinaten
        coords1 = self.canvas.coords(self.button_endlos)
        coords2 = self.canvas.coords(self.button_level_modus)
        coords3 = self.canvas.coords(self.button_beenden)

        # Prüfe ob Klick im Rechteck
        if coords1[0] <= x <= coords1[2] and coords1[1] <= y <= coords1[3]:
            return "endless"
        if coords2[0] <= x <= coords2[2] and coords2[1] <= y <= coords2[3]:
            return 'levels'
        if coords3[0] <= x <= coords3[2] and coords3[1] <= y <= coords3[3]:
            return 'quit'
        
    def show_pause(self):
        """ Zeigt den Pause Text an """
        self.pause_id = self.canvas.create_text(
            CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2,
            text="PAUSED",
            fill="white",
            font=(FONTTYPE, 50, 'bold')
        )

    def hide_pause(self):
        """ Versteckt den Pause Text """
        self.canvas.delete(self.pause_id)

    def hide_level_complete(self):
        """ Versteckt den Level-Abgeschlossen Text wieder """
        # Timer abbrechen falls noch aktiv
        if hasattr(self, 'level_complete_timer') and self.level_complete_timer:
            self.canvas.after_cancel(self.level_complete_timer)
            self.level_complete_timer = None
        # Text löschen
        if hasattr(self, 'level_complete_id') and self.level_complete_id:
            self.canvas.delete(self.level_complete_id)
            self.level_complete_id = None

    def handle_hover(self, event):
        """ Ändert Button-Farben bei Maus-Hover """
        if len(self.menu_items) == 0:
            return
        
        try:
            # Maus Koordinaten holen
            x = event.x
            y = event.y

            # Koordinaten der Buttons holen.
            coords1 = self.canvas.coords(self.button_beenden)
            coords2 = self.canvas.coords(self.button_endlos)
            coords3 = self.canvas.coords(self.button_level_modus)

            # Prüfe ob Klick im Rechteck
            if coords1[0] <= x <= coords1[2] and coords1[1] <= y <= coords1[3]:
                self.canvas.itemconfig(self.button_beenden, fill="#FF6666")
            else:
                self.canvas.itemconfig(self.button_beenden, fill="red")
            if coords2[0] <= x <= coords2[2] and coords2[1] <= y <= coords2[3]:
                self.canvas.itemconfig(self.button_endlos, fill="#6666FF")
            else:
                self.canvas.itemconfig(self.button_endlos, fill="blue")
            if coords3[0] <= x <= coords3[2] and coords3[1] <= y <= coords3[3]:
                self.canvas.itemconfig(self.button_level_modus, fill="#AA55AA")
            else:
                self.canvas.itemconfig(self.button_level_modus, fill="purple")
        
        except:
            pass
