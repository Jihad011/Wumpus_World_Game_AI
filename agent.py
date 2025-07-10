# WumpusWorldGame/agent.py

from config import Config
from knowledgebase import KnowledgeBase # Assuming a KB for advanced reasoning

class WumpusAgent:
    def __init__(self, config: Config):
        self.config = config
        self.row, self.col = config.AGENT_START
        self.direction = "right" # Initial direction: right, up, left, down
        self.has_gold = False
        self.has_arrow = True
        self.score = 0
        self.percepts = [] # Current percepts (Breeze, Stench, Glitter, Bump, Scream)

        # Agent's internal map of what it knows
        # Values could be: "Unknown", "Safe", "Breeze", "Stench", "Pit?", "Wumpus?"
        # Initialize as all "Unknown"
        self.known_grid = {}
        for r in range(self.config.GRID_SIZE):
            for c in range(self.config.GRID_SIZE):
                self.known_grid[(r, c)] = {"status": "Unknown", "percepts": [], "visited": False}
        self.known_grid[self.row, self.col]["visited"] = True
        self.known_grid[self.row, self.col]["status"] = "Safe"

        self.knowledge_base = KnowledgeBase(config) # For logical inference
        self.knowledge_base.tell(f"Safe({self.row},{self.col})")

    def update_percepts(self, percepts):
        self.percepts = percepts

    def update_score(self, amount):
        self.score += amount

    def move(self, new_row, new_col):
        self.row = new_row
        self.col = new_col
        self.score += self.config.MOVE_COST
        self.known_grid[(self.row, self.col)]["visited"] = True

    def shoot(self):
        if self.has_arrow:
            self.has_arrow = False
            self.score += self.config.SHOOT_COST
            return True
        return False

    def grab_gold(self):
        if not self.has_gold and self.config.GLITTER in self.percepts:
            self.has_gold = True
            self.score += self.config.GRAB_GOLD_REWARD
            return True
        return False

    def climb_out(self):
        if self.row == self.config.AGENT_START[0] and self.col == self.config.AGENT_START[1]:
            if self.has_gold:
                self.score += self.config.CLIMB_OUT_REWARD
                return True # Game won
        return False # Cannot climb out from elsewhere or without gold

    def turn_left(self):
        directions = ["right", "up", "left", "down"]
        current_index = directions.index(self.direction)
        self.direction = directions[(current_index + 1) % 4]

    def turn_right(self):
        directions = ["right", "up", "left", "down"]
        current_index = directions.index(self.direction)
        self.direction = directions[(current_index - 1 + 4) % 4]

    def infer_from_percepts(self):
        # This is where the agent's logical reasoning happens.
        # It updates its 'known_grid' based on current percepts and rules.
        # Example: If a square is safe and has a breeze, its neighbors *might* have pits.
        # If a square is safe and has a stench, its neighbors *might* have a wumpus.

        r, c = self.row, self.col
        self.known_grid[(r, c)]["percepts"] = self.percepts # Store current percepts

        # Mark current cell as safe if not already marked as such (e.g., if it was just visited)
        if self.known_grid[(r, c)]["status"] != "Wumpus?" and self.known_grid[(r, c)]["status"] != "Pit?":
            self.known_grid[(r, c)]["status"] = "Safe"
            self.knowledge_base.tell(f"Safe({r},{c})")

        neighbors = self._get_neighbors(r, c)

        if self.config.BREEZE in self.percepts:
            # If breeze, mark neighbors as potentially having a pit
            for nr, nc in neighbors:
                if self.known_grid[(nr, nc)]["status"] == "Unknown":
                    self.known_grid[(nr, nc)]["status"] = "Pit?"
                    self.knowledge_base.tell(f"MaybePit({nr},{nc})")

        if self.config.STENCH in self.percepts:
            # If stench, mark neighbors as potentially having a wumpus
            for nr, nc in neighbors:
                if self.known_grid[(nr, nc)]["status"] == "Unknown":
                    self.known_grid[(nr, nc)]["status"] = "Wumpus?"
                    self.knowledge_base.tell(f"MaybeWumpus({nr},{nc})")

        if not self.config.BREEZE in self.percepts:
            # If no breeze, neighbors are safe from pits
            for nr, nc in neighbors:
                if self.known_grid[(nr, nc)]["status"] == "Pit?":
                    self.known_grid[(nr, nc)]["status"] = "Safe"
                    self.knowledge_base.tell(f"Safe({nr},{nc})")
                elif self.known_grid[(nr, nc)]["status"] == "Unknown":
                    self.known_grid[(nr, nc)]["status"] = "Safe"
                    self.knowledge_base.tell(f"Safe({nr},{nc})")

        if not self.config.STENCH in self.percepts:
            # If no stench, neighbors are safe from wumpus
            for nr, nc in neighbors:
                if self.known_grid[(nr, nc)]["status"] == "Wumpus?":
                    self.known_grid[(nr, nc)]["status"] = "Safe"
                    self.knowledge_base.tell(f"Safe({nr},{nc})")
                elif self.known_grid[(nr, nc)]["status"] == "Unknown":
                    self.known_grid[(nr, nc)]["status"] = "Safe"
                    self.knowledge_base.tell(f"Safe({nr},{nc})")

        # More complex inferences using the KB (e.g., if A is safe, and B is adjacent to A,
        # and A has a breeze, then if C is another safe neighbor of A, and C has no breeze,
        # then the pit must be near B). This is where the KB shines.
        # This is a placeholder for more advanced logical inference.
        # For example, if KB says "NOT Pit(x,y)", update known_grid accordingly.
        # self.knowledge_base.ask("Pit(x,y)") etc.

    def _get_neighbors(self, r, c):
        neighbors = []
        possible = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        for nr, nc in possible:
            if 0 <= nr < self.config.GRID_SIZE and 0 <= nc < self.config.GRID_SIZE:
                neighbors.append((nr, nc))
        return neighbors

    # Placeholder for AI agent's decision-making
    def choose_action(self):
        # This function would contain the AI's logic to decide its next move.
        # For a human-played game, this function is not needed.
        # For an AI, it would use self.known_grid and self.percepts
        # to decide whether to move, shoot, grab, or climb.
        # E.g., if glitter, grab gold. If safe path, move. If wumpus suspected, shoot.
        pass