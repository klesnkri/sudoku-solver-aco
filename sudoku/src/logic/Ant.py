import random


class Ant:
    def __init__(self, pher_matrix=None, initial_pher_val=0, local_pher_update=0, greediness=1, grid=None,
                 start_pos=(0, 0)):
        self.pher_matrix = pher_matrix
        self.initial_pher_val = initial_pher_val
        self.local_pher_update = local_pher_update
        self.greediness = greediness
        self.grid = grid
        self.pos = start_pos

    def get_fixed_cnt(self):
        return self.grid.fixed_cell_cnt

    def step(self):
        cell = self.grid.get_cell(self.pos)

        if not cell.failed() and not cell.fixed():
            # Select value based on pheromone matrix
            pher = self.pher_matrix[self.pos[0]][self.pos[1]]
            best_val = 0
            best_pheromone = 0
            possible_vals = self.grid.get_cell(self.pos).possible_vals

            # Greedy selection
            if random.random() > self.greediness:
                for val in possible_vals:
                    if pher[val - 1] > best_pheromone:
                        best_val = val
                        best_pheromone = pher[val - 1]
            # Roulette wheel selection
            else:
                total_pher = 0
                wheel = []

                for val_idx in range(len(possible_vals)):
                    wheel.append(total_pher + pher[possible_vals[val_idx] - 1])
                    total_pher = wheel[val_idx]

                spin_val = total_pher * random.random()

                for val_idx in range(len(possible_vals)):
                    if wheel[val_idx] > spin_val:
                        best_val = possible_vals[val_idx]
                        break

            # Set value
            self.grid.set_cell_val(self.pos, best_val)

            # Propagate constraints
            self.grid.propagate_constraints_cell(self.pos)

            # Try deducing values of some cells
            self.grid.deduce_vals_all_cells()

            # Update local pheromone -> decrease the probability of the value being selected by other ant
            pher_val_to_update = self.pher_matrix[self.pos[0]][self.pos[1]][best_val - 1]
            self.pher_matrix[self.pos[0]][self.pos[1]][best_val - 1] = (
                                                                               1 - self.local_pher_update) * pher_val_to_update + self.local_pher_update * self.initial_pher_val

        # Move by one cell
        new_row = self.pos[0]
        new_col = self.pos[1] + 1

        if new_col == self.grid.grid_size:
            new_col = 0
            new_row += 1

        if new_row == self.grid.grid_size:
            new_row = 0

        self.pos = (new_row, new_col)
