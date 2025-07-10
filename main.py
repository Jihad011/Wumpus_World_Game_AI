# WumpusWorldGame/main.py

import tkinter as tk
from config import Config
from environment import WumpusEnvironment
from agent import WumpusAgent
from ui import WumpusGUI
from logic import GameLogic

class WumpusGameApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Wumpus World Game")
        self.master.geometry("1000x800") # Initial window size

        self.config = Config()
        self.environment = None
        self.agent = None
        self.game_logic = None
        self.gui = None

        self.setup_initial_config_ui()

    def setup_initial_config_ui(self):
        # Clear any existing widgets
        for widget in self.master.winfo_children():
            widget.destroy()

        config_frame = tk.Frame(self.master, padx=20, pady=20)
        config_frame.pack(expand=True)

        tk.Label(config_frame, text="Wumpus World Configuration", font=("Arial", 16, "bold")).pack(pady=10)

        # Grid Size
        tk.Label(config_frame, text="Grid Size (N x N):").pack(anchor='w', pady=5)
        self.grid_size_entry = tk.Entry(config_frame)
        self.grid_size_entry.insert(0, str(self.config.GRID_SIZE))
        self.grid_size_entry.pack(fill='x', pady=2)

        # Number of Pits
        tk.Label(config_frame, text="Number of Pits:").pack(anchor='w', pady=5)
        self.num_pits_entry = tk.Entry(config_frame)
        self.num_pits_entry.insert(0, str(self.config.NUM_PITS))
        self.num_pits_entry.pack(fill='x', pady=2)

        # Allow Wumpus/Gold to be placed dynamically (optional, could be fixed)
        # For simplicity, let's keep them fixed in initial setup but configurable

        start_button = tk.Button(config_frame, text="Start Game", command=self.start_game, font=("Arial", 12))
        start_button.pack(pady=20)

    def start_game(self):
        try:
            new_grid_size = int(self.grid_size_entry.get())
            new_num_pits = int(self.num_pits_entry.get())

            if new_grid_size < 4 or new_grid_size > 10: # Example constraints
                raise ValueError("Grid size must be between 4 and 10.")
            if new_num_pits < 0 or new_num_pits >= new_grid_size * new_grid_size - 2: # Min 2 spots for agent/gold
                raise ValueError("Invalid number of pits.")

            self.config.GRID_SIZE = new_grid_size
            self.config.NUM_PITS = new_num_pits

            # Initialize game components with new configuration
            self.environment = WumpusEnvironment(self.config)
            self.agent = WumpusAgent(self.config)
            self.game_logic = GameLogic(self.environment, self.agent, self.config)

            # Clear initial config UI and set up game UI
            for widget in self.master.winfo_children():
                widget.destroy()

            self.gui = WumpusGUI(self.master, self.game_logic, self.config, self.environment.grid)
            self.gui.pack(expand=True, fill='both')

            # Initial update of the UI based on agent's starting perceptions
            self.game_logic.perceive_current_location()
            self.gui.update_grid(self.game_logic.agent.known_grid)
            self.gui.update_percepts_display(self.game_logic.agent.percepts)
            self.gui.update_score(self.game_logic.agent.score)

        except ValueError as e:
            tk.messagebox.showerror("Configuration Error", str(e))
        except Exception as e:
            tk.messagebox.showerror("Game Initialization Error", f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = WumpusGameApp(root)
    root.mainloop()