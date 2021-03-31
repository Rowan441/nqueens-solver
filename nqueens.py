import random


# A solver that returns a list of queen's locations
def solve(board_size, ATTEMPTS=2000):

    # Algorithm struggles with n=6 so we return hard coded solution
    if board_size == 6:
        return [2, 4, 6, 1, 3, 5]

    # n=2 and n=3 do not have any solution
    if board_size == 2 or board_size == 3:
        return None

    solution = False

    while not solution:

        # Create the arrays for tracking queen conflicts
        conflicts = Conflicts(board_size)

        # First initialize a list of queen positions
        current = [-1 for i in range(board_size)]

        # Add queens to board
        current = conflicts.populateBoard(current, ATTEMPTS_PER_COLUMN=ATTEMPTS)

        # Track the number of step of the numConflicts algorithm
        MAX_STEPS = 200
        steps = 0

        # Preform a while loop until the nQueens is solved or MAX_STEPS elapsed
        while (not conflicts.isSolved()) and (steps <= MAX_STEPS):
            steps += 1

            # Find the current queens with the most conflicts
            highestConflicts = -1
            mostConflictedQueens = [-1]  # List of queens with the highest number of conflicts
            for i in range(len(current)):
                thisQueensConflicts = conflicts.numConflicts(i, current[i])

                if thisQueensConflicts > highestConflicts:
                    highestConflicts = thisQueensConflicts
                    mostConflictedQueens = [i]
                elif thisQueensConflicts == highestConflicts:
                    mostConflictedQueens.append(i)

            # Randomly pick from the list of most conflicted queens
            index = random.choice(mostConflictedQueens)

            # Move the queens at 'index'
            current[index] = conflicts.moveQueen(index, current[index])

        # if we've exited the loop in less than the max_steps, there is a valid solution
        if steps <= MAX_STEPS:
            return [x + 1 for x in current]

        # if we are here the minConflicts algorithm failed, so we start again...


# Class that holds all information for the current conflicts on the board
class Conflicts:

    def __init__(self, board_size):
        self.board_size = board_size
        self.rowConflicts = [0 for i in range(board_size)]
        self.upDiagConflicts = [0 for i in range(2 * board_size - 1)]
        self.downDiagConflicts = [0 for i in range(2 * board_size - 1)]

    # Checks if the board is in a solved state
    def isSolved(self):
        # Return false if there are ANY conflicts
        for i in range(self.board_size):
            if self.rowConflicts[i] > 1:
                return False
        for i in range(2 * self.board_size - 1):
            if self.upDiagConflicts[i] > 1:
                return False
            if self.downDiagConflicts[i] > 1:
                return False
        # Otherwise return true
        return True

    def populateBoard(self, current, ATTEMPTS_PER_COLUMN=2000):

        # Generate a random permutation of rows
        potentialRows = list(range(self.board_size))

        # Keep track of all columns that could not find a safe home for their queen
        failedColumns = []

        for column in range(len(current)):

            successfulPlacement = False
            for attempt in range(ATTEMPTS_PER_COLUMN):

                # Take the first row from the list
                maybeRow = potentialRows.pop(0)

                # If there are no conflicts, place the queen on maybeRow
                if self.numConflicts(column, maybeRow, queenOnSpot=False) == 0:
                    current[column] = maybeRow
                    self.addQueen(column, maybeRow)  # Keeps track of conflicts
                    successfulPlacement = True
                    # Queen has a safe home, so no more attempts are needed
                    break
                else:
                    # If the row was not a safe home, add it back to the end of the list for other queens
                    potentialRows.append(maybeRow)

            if not successfulPlacement:
                failedColumns.append(column)

        # Now put all the remaining queens from failedColumns in any remaining spots
        for column in failedColumns:
            row = potentialRows.pop(0)
            current[column] = row
            self.addQueen(column, row)  # Keeps track of conflicts

        return current

    # For a given column: Finds the best row to place a queen to minimize conflicts.
    def placeQueen(self, column):

        # Find number of conflicts on all possible rows
        possibleRows = []
        for row in range(self.board_size):
            possibleRows.append(self.numConflicts(column, row, queenOnSpot=False))

        # Find all rows with the minimal amount of conflicts in possibleRows
        leastConflicts = self.board_size + 1
        goodRows = []
        for row in range(len(possibleRows)):
            if possibleRows[row] < leastConflicts:
                leastConflicts = possibleRows[row]
                goodRows = [row]
            if possibleRows[row] == leastConflicts:
                goodRows.append(row)

        # Pick a random row from goodRows
        newRow = random.choice(goodRows)

        # Adjust the number of conflicts on the board when this queen is added
        # Because this is an initial placement, we don't have to removeQueen()
        self.addQueen(column, newRow)

        return newRow

    # moves a Queen to a better (less conflicted) row
    def moveQueen(self, column, row):
        # remove the queen from its original position
        self.removeQueen(column, row)
        # Find a better row
        return self.placeQueen(column)

    # adjusts the number of conflicts on the board if a queen is to be removed from the position at (column, row)
    def removeQueen(self, column, row):
        self.rowConflicts[row] -= 1
        self.upDiagConflicts[self.getUpDiag(column, row)] -= 1
        self.downDiagConflicts[self.getDownDiag(column, row)] -= 1

    # adjusts the number of conflicts on the board if a queen is to be added to the position at (column, row)
    def addQueen(self, column, row):
        self.rowConflicts[row] += 1
        self.upDiagConflicts[self.getUpDiag(column, row)] += 1
        self.downDiagConflicts[self.getDownDiag(column, row)] += 1

    # gets the upwards diagonal that the point (column, row) lies on
    def getUpDiag(self, column, row):
        return column + row

    # gets the downwards diagonal that the point (column, row) lies on
    def getDownDiag(self, column, row):
        return column - row + (self.board_size - 1)

    # get the number of conflicts at the given (column, row)
    def numConflicts(self, column, row, queenOnSpot=True):
        numConflicts = (
                self.rowConflicts[row] +  # number of queens on row
                self.upDiagConflicts[self.getUpDiag(column, row)] +  # number of queens on upward diagonal
                self.downDiagConflicts[self.getDownDiag(column, row)]  # number of queens on downward diagonal
        )
        # If there is a queen on the spot in question we must remove 3 to avoid counting conflicts with itself
        if queenOnSpot:
            numConflicts -= 3

        return numConflicts
