import tkinter as tk
import random

class SnakeAndLadder:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake and Ladder Game")
        
        # Initialize player positions
        self.player1_position = 1
        self.player2_position = 1
        self.current_player = 1
        
        # Define snakes and ladders
        self.snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        self.ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}
        
        # Create canvas for the board
        self.canvas = tk.Canvas(master, width=600, height=600, bg="white")
        self.canvas.pack()
        
        # Draw the board
        self.draw_board()
        
        # Create labels and buttons
        self.label = tk.Label(master, text="Player 1's turn", font=("Arial", 16))
        self.label.pack()
        
        self.roll_button = tk.Button(master, text="Roll Dice", command=self.roll_dice, font=("Arial", 16))
        self.roll_button.pack()
        
        self.reset_button = tk.Button(master, text="Reset Game", command=self.reset_game, font=("Arial", 16))
        self.reset_button.pack()
        
        self.result_label = tk.Label(master, text="", font=("Arial", 16))
        self.result_label.pack()

        # Create player markers
        self.player1_marker = self.canvas.create_oval(10, 550, 50, 590, fill="blue")  # Player 1 marker
        self.player2_marker = self.canvas.create_oval(10, 550, 50, 590, fill="red")   # Player 2 marker

    def draw_board(self):
        # Draw the squares on the board
        for i in range(10):
            for j in range(10):
                x1 = j * 60
                y1 = 600 - (i * 60)
                x2 = x1 + 60
                y2 = y1 - 60
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="lightblue")
                # Label the squares with numbers from 1 to 100
                square_number = (i * 10 + j + 1)
                self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(square_number), font=("Arial", 12))

        # Draw snakes
        for start, end in self.snakes.items():
            self.draw_snake(start, end)

        # Draw ladders
        for start, end in self.ladders.items():
            self.draw_ladder(start, end)

    def draw_snake(self, start, end):
        start_x, start_y = self.get_coordinates(start)
        end_x, end_y = self.get_coordinates(end)
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill="red", width=5)

    def draw_ladder(self, start, end):
        start_x, start_y = self.get_coordinates(start)
        end_x, end_y = self.get_coordinates(end)
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill="green", width=5)

    def get_coordinates(self, position):
        # Calculate the coordinates of the square based on the position
        row = (position - 1) // 10
        col = (position - 1) % 10
        x = col * 60 + 30
        y = 600 - (row * 60 + 30)
        return x, y

    def roll_dice(self):
        dice_value = random.randint(1, 6)
        if self.current_player == 1:
            self.player1_position += dice_value
            if self.player1_position > 100:
                self.player1_position -= dice_value  # Don't move if over 100
            self.player1_position = self.check_snakes_and_ladders(self.player1_position)
            self.label.config(text=f"Player 1 rolled a {dice_value}. Player 1 is on {self.player1_position}.")
            self.move_player(self.player1_marker, self.player1_position)
            if self.player1_position == 100:
                self.result_label.config(text="Player 1 wins!")
                self.roll_button.config(state="disabled")
            self.current_player = 2
        else:
            self.player2_position += dice_value
            if self.player2_position > 100:
                self.player2_position -= dice_value  # Don't move if over 100
            self.player2_position = self.check_snakes_and_ladders(self.player2_position)
            self.label.config(text=f"Player 2 rolled a {dice_value}. Player 2 is on {self.player2_position}.")
            self.move_player(self.player2_marker, self.player2_position)
            if self.player2_position == 100:
                self.result_label.config(text="Player 2 wins!")
                self.roll_button.config(state="disabled")
            self.current_player = 1

    def move_player(self, marker, position):
        x, y = self.get_coordinates(position)
        self.canvas.coords(marker, x - 20, y - 20, x + 20, y + 20)  # Move the player marker

    def check_snakes_and_ladders(self, position):
        if position in self.snakes:
            position = self.snakes[position]
            self.label.config(text=f"Player {self.current_player} encountered a snake! Moving down to {position}.")
        elif position in self.ladders:
            position = self.ladders[position]
            self.label.config(text=f"Player {self.current_player} climbed a ladder! Moving up to {position}.")
        return position

    def reset_game(self):
        self.player1_position = 1
        self.player2_position = 1
        self.current_player = 1
        self.label.config(text="Player 1's turn")
        self.result_label.config(text="")
        self.roll_button.config(state="normal")
        self.canvas.delete("all")  # Clear the canvas
        self.draw_board()  # Redraw the board
        # Reset player markers
        self.canvas.coords(self.player1_marker, 10, 550, 50, 590)
        self.canvas.coords(self.player2_marker, 10, 550, 50, 590)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeAndLadder(root)
    root.mainloop()