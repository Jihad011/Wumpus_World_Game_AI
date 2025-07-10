# WumpusWorldGame/utils.py

def get_neighbors(row, col, grid_size):
    """Returns a list of valid neighboring coordinates."""
    neighbors = []
    possible = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
    for r, c in possible:
        if 0 <= r < grid_size and 0 <= c < grid_size:
            neighbors.append((r, c))
    return neighbors

# Add other utility functions as needed, e.g., for logging, data serialization etc.