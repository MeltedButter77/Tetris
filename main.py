import random
import pygame
import sys


class Piece:
    def __init__(self, game, p_type="z", colour="red"):
        self.game = game
        self.origin = [0, 0]
        self.colour = colour
        self.type = p_type

        # Each list of offsets should have the same amount of tuples
        self.offsets = []
        self.offset_num = 0
        if self.type.upper() == "I":
            self.offsets = [
                [(0, 1), (1, 1), (2, 1), (3, 1)],
                [(2, 0), (2, 1), (2, 2), (2, 3)],
                [(0, 2), (1, 2), (2, 2), (3, 2)],
                [(1, 0), (1, 1), (1, 2), (1, 3)]
            ]
        elif self.type.upper() == "O":
            self.offsets = [
                [(1, 1), (1, 2), (2, 1), (2, 2)],
                [(1, 1), (1, 2), (2, 1), (2, 2)],
                [(1, 1), (1, 2), (2, 1), (2, 2)],
                [(1, 1), (1, 2), (2, 1), (2, 2)]
            ]
        elif self.type.upper() == "T":
            self.offsets = [
                [(1, 0), (0, 1), (1, 1), (2, 1)],
                [(1, 0), (1, 1), (2, 1), (1, 2)],
                [(0, 1), (1, 1), (2, 1), (1, 2)],
                [(1, 0), (0, 1), (1, 1), (1, 2)]
            ]
        elif self.type.upper() == "J":
            self.offsets = [
                [(1, 0), (1, 1), (1, 2), (0, 2)],
                [(0, 1), (1, 1), (2, 1), (2, 0)],
                [(1, 0), (1, 1), (1, 2), (2, 2)],
                [(0, 1), (1, 1), (2, 1), (0, 2)]
            ]
        elif self.type.upper() == "L":
            self.offsets = [
                [(1, 0), (1, 1), (1, 2), (2, 2)],
                [(0, 1), (1, 1), (2, 1), (0, 0)],
                [(0, 0), (1, 0), (1, 1), (1, 2)],
                [(0, 1), (1, 1), (2, 1), (2, 2)]
            ]
        elif self.type.upper() == "S":
            self.offsets = [
                [(1, 0), (2, 0), (0, 1), (1, 1)],  # Original position
                [(0, 0), (0, 1), (1, 1), (1, 2)],  # Rotated 90 degrees clockwise
                [(1, 1), (2, 1), (0, 0), (1, 0)],  # Rotated 180 degrees clockwise
                [(1, 0), (1, 1), (2, 1), (2, 2)]  # Rotated 270 degrees clockwise
            ]
        elif self.type.upper() == "Z":
            self.offsets = [
                [(0, 0), (1, 0), (1, 1), (2, 1)],  # Original position
                [(1, 0), (1, 1), (0, 1), (0, 2)],  # Rotated 90 degrees clockwise
                [(2, 1), (1, 1), (1, 0), (0, 0)],  # Rotated 180 degrees clockwise
                [(0, 2), (0, 1), (1, 1), (1, 0)]  # Rotated 270 degrees clockwise
            ]

    def render(self):
        for offset in self.offsets[self.offset_num]:
            pygame.draw.rect(self.game.screen, self.colour, pygame.Rect(
                self.origin[0] * self.game.grid_size + offset[0] * self.game.grid_size + self.game.game_location[0],
                self.origin[1] * self.game.grid_size + offset[1] * self.game.grid_size + self.game.game_location[1],
                self.game.grid_size,
                self.game.grid_size
            ))

    def update_board(self):
        blocks = []
        for offset in self.offsets[self.offset_num]:
            block = {
                "location": (offset[0] + self.origin[0], offset[1] + self.origin[1]),
                "colour": self.colour
            }
            blocks.append(block)
            if block["location"][1] <= 0:
                self.game.game_over()

        self.game.board.extend(blocks)

    def update_blocks(self, direction=None):
        # returns True if a collision is made

        blocks = []
        for offset in self.offsets[self.offset_num]:
            blocks.append({
                "location": (offset[0] + self.origin[0], offset[1] + self.origin[1]),
                "colour": self.colour
            })

        board_locations = []
        for block in self.game.board:
            board_locations.append(block["location"])

        for block in blocks:
            if block["location"][1] >= self.game.game_area[1]:
                return True
            if block["location"][0] >= self.game.game_area[0] or block["location"][0] < 0:
                return True
            if block["location"] in board_locations:
                return True

    def move(self, direction):
        origin = self.origin.copy()
        if direction == "down":
            self.origin[1] += 1
        elif direction == "left":
            self.origin[0] -= 1
        elif direction == "right":
            self.origin[0] += 1
        # if collision is made, rollback changes and update the rects back to rollback state
        if self.update_blocks(direction):
            self.origin = origin
            self.update_blocks()
            if direction == "down":
                self.update_board()

                # handle collision
                self.game.pieces.remove(self.game.pieces[0])
                b_type = random.choice(self.game.types).upper()
                colour = self.game.colours[b_type]
                self.game.pieces.insert(0, Piece(self.game, b_type, colour))
                return True


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

        self.app_state = "menu"
        self.menu_buttons = [
            {"rect": pygame.Rect(200, 200, 100, 50), "text": "Play", "action": "game", "colour": "green"},
            {"rect": pygame.Rect(300, 200, 100, 50), "text": "Quit", "action": "quit", "colour": "red"}
        ]

        self.fps = 60
        self.types = ["I", "o", "t", "j", "l", "s", "z"]
        self.colours = {
            'I': (0, 255, 255),  # Cyan
            'O': (255, 255, 0),  # Yellow
            'T': (128, 0, 128),  # Purple
            'J': (0, 0, 255),  # Blue
            'L': (255, 165, 0),  # Orange
            'S': (0, 255, 0),  # Green
            'Z': (255, 0, 0)  # Red
        }
        self.images = {
            (0, 255, 255): pygame.image.load("cyan.png"),
            (255, 255, 0): pygame.image.load("yellow.png"),
            (128, 0, 128): pygame.image.load("purple.png"),
            (0, 0, 255): pygame.image.load("blue.png"),
            (255, 165, 0): pygame.image.load("orange.png"),
            (0, 255, 0): pygame.image.load("green.png"),
            (255, 0, 0): pygame.image.load("red.png")
        }

        self.grid_size = 20
        self.game_location = (220, 40)
        self.game_area = (10, 20)

        self.pieces = [
            Piece(self, "l", "blue"),
        ]

        # Reset variables
        self.board = []
        self.score = 0
        self.move_down_delay = 30

        self.USEREVENT = 1
        pygame.time.set_timer(self.USEREVENT, 250)

    def game_over(self):
        self.app_state = "game_over"
        self.menu_buttons = [
            {"rect": pygame.Rect(200, 200, 100, 50), "text": "Play Again", "action": "game", "colour": "green"},
            {"rect": pygame.Rect(300, 200, 100, 50), "text": "Quit", "action": "quit", "colour": "red"}
        ]

    def handle_game_input(self, event=None, keys_pressed=None):
        if keys_pressed:
            if keys_pressed[pygame.K_s]:
                if self.move_down_delay > 0:
                    self.move_down_delay -= 1
                else:
                    self.move_down_delay = 5
                    self.pieces[0].move("down")
            else:
                self.move_down_delay = 0

        if not event:  # filter for no event
            return
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        direction = None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                while not self.pieces[0].move("down"):
                    pass
            if event.key == pygame.K_d:
                self.pieces[0].move("right")
            if event.key == pygame.K_a:
                self.pieces[0].move("left")
            if event.key == pygame.K_w:
                self.pieces[0].offset_num = (self.pieces[0].offset_num + 1) % len(self.pieces[0].offsets)
        if event.type == self.USEREVENT and not keys_pressed[pygame.K_s]:
            self.pieces[0].move("down")

        # Check for full row
        rows = []
        for i in range(self.game_area[1]):
            rows.append(0)

        for block in self.board:
            for i in range(len(rows)):
                if block["location"][1] == i:
                    rows[i] += 1
                    if rows[i] >= self.game_area[0]:
                        self.board = [block for block in self.board if block["location"][1] != i]
                        for block in self.board:
                            if block["location"][1] < i:
                                block["location"] = (block["location"][0], block["location"][1] + 1)

    def render_game(self):
        # draw game area in game location
        pygame.draw.rect(self.screen, "black", (
            self.game_location[0],
            self.game_location[1],
            self.game_area[0] * self.grid_size,
            self.game_area[1] * self.grid_size
        ))
        for piece in self.pieces:
            piece.render()

        for block in self.board:
            pygame.draw.rect(self.screen, block["colour"], pygame.Rect(
                block["location"][0] * self.grid_size + self.game_location[0],
                block["location"][1] * self.grid_size + self.game_location[1],
                self.grid_size,
                self.grid_size
            ))

    def handle_menu_input(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.menu_buttons:
                if button["rect"].collidepoint(event.pos):
                    if button["action"] == "quit":
                        pygame.quit()
                        sys.exit()
                    if button["action"] == "game":
                        self.board = []
                        self.score = 0
                    self.app_state = button["action"]

    def render_menu(self):
        for button in self.menu_buttons:
            image = self.images[button["colour"]].scale((button["rect"].width, button["rect"].height))
            self.screen.blit(image, button["rect"].topleft)

            text = self.font.render(button["text"], True, "white")
            self.screen.blit(text, (button["rect"].x + 10, button["rect"].y + 10))

    def start(self):
        while True:
            while self.app_state == "menu":
                for event in pygame.event.get():
                    self.handle_menu_input(event=event)
                # Render
                self.screen.fill("white")
                self.render_menu()
                pygame.display.update()

            while self.app_state == "game_over":
                for event in pygame.event.get():
                    self.handle_menu_input(event=event)
                # Render
                self.screen.fill("white")
                self.render_game()
                self.render_menu()
                pygame.display.update()

            while self.app_state == "game":
                for event in pygame.event.get():
                    self.handle_game_input(event=event, keys_pressed=pygame.key.get_pressed())
                self.handle_game_input(keys_pressed=pygame.key.get_pressed())
                # Render
                self.screen.fill("white")
                self.render_game()
                pygame.display.update()

            self.clock.tick(self.fps)


Game().start()
