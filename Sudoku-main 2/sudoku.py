import pygame
from pygame.locals import *
import sys
import sudoku_dfs
import Sudoku_matrix_9x9
import numpy as np


class Sudoku():
    def __init__(self):
        pygame.init()
        # Create the canvas
        self.surface = pygame.display.set_mode((650, 450))
        pygame.display.set_caption("Sudoku Game")
        self.font = pygame.font.Font(None, 40)
        # Set background color white
        color = (255, 255, 255)
        self.surface.fill(color)

        self.isBox = True                   # Check if it is a input number box
        self.has_no_number = False          # Check if this box has no number in it
        self.position = -1                  # Record input position

        # For each input box
        # Tuple of (value, is_original)
        self.box = np.zeros((9, 9), dtype=[('value', int), ('is_original', bool)])

        # Each box is a button for user to input number
        self.buttons = []
        for i in range(9):
            for j in range(9):
                self.buttons.append(pygame.Rect(j * 50, i * 50, 49, 49))

        # Generate and store board and puzzle
        self.board = np.zeros((9, 9), dtype=int)
        self.puzzle = np.zeros((9, 9), dtype=int)
        self.generate()

    def generate(self):
        """Generate completed board and solvable sudoku puzzle"""
        sudoku_dic = Sudoku_matrix_9x9.sudoku_init(9)
        self.board = sudoku_dfs.sudoku_solver_help(sudoku_dic)
        print("\nBoard: ")
        sudoku_dfs.print_grid(self.board)
        self.puzzle = sudoku_dfs.generate_puzzle(self.board, 0.8)
        print("\nPuzzle: ")
        sudoku_dfs.print_grid(self.puzzle)

        # Initialize original numbers
        self.box['value'] = self.puzzle
        self.box['is_original'] = self.puzzle != 0

    def show_message(self, message):
        # Clear the existing label by fill the screen with white
        self.surface.fill(pygame.Color("white"))
        # Label new message
        message_font = pygame.font.Font(None, 15)
        text = message_font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(550, 260))

        self.surface.blit(text, text_rect)
        pygame.display.update()

    def display(self):
        """Display the Sudoku puzzle on the canvas"""
        self.draw()
        # Keep updating for events happened
        pygame.display.update()
        while True:
            self.handle_event(self.board)
            self.draw()
            pygame.display.update()

    def draw(self):
        """Draw numbers and boxes on canvas"""
        original_color = (176, 196, 222)  # Blue for original numbers
        user_color = (220, 220, 220)  # Grey for user-inputted numbers

        for i in range(len(self.puzzle)):
            for j in range(len(self.puzzle[0])):
                # Draw box for each position
                # Different Color for
                box_color = original_color if self.box['is_original'][i][j] else user_color
                pygame.draw.rect(self.surface, box_color, self.buttons[j + i * 9])

                if self.box['value'][i][j] != 0:
                    # Draw numbers
                    # color = original_color if self.box[i + j * 9][1] else user_color
                    self.surface.blit(self.font.render(str(self.box['value'][i][j]), True, (0, 0, 0)),
                                      (15 + j * 50, 15 + i * 50))
        # Draw Button
        # "Check" Button
        pygame.draw.rect(self.surface, (220, 220, 220), pygame.Rect(480, 50, 130, 50), 0, 15)
        self.surface.blit(self.font.render("Check", True, (0, 0, 0)), (500, 60))

        # "New" Button
        pygame.draw.rect(self.surface, (220, 220, 220), pygame.Rect(480, 120, 130, 50), 0, 15)
        self.surface.blit(self.font.render("New", True, (0, 0, 0)), (510, 133))

        # "Clear" button
        pygame.draw.rect(self.surface, (220, 220, 220), pygame.Rect(480, 190, 130, 50), 0, 15)
        self.surface.blit(self.font.render("Clear", True, (0, 0, 0)), (505, 203))

        pygame.display.update()

    def check_solution(self, solution):
        """Check if the current puzzle matches the solution"""
        user_solution = self.box['value']
        return np.array_equal(user_solution, solution)

    def handle_event(self, board):
        """Event handling"""
        # Check for every event happened
        for event in pygame.event.get():
            # If the user close the window, quit
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # Check the event happen is not the input boxes
            if self.isBox:
                # Case 1: that where the event happen is the input boxe
                if event.type == KEYDOWN and self.has_no_number:
                    self.handle_input(event)
                    self.position = -1
                    self.has_no_number = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[0] <= 450 and event.pos[1] <= 450:
                        self.position = event.pos[1] // 50, event.pos[0] // 50
                        self.has_no_number = True
                    else:
                        self.isBox = False
                        self.draw()
            else:
                # Case 2: that where the event happen is not the input boxe
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # "Check" Button
                    if 480 <= event.pos[0] <= 630 and 50 <= event.pos[1] <= 120:
                        if self.check_solution(board):
                            # Show a message box of the success
                            self.show_message("Congratulations! You solved it!")
                        else:
                            # Show a message box of the failure
                            self.show_message("Incorrect! Click \"Clear\" to retry!")
                    # "New" Button
                    elif 480 <= event.pos[0] <= 620 and 120 <= event.pos[1] <= 180:
                        self.box['value'] = np.zeros((9, 9), dtype=int)
                        self.box['is_original'] = np.zeros((9, 9), dtype=bool)
                        self.board = np.zeros((9, 9), dtype=int)
                        self.puzzle = np.zeros((9, 9), dtype=int)
                        self.isBox = True
                        # Regenerate new problem
                        self.generate()
                        # Clear the label
                        self.show_message("")
                        pygame.display.update()
                        # Update and display new puzzle
                        self.display()
                    # "Clear" Button
                    elif 480 <= event.pos[0] <= 620 and 180 <= event.pos[1] <= 240:
                        # Clear the board, but keep the original puzzle
                        self.box['value'] = np.where(self.box['is_original'], self.box['value'], 0)
                        self.isBox = True
                        # Clear the label
                        self.show_message("")
                        pygame.display.update()
                        # self.draw()
                        self.display()

    def handle_input(self, event):
        """Get keyboard input"""
        if pygame.key.name(event.key).isdigit():
            self.box['value'][self.position] = int(pygame.key.name(event.key))
        else:
            self.box['value'][self.position] = 0


sudoku = Sudoku()
sudoku.display()