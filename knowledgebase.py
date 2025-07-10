# WumpusWorldGame/kb.py

from config import Config

class KnowledgeBase:
    def __init__(self, config: Config):
        self.config = config
        self.facts = set() # Store known facts (e.g., "Safe(0,0)", "HasBreeze(1,0)")

    def tell(self, fact):
        """Adds a fact to the knowledge base."""
        self.facts.add(fact)

    def ask(self, query):
        """
        Queries the knowledge base for a fact.
        For a more advanced KB, this would involve inference rules.
        For now, it's a simple lookup.
        """
        return query in self.facts

    def infer_safe_from_no_percepts(self, r, c, neighbors_percepts):
        """
        Example inference: If a cell (r,c) has no breeze and no stench,
        then its neighbors are safe from pits and Wumpus.
        """
        # This is typically called by the agent's infer_from_percepts method
        # but the KB could also contain more general rules.
        pass

    def apply_wumpus_logic(self, known_grid):
        """
        More complex inference rules for Wumpus location.
        E.g., if a Wumpus? cell is adjacent to a non-stench cell, it cannot be a Wumpus.
        """
        # This is where a more sophisticated inference engine would live.
        # For example, using resolution or forward/backward chaining.
        pass

    def apply_pit_logic(self, known_grid):
        """
        More complex inference rules for Pit location.
        """
        pass