# WumpusWorldGame/logic.py

from config import Config
from environment import WumpusEnvironment
from agent import WumpusAgent

class GameLogic:
    def __init__(self, environment: WumpusEnvironment, agent: WumpusAgent, config: Config):
        self.environment = environment
        self.agent = agent
        self.config = config
        self.game_state = self.config.GAME_RUNNING

    def perceive_current_location(self):
        current_percepts = self.environment.get_percepts_at_location(self.agent.row, self.agent.col)
        self.agent.update_percepts(current_percepts)

    def move_agent(self, direction):
        new_row, new_col = self.agent.row, self.agent.col
        if direction == "up":
            new_row -= 1
        elif direction == "down":
            new_row += 1
        elif direction == "left":
            new_col -= 1
        elif direction == "right":
            new_col += 1

        if not self.environment.is_valid_location(new_row, new_col):
            self.agent.update_percepts([self.config.BUMP]) # Add bump percept
            return False, "Bumped into a wall!"

        self.agent.move(new_row, new_col) # Update agent's position and score

        # Check for consequences of moving
        if self.environment.has_pit(new_row, new_col):
            self.agent.update_score(self.config.FALL_IN_PIT_COST)
            self.game_state = self.config.GAME_OVER_LOST
            return True, "You fell into a pit! Game Over."
        elif self.environment.has_wumpus(new_row, new_col):
            self.agent.update_score(self.config.WUMPUS_KILL_COST)
            self.game_state = self.config.GAME_OVER_LOST
            return True, "The Wumpus ate you! Game Over."

        return False, "" # Game continues

    def shoot_arrow(self):
        if not self.agent.has_arrow:
            return False, "No arrows left!"

        self.agent.shoot() # Deduct arrow and cost

        # Determine target based on agent's direction
        target_row, target_col = self.agent.row, self.agent.col
        if self.agent.direction == "up":
            target_row -= 1
        elif self.agent.direction == "down":
            target_row += 1
        elif self.agent.direction == "left":
            target_col -= 1
        elif self.agent.direction == "right":
            target_col += 1

        # The arrow flies only one square in Wumpus World
        if self.environment.is_valid_location(target_row, target_col):
            if self.environment.has_wumpus(target_row, target_col):
                self.environment.kill_wumpus()
                self.agent.update_score(self.config.WUMPUS_DEFEAT_REWARD)
                self.agent.update_percepts([self.config.SCREAM]) # Wumpus screams
                return False, "You shot the Wumpus! It screamed!"
            else:
                return False, "Your arrow flew into the void."
        else:
            return False, "You shot at a wall."

    def grab_gold(self):
        if self.environment.has_gold(self.agent.row, self.agent.col):
            self.agent.grab_gold()
            self.environment.remove_gold(self.agent.row, self.agent.col)
            return False, "You grabbed the gold!"
        return False, "No gold here to grab."

    def climb_out(self):
        if self.agent.climb_out():
            self.game_state = self.config.GAME_OVER_WON
            return True, "You successfully climbed out with the gold! You Win!"
        return False, "You can only climb out from the starting point with the gold!"