# WumpusWorldGame/environment.py

import random
from config import Config

class WumpusEnvironment:
    def __init__(self, config: Config):
        self.config = config
        self.grid_size = config.GRID_SIZE
        self.grid = self._initialize_grid()
        self.wumpus_alive = True
        self.gold_collected = False

    def _initialize_grid(self):
        grid = {}
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                grid[(r, c)] = [] # Each cell can contain multiple items/percepts

        # Place Wumpus, Pits, Gold ensuring no overlap and not at (0,0)
        possible_locations = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size) if (r, c) != self.config.AGENT_START]
        random.shuffle(possible_locations)

        # Place Wumpus
        wumpus_pos = possible_locations.pop(0)
        grid[wumpus_pos].append("Wumpus")
        self.wumpus_location = wumpus_pos
        self._add_stench_percepts(wumpus_pos, grid)

        # Place Gold
        gold_pos = possible_locations.pop(0)
        grid[gold_pos].append("Gold")
        self.gold_location = gold_pos
        grid[gold_pos].append(self.config.GLITTER) # Glitter at gold location

        # Place Pits
        for _ in range(self.config.NUM_PITS):
            if not possible_locations:
                print("Warning: Not enough unique locations for all pits.")
                break
            pit_pos = possible_locations.pop(0)
            grid[pit_pos].append("Pit")
            self._add_breeze_percepts(pit_pos, grid)

        return grid

    def _add_stench_percepts(self, pos, grid):
        r, c = pos
        # Neighbors (up, down, left, right)
        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        for nr, nc in neighbors:
            if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                if self.config.STENCH not in grid[(nr, nc)]:
                    grid[(nr, nc)].append(self.config.STENCH)

    def _add_breeze_percepts(self, pos, grid):
        r, c = pos
        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        for nr, nc in neighbors:
            if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                if self.config.BREEZE not in grid[(nr, nc)]:
                    grid[(nr, nc)].append(self.config.BREEZE)

    def get_percepts_at_location(self, row, col):
        if (row, col) in self.grid:
            percepts = []
            for item in self.grid[(row, col)]:
                if item in [self.config.BREEZE, self.config.STENCH, self.config.GLITTER]:
                    percepts.append(item)
            return percepts
        return []

    def has_wumpus(self, row, col):
        return "Wumpus" in self.grid.get((row, col), []) and self.wumpus_alive

    def has_pit(self, row, col):
        return "Pit" in self.grid.get((row, col), [])

    def has_gold(self, row, col):
        return "Gold" in self.grid.get((row, col), []) and not self.gold_collected

    def remove_gold(self, row, col):
        if "Gold" in self.grid.get((row, col), []):
            self.grid[(row, col)].remove("Gold")
            if self.config.GLITTER in self.grid.get((row,col), []):
                self.grid[(row,col)].remove(self.config.GLITTER)
            self.gold_collected = True

    def kill_wumpus(self):
        self.wumpus_alive = False
        # Remove Stench from all cells when Wumpus is dead
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.config.STENCH in self.grid[(r, c)]:
                    self.grid[(r, c)].remove(self.config.STENCH)

    def is_valid_location(self, row, col):
        return 0 <= row < self.grid_size and 0 <= col < self.grid_size