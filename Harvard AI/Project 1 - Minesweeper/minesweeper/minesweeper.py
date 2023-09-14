import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # If number of cells is equal to the count, all cells are mines.
        if self.count == len(self.cells) != 0:
            return self.cells
        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If the count is equal to 0, all cells are safe.
        if self.count == 0:
            return self.cells
        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Check if cell is in sentence, then remove.
        if cell in self.cells:
            self.cells.remove(cell)
            # Number of mines in sentence decreases by 1 upon removal.
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Number of mines remain unchanged as cell is safe.
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring neighbours have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional neighbours as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # 1) Mark the cell as a move that has been made.
        self.moves_made.add(cell)

        # 2) Mark the cell as safe
        self.mark_safe(cell)

        # 3) Adding a new sentence to the AI's knowledge base.
        neighbours = set()  # Set of neighbouring cells.

        # Adding neighbouring neighbours to set.
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # If identified as mine, remove from sentence and decrease count.
                if (i, j) in self.mines:
                    count -= 1
                    continue

                # If safe, played move, or cell itself then ignore.
                elif (i, j) in self.safes or (i, j) in self.moves_made or (i, j) == cell:
                    continue

                # Ensure cell is within game grid, then add to neighbours
                elif 0 <= i < self.height and 0 <= j < self.width:
                    neighbours.add((i, j))

        # Creating an adding new sentence to knowledge base.
        sentence = Sentence(neighbours, count)
        self.knowledge.append(sentence)

        # 4) Marking additional neighbours as safe or as mines.
        # Iterating through all sentences
        for sentence in self.knowledge:
            safes = sentence.known_safes()
            mines = sentence.known_mines()
            # First check if safes exist.
            if safes:
                # .copy() prevents modification during iteration of a set.
                for cell in safes.copy():
                    self.mark_safe(cell)
            if mines:
                for cell in mines.copy():
                    self.mark_mine(cell)

        # 5) Add any new sentences inferring from existing knowledge.
        # Nested loops to make comparison between 2 sentences.
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                # Subset method described in 'Background'.
                set1 = sentence1.cells
                set2 = sentence2.cells
                count1 = sentence1.count
                count2 = sentence2.count
                # Skip this iteration if number of mines or cells are same.
                if count1 == count2 or set1 == set2:
                    continue
                # set1 must be a subset of set2
                elif set1 in set2:
                    set3 = set2 - set1
                    count3 = count2 - count1
                    sentence = Sentence(set3, count3)
                    # Only add if sentence is new. Prevent duplication.
                    if sentence not in self.knowledge:
                        self.knowledge.add(sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Available safe moves which aren't already played.
        moves = self.safes - self.moves_made
        if moves:
            # Selects a random move from 'moves'.
            # set() doesn't support random.choice, hence converted to a list.
            return random.choice(list(moves))
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Set of all possible moves.
        moves = set([(i, j) for j in range(self.width) for i in range(self.height)])

        # All available moves, excluding mines and played moves.
        available_moves = moves - self.mines - self.moves_made

        # If any moves are available, return a random move.
        if available_moves:
            return random.choice(list(available_moves))
        return None
