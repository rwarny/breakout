import random
from game_config import *
from components.block import Block
from utils.shapes import SHAPE_COLORS

class LevelManager():
    """ Verwaltet Block-Reihen und Level Erstellung """
    def __init__(self, canvas):
        self.canvas = canvas

    def create_row(self, y_position, difficulty=1):
        """ Erstellt eine Reihe mit zufälligen Blöcken """
        # Liste für alle Bläcker dieser Reihe
        blocks = []

        # Berechnung wie viele Blöcke in eine Reihe passen
        blocks_per_row = CANVAS_WIDTH // (BLOCK_WIDTH + BLOCK_SPACES)

        # Für jeden Block in der Reihe:
        for i in range(blocks_per_row):
            # X Position berechnen
            x = i * (BLOCK_WIDTH + BLOCK_SPACES)

            # Zufällige Farbe wählen:
            color = random.choice(BLOCK_COLORS)

            # Zufällige Treffer (1-3)
            hits = random.randint(1, 3 + difficulty)

            # Block erstellen
            block = Block(self.canvas, x, y_position, color, hits)

            # Block zur Liste hinzufügen
            blocks.append(block)

        # Liste zurückgeben
        return blocks
    
    def move_blocks_down(self, blocks):
        """ bewegt die Blöcke nach unten """
        for block in blocks:
            self.canvas.move(block.id, 0, BLOCK_HEIGHT + BLOCK_SPACES)

    def create_level(self, shape_array):
        """ Erstellt ein Level aus dem Shape-Array"""
        blocks = []

        form_width = len(shape_array[0]) * (BLOCK_WIDTH + BLOCK_SPACES)
        offset_x = (CANVAS_WIDTH - form_width) // 2

        for row_index, row in enumerate(shape_array):
            for col_index, cell in enumerate(row):
                if  cell == 0:
                    continue

                elif cell == 1:
                    color = random.choice(BLOCK_COLORS)
                    hits = random.randint(1, 5)
                    x = offset_x + col_index * (BLOCK_WIDTH + BLOCK_SPACES)
                    y = 50 + row_index * (BLOCK_HEIGHT + BLOCK_SPACES)
                    block = Block(self.canvas, x, y, color, hits )
                    blocks.append(block)
                elif cell in SHAPE_COLORS:
                    color = SHAPE_COLORS[cell]
                    hits = random.randint(1, 5)
                    x = offset_x + col_index * (BLOCK_WIDTH + BLOCK_SPACES)
                    y = 50 + row_index * (BLOCK_HEIGHT + BLOCK_SPACES)
                    block = Block(self.canvas, x, y, color, hits )
                    blocks.append(block)

        return blocks

