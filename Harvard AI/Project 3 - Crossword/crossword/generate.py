import sys
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox(
                            (0, 0),
                            letters[i][j], font=font
                        )
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Deep copying prevents modification during iteration error.
        domain = copy.deepcopy(self.domains)

        for var in domain.keys():
            for word in domain[var]:
                # If the word isn't the required length (unary constraint).
                if len(word) != var.length:
                    # Remove it from the domain.
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Coordinates of overlap between the two variables.
        overlap = self.crossword.overlaps[x, y]
        revised = False

        if overlap is None:
            return False
        else:
            i, j = overlap
            for v1 in self.domains[x].copy():
                satisfied = False
                for v2 in self.domains[y]:
                    # If the overlapping characters are identical.
                    if v1[i] == v2[j]:
                        # Then the binary constraint is met.
                        satisfied = True
                # If no common overlap, v1 is removed from x's domain.
                if not satisfied:
                    self.domains[x].remove(v1)
                    # A change is made, hence revised is true.
                    revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = []

        # If arcs is none, an initial queue of all arcs is used.
        if arcs is None:
            for x in self.domains.keys():
                for y in self.domains.keys():
                    # Arcs with non-identical variables added to the queue.
                    if x != y:
                        queue.append((x, y))

        # Otherwise, queue is initialised with given arcs.
        else:
            queue = [(x, y) for x, y in arcs]

        # Repeated until the queue is empty.
        while len(queue) > 0:
            # Arc is considered & removed from queue (Dequeue).
            x, y = queue.pop()
            # Checks if changes are made to make arc consistent.
            if self.revise(x, y):
                # If the resulting domain of x is empty, the csp is unsolvable.
                if len(self.domains[x]) == 0:
                    return False
                # Checks if other arcs associated with x are still consistent.
                for z in (self.crossword.neighbors(x) - {y}):
                    queue.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.

        An assignment `isn't` complete if:
        1. A variable present in self.domains is missing from the assignment.
        2. A variable present in the assignment has no value.
        """
        for var in self.domains.keys():
            if var not in assignment.keys() or assignment[var] is None:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for var in assignment.keys():
            # v1 is the value of variable 'var' in the assignment.
            v1 = assignment[var]

            # Length of the value must be the variable's length.
            if len(v1) != var.length:
                return False

            # Every value must be distinct and occur only once.
            elif list(assignment.values()).count(v1) > 1:
                return False

            # Locates every possible neighbour of the variable.
            neighbors = self.crossword.neighbors(var)

            # Locates every neighbour which is also in the assignment.
            available_neighbors = neighbors.intersection(assignment)

            for neighbor in available_neighbors:
                i, j = self.crossword.overlaps[var, neighbor]
                v2 = assignment[neighbor]
                # Conflicting overlapping characters results in inconsistency.
                if v1[i] != v2[j]:
                    return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        domain = self.domains[var]

        """Dictionary with possible variable values &
        corresponding count of constrained variables."""
        values = {value: 0 for value in domain}

        # All neighbours of variable not present in assignment.
        neighbors = self.crossword.neighbors(var) - set(assignment.keys())

        for v1 in domain:
            constrained = 0
            for neighbor in neighbors:
                for v2 in self.domains[neighbor]:
                    overlap = self.crossword.overlaps[var, neighbor]
                    if overlap:
                        i, j = overlap
                        # If the overlapping characters are identical.
                        if v1[i] != v2[j]:
                            # This value 'v1' puts a constraint on 'neighbor'.
                            constrained += 1
            values[v1] += constrained

        # Returns a list in ascending order of 'constrained' count.
        return sorted([value for value in values], key=lambda x: values[x])

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # A list of all variables present in the domain but not in assignment.
        unassigned = list(set(self.domains.keys()) - set(assignment.keys()))

        # List is sorted based on heuristic values.
        variables = sorted(unassigned, key=lambda x: self.heuristics(x))

        # Value with minimum remaining values (followed by highest degree).
        return variables[0]

    # Helper function which returns heuristic values.
    def heuristics(self, variable):
        # Number of remaining values present in domain.
        remaining = len(self.domains[variable])

        # Number of neighbours (degree) of variable.
        # Negated to ensure the highest degree is picked first.
        degree = -len(self.crossword.neighbors(variable))

        # Returns heuristics in order of precedence.
        return remaining, degree

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # A finished algorithm will return the completed assignment.
        if self.assignment_complete(assignment):
            return assignment

        # If not complete, it will select an unassigned variable.
        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                # If the assignment is consistent, recursion is used.
                result = self.backtrack(assignment)
                # If the resulting value is not a failure, return it.
                if result:
                    return result
                # Otherwise, remove the variable from the assignment.
                del assignment[var]
        # Returns failure.
        return None


def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
