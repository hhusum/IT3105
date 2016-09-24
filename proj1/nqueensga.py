import random

class problemState():
    """Contains information dependent on problem size to be looked up.
    Should not be changed after initialization."""
    def __init__(self, size):
        self.size = size
        self.comb = problemState.nC2List(size + 1)
        self.target = self.comb[size]
        self.diagCoords = problemState.diagonalCoordinates(size)

    def nC2List(n):
        """List of n choose 2 from 0 to n"""
        l = []
        for i in range(n):
            l.append(int(i*(i-1)/2))
        return(l)

    def diagonalCoordinates(size):
        """Returns a lookup table of diagonal coordinates for each board square. In
        this context a diagonal coordinate is the diagonal number for the sqare, both
        from NW to SE and SW to NE, ordered from west to east. Coordinate location in
        the table is given by standard column and rom number."""
        diagCoords = [[[0 for i in range(2)] for j in range(size)] for k in range(size)]
        for col in range(size):
            for row in range(size):
                #NW to SE diagonal
                diagCoords[col][row][0] = col - row + size - 1
                #SW to NE diagonal
                diagCoords[col][row][1] = col + row
        return diagCoords

class boardState():
    def __init__(self, pS, **kwargs):
        self.pS = pS
        self.board = kwargs.get('board')
        if self.board is not None:
            self.locationStates();
            self.energy()
            self.req = 0

    def locationStates(self):
        """Returns a lookup table for number of queens in a given diagonal"""
        self.locStates = [[0 for i in range(self.pS.size)], [0 for i in range(2 * self.pS.size - 1)], [0 for i in range(2 * self.pS.size - 1)]]
        for col in range(self.pS.size):
            row = self.board[col]
            self.locStates[0][row] += 1
            #marking NW to SE diagonal as under attack
            self.locStates[1][self.pS.diagCoords[col][row][0]] += 1
            #marking SW to NE diagonal as under attack
            self.locStates[2][self.pS.diagCoords[col][row][1]] += 1

    def energy(self):
        self.energy = self.pS.target
        for locList in self.locStates:
            for line in locList:
                    self.energy -= self.pS.comb[line]

    def neighbour(self):
        col = random.randint(0, self.pS.size-1)
        row = random.randint(0, self.pS.size-1)
        newBoard = self.board[:]
        newBoard[col] = row
        neighbour = boardState(self.pS, board=newBoard)
        return neighbour

class population():
	def __init__(self, boardState):

def initializePopulation(bS, pS):
	population = []
	population.append(bS)
	for i in range(size-1):
		derivative = bS.board[:]
		for i in range(2):
			col = random.randint(0, pS.size-1)
        	row = random.randint(0, pS.size-1)
        	derivative[col] = row
        population.append(boardState(pS, board=derivative))
    return population

def rouletteWheelSelection(population, pointers):
    keep = []
    for p in pointers:
        i = 0
        fSum = 0
        while fSum < p:
            fSum+=population[i].energy
            i++
        keep.append(population[i])
    return keep


def stocasticUniversalSampling(population, n):
    f = 0
    for individual in population:
        f += individual.energy
    pD = f/n
    sP = random.randint(0, pD)
    pointers = [(sP + i*pD) for i in range(n-1)]
    return rouletteWheelSelection(population, pointers)

def nQueensGenAlg(initPop, itr):
    population = initPop
    solutions = []
    for i in range(itr):
        parents = stocasticUniversalSampling(population, 30)
        children = mutate(reproduce(parents))
        population = selectFromPopulations(parents, children)
        for individual in population:
        	if individual.energy: #is goal
        		solutions.append(individual)
    return solutions

def main():
	inBoard = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

	pS = problemState(len(inBoard))

    bS = boardState(pS, board=inBoard)

    initPop = initializePopulation(bS, 50)

    solutions = nQueensGenAlg(initPop, 1000)

if __name__ == '__main__':
    main()
