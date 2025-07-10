# WumpusWorldGame/config.py

class Config:
    def __init__(self):
        self.GRID_SIZE = 5  # Default 5x5 grid
        self.NUM_PITS = 3   # Default number of pits
        self.WUMPUS_COUNT = 1
        self.GOLD_COUNT = 1
        self.AGENT_START = (0, 0) # Agent always starts at (0,0) in Wumpus World

        # Score parameters
        self.MOVE_COST = -1
        self.SHOOT_COST = -10
        self.GRAB_GOLD_REWARD = 1000
        self.CLIMB_OUT_REWARD = 10
        self.FALL_IN_PIT_COST = -1000
        self.WUMPUS_KILL_COST = -1000 # If agent dies
        self.WUMPUS_DEFEAT_REWARD = 500 # If wumpus is shot

        # Percepts
        self.BREEZE = "Breeze"
        self.STENCH = "Stench"
        self.GLITTER = "Glitter"
        self.BUMP = "Bump"
        self.SCREAM = "Scream"

        # Game states
        self.GAME_RUNNING = "Running"
        self.GAME_OVER_WON = "Won"
        self.GAME_OVER_LOST = "Lost"

        # UI Colors (can be configured)
        self.COLOR_KNOWN = "#ADD8E6"  # Light Blue
        self.COLOR_UNKNOWN = "#A9A9A9" # Dark Gray
        self.COLOR_AGENT = "#FFD700"  # Gold
        self.COLOR_WUMPUS_KNOWN = "#8B0000" # Dark Red
        self.COLOR_PIT_KNOWN = "#4F4F4F"   # Darker Gray
        self.COLOR_GOLD_KNOWN = "#FFC300" # Brighter Gold
        self.COLOR_WUMPUS_PERCEIVED = "#FF6347" # Tomato Red
        self.COLOR_PIT_PERCEIVED = "#708090"    # Slate Gray
        self.COLOR_GOLD_PERCEIVED = "#FFEB3B"   # Yellow
        self.COLOR_SAFE = "#90EE90"   # Light Green
        self.COLOR_DANGER = "#FF4500" # Orange Red