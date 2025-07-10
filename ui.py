# WumpusWorldGame/ui.py

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk # Requires Pillow: pip install Pillow
import os

class WumpusGUI(tk.Frame):
    def __init__(self, master, game_logic, config, initial_env_grid):
        super().__init__(master)
        self.game_logic = game_logic
        self.config = config
        self.master = master

        self.grid_size = self.config.GRID_SIZE
        self.cell_size = 80 # Size of each cell in pixels

        self.images = self._load_images()
        self.canvas = tk.Canvas(self, width=self.grid_size * self.cell_size,
                                height=self.grid_size * self.cell_size,
                                bg="white", borderwidth=2, relief="groove")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        self.info_frame = tk.Frame(self, width=250, height=self.grid_size * self.cell_size,
                                   bg="#F0F0F0", borderwidth=2, relief="solid")
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        self.info_frame.pack_propagate(False) # Prevent frame from shrinking to fit content

        self.controls_frame = tk.Frame(self.info_frame, pady=10)
        self.controls_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self._create_info_widgets()
        self._create_control_buttons()

        self.draw_grid_lines()
        self.update_grid(self.game_logic.agent.known_grid) # Initial draw

    def _load_images(self):
        images = {}
        script_dir = os.path.dirname(__file__)
        assets_path = os.path.join(script_dir, "assets")

        try:
            images["agent"] = ImageTk.PhotoImage(Image.open(os.path.join(assets_path, "agent.png")).resize((self.cell_size - 10, self.cell_size - 10)))
            images["gold"] = ImageTk.PhotoImage(Image.open(os.path.join(assets_path, "gold.png")).resize((self.cell_size - 20, self.cell_size - 20)))
            images["wumpus"] = ImageTk.PhotoImage(Image.open(os.path.join(assets_path, "wumpus.png")).resize((self.cell_size - 10, self.cell_size - 10)))
            images["pit"] = ImageTk.PhotoImage(Image.open(os.path.join(assets_path, "pit.png")).resize((self.cell_size - 10, self.cell_size - 10)))
            images["breeze"] = ImageTk.PhotoImage(Image.open(os.path.join(assets_path, "breeze.png")).resize((self.cell_size // 3, self.cell_size // 3)))
            images["stench"] = ImageTk.PhotoImage(Image.open(os.path.join(assets_path, "stench.png")).resize((self.cell_size // 3, self.cell_size // 3)))
            images["glitter"] = ImageTk.PhotoImage(Image.open(os.path.join(assets_path, "glitter.png")).resize((self.cell_size // 3, self.cell_size // 3)))
        except FileNotFoundError as e:
            messagebox.showerror("Image Load Error", f"Could not load image: {e}\nPlease ensure 'assets' folder is in the same directory as 'ui.py'")
            # Create dummy images if not found, to prevent crash
            images["agent"] = tk.PhotoImage(width=1, height=1)
            images["gold"] = tk.PhotoImage(width=1, height=1)
            images["wumpus"] = tk.PhotoImage(width=1, height=1)
            images["pit"] = tk.PhotoImage(width=1, height=1)
            images["breeze"] = tk.PhotoImage(width=1, height=1)
            images["stench"] = tk.PhotoImage(width=1, height=1)
            images["glitter"] = tk.PhotoImage(width=1, height=1)
        return images

    def _create_info_widgets(self):
        tk.Label(self.info_frame, text="Game Status", font=("Arial", 14, "bold"), bg="#F0F0F0").pack(pady=10)
        self.status_label = tk.Label(self.info_frame, text=f"Status: {self.config.GAME_RUNNING}", bg="#F0F0F0", font=("Arial", 10))
        self.status_label.pack(anchor='w', padx=10, pady=2)

        self.score_label = tk.Label(self.info_frame, text=f"Score: {self.game_logic.agent.score}", bg="#F0F0F0", font=("Arial", 10))
        self.score_label.pack(anchor='w', padx=10, pady=2)

        self.arrows_label = tk.Label(self.info_frame, text=f"Arrows: {'Yes' if self.game_logic.agent.has_arrow else 'No'}", bg="#F0F0F0", font=("Arial", 10))
        self.arrows_label.pack(anchor='w', padx=10, pady=2)

        self.gold_label = tk.Label(self.info_frame, text=f"Gold: {'Yes' if self.game_logic.agent.has_gold else 'No'}", bg="#F0F0F0", font=("Arial", 10))
        self.gold_label.pack(anchor='w', padx=10, pady=2)

        tk.Label(self.info_frame, text="Percepts:", font=("Arial", 12, "bold"), bg="#F0F0F0").pack(pady=5, anchor='w', padx=10)
        self.percepts_display = tk.Label(self.info_frame, text="", wraplength=200, justify='left', bg="#F0F0F0", font=("Arial", 9))
        self.percepts_display.pack(anchor='w', padx=10, pady=2)

    def _create_control_buttons(self):
        button_font = ("Arial", 10)
        padding = 5

        move_frame = tk.Frame(self.controls_frame)
        move_frame.pack(pady=padding)
        tk.Button(move_frame, text="Up", command=lambda: self._perform_action("move", "up"), font=button_font, width=8).grid(row=0, column=1, padx=2, pady=2)
        tk.Button(move_frame, text="Left", command=lambda: self._perform_action("move", "left"), font=button_font, width=8).grid(row=1, column=0, padx=2, pady=2)
        tk.Button(move_frame, text="Right", command=lambda: self._perform_action("move", "right"), font=button_font, width=8).grid(row=1, column=2, padx=2, pady=2)
        tk.Button(move_frame, text="Down", command=lambda: self._perform_action("move", "down"), font=button_font, width=8).grid(row=2, column=1, padx=2, pady=2)

        action_frame = tk.Frame(self.controls_frame)
        action_frame.pack(pady=padding)
        tk.Button(action_frame, text="Shoot", command=lambda: self._perform_action("shoot"), font=button_font, width=10).pack(side=tk.LEFT, padx=5, pady=2)
        tk.Button(action_frame, text="Grab Gold", command=lambda: self._perform_action("grab"), font=button_font, width=10).pack(side=tk.LEFT, padx=5, pady=2)
        tk.Button(action_frame, text="Climb Out", command=lambda: self._perform_action("climb"), font=button_font, width=10).pack(side=tk.LEFT, padx=5, pady=2)

        game_control_frame = tk.Frame(self.controls_frame)
        game_control_frame.pack(pady=padding)
        tk.Button(game_control_frame, text="Reset Game", command=self._reset_game, font=button_font, bg="red", fg="white", width=12).pack(side=tk.LEFT, padx=5, pady=5)


    def draw_grid_lines(self):
        for i in range(self.grid_size + 1):
            x = i * self.cell_size
            y = i * self.cell_size
            self.canvas.create_line(x, 0, x, self.grid_size * self.cell_size, fill="gray")
            self.canvas.create_line(0, y, self.grid_size * self.cell_size, y, fill="gray")

    def update_grid(self, known_grid):
        self.canvas.delete("all_cells") # Clear previous cell content

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size

                cell_status = known_grid[(r, c)]["status"]
                is_visited = known_grid[(r, c)]["visited"]
                percepts_at_cell = known_grid[(r, c)]["percepts"]

                fill_color = self.config.COLOR_UNKNOWN
                if is_visited:
                    fill_color = self.config.COLOR_KNOWN
                    if cell_status == "Safe":
                        fill_color = self.config.COLOR_SAFE
                    elif "Breeze" in percepts_at_cell or "Stench" in percepts_at_cell:
                        fill_color = self.config.COLOR_DANGER # Indicate perceived danger
                elif cell_status == "Pit?":
                    fill_color = self.config.COLOR_PIT_PERCEIVED
                elif cell_status == "Wumpus?":
                    fill_color = self.config.COLOR_WUMPUS_PERCEIVED

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="gray", tags="all_cells")

                # Add percepts and known entities if cell is visited
                if is_visited:
                    # Display percept icons
                    icon_offset_x = 5
                    icon_offset_y = 5
                    if self.config.BREEZE in percepts_at_cell:
                        self.canvas.create_image(x1 + icon_offset_x, y1 + icon_offset_y, anchor='nw', image=self.images["breeze"], tags="all_cells")
                        icon_offset_x += self.cell_size // 3 + 5
                    if self.config.STENCH in percepts_at_cell:
                        self.canvas.create_image(x1 + icon_offset_x, y1 + icon_offset_y, anchor='nw', image=self.images["stench"], tags="all_cells")
                        icon_offset_x += self.cell_size // 3 + 5
                    if self.config.GLITTER in percepts_at_cell:
                        self.canvas.create_image(x1 + icon_offset_x, y1 + icon_offset_y, anchor='nw', image=self.images["glitter"], tags="all_cells")


                    # Display known entities
                    if "Wumpus" in percepts_at_cell: # This would only be known if Wumpus is in visited square
                         self.canvas.create_image(x1 + self.cell_size // 2, y1 + self.cell_size // 2, anchor='center', image=self.images["wumpus"], tags="all_cells")
                    if "Pit" in percepts_at_cell:
                        self.canvas.create_image(x1 + self.cell_size // 2, y1 + self.cell_size // 2, anchor='center', image=self.images["pit"], tags="all_cells")
                    if "Gold" in percepts_at_cell and not self.game_logic.environment.gold_collected:
                        self.canvas.create_image(x1 + self.cell_size // 2, y1 + self.cell_size // 2, anchor='center', image=self.images["gold"], tags="all_cells")

                # Always draw agent at its current position
                if (r, c) == (self.game_logic.agent.row, self.game_logic.agent.col):
                    self.canvas.create_image(x1 + self.cell_size // 2, y1 + self.cell_size // 2, anchor='center', image=self.images["agent"], tags="all_cells")

        self.canvas.tag_raise("agent") # Ensure agent is always on top

    def update_percepts_display(self, percepts):
        percept_text = "Current Percepts: "
        if not percepts:
            percept_text += "None"
        else:
            percept_text += ", ".join(percepts)
        self.percepts_display.config(text=percept_text)

    def update_score(self, score):
        self.score_label.config(text=f"Score: {score}")

    def update_arrows(self, has_arrow):
        self.arrows_label.config(text=f"Arrows: {'Yes' if has_arrow else 'No'}")

    def update_gold(self, has_gold):
        self.gold_label.config(text=f"Gold: {'Yes' if has_gold else 'No'}")

    def update_status(self, status_message):
        self.status_label.config(text=f"Status: {status_message}")

    def _perform_action(self, action_type, direction=None):
        if self.game_logic.game_state != self.config.GAME_RUNNING:
            messagebox.showinfo("Game Over", "The game is over. Please reset to play again.")
            return

        result_message = ""
        game_over = False

        if action_type == "move":
            game_over, result_message = self.game_logic.move_agent(direction)
        elif action_type == "shoot":
            game_over, result_message = self.game_logic.shoot_arrow()
        elif action_type == "grab":
            game_over, result_message = self.game_logic.grab_gold()
        elif action_type == "climb":
            game_over, result_message = self.game_logic.climb_out()

        # Update UI after action
        self.game_logic.perceive_current_location() # Agent perceives new location
        self.game_logic.agent.infer_from_percepts() # Agent updates its knowledge
        self.update_grid(self.game_logic.agent.known_grid)
        self.update_percepts_display(self.game_logic.agent.percepts)
        self.update_score(self.game_logic.agent.score)
        self.update_arrows(self.game_logic.agent.has_arrow)
        self.update_gold(self.game_logic.agent.has_gold)
        self.update_status(self.game_logic.game_state) # Update game state display

        if result_message:
            messagebox.showinfo("Action Result", result_message)

        if game_over:
            if self.game_logic.game_state == self.config.GAME_OVER_WON:
                messagebox.showinfo("Game Won!", f"Congratulations! You won with a score of {self.game_logic.agent.score}!")
            elif self.game_logic.game_state == self.config.GAME_OVER_LOST:
                messagebox.showerror("Game Over!", f"You lost! Final score: {self.game_logic.agent.score}")
            # Optionally disable buttons or prompt for reset

    def _reset_game(self):
        # This will trigger the main application to re-initialize the game
        self.master.winfo_toplevel().destroy() # Close current window
        import main # Re-import main to re-run the startup
        root = tk.Tk()
        app = main.WumpusGameApp(root)
        root.mainloop()