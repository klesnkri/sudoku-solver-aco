class Cell:
    def __init__(self, grid_size):
        # Possible values of cell (1 - 9)
        self.possible_vals = []

        self.grid_size = grid_size

        for i in range(1, self.grid_size + 1):
            self.possible_vals.append(i)

    def fixed(self):
        return len(self.possible_vals) == 1

    def failed(self):
        return len(self.possible_vals) == 0

    def get_val(self):
        return self.possible_vals[0]

    # Set cell to value
    def set_val(self, new_val):
        self.possible_vals = [new_val]

    # Delete value from possible values
    def delete(self, val):
        self.possible_vals = [pos_val for pos_val in self.possible_vals if pos_val != val]

    def can_contain(self, val):
        for pos_val in self.possible_vals:
            if pos_val == val:
                return True
        return False
