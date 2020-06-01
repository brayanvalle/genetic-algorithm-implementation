import random
import time

TARGET = "clase de ia poli jic"
INDIVIDUAL_SIZE = len(TARGET)
POPULATION_SIZE = 100
MUTATION_RATE = 0.5
TOURNAMENT_SELECTION_SIZE = 40

KEYS = 'abcdefghijklmnopqrstuvwxyz '

class Individual:
	def __init__(self):
		self._dna = random.choices(KEYS, k=INDIVIDUAL_SIZE)
		self._fitness = -1
		self._score = -1

	def getDNA(self):
		self._fitness = -1
		self._score = -1
		return self._dna

	@property
	def fitness(self):
		if self._score == -1:	
			self._score = 0
			for own_letter, target_letter in zip(self._dna, TARGET):
				if own_letter == target_letter:
					self._score += 1

			self._fitness = self._score / len(TARGET)
		return self._fitness

	def __str__(self):
		return "".join(self._dna)

class Population:
	def __init__(self, size):
		self._population = []

		for i in range(size):
			self._population.append(Individual())

	def getPopulation(self):
		return self._population

class GeneticAlgorithm:
	def selectTournamentPopulation(self, pop):
		tournament_pop = Population(0)

		i = 0
		while i < TOURNAMENT_SELECTION_SIZE:
			tournament_pop.getPopulation().append(pop.getPopulation()[random.randrange(0, POPULATION_SIZE)])
			i += 1
			
		tournament_pop.getPopulation().sort(key = lambda x: x.fitness, reverse = True)
		return tournament_pop

	def reproduction(self, pop):
		for i in range(len(pop.getPopulation())):
			partnerA = self.selectTournamentPopulation(pop).getPopulation()[0]	
			partnerB = self.selectTournamentPopulation(pop).getPopulation()[1]	

			child = self.crossover(partnerA, partnerB)
			

			pop.getPopulation()[i] = child
		self.mutate(pop)
		
	def crossover(self, parentA, parentB):
		child = Individual()
		midpoint = random.randrange(0, INDIVIDUAL_SIZE)

		child.getDNA()[:midpoint] = parentA.getDNA()[:midpoint]
		child.getDNA()[midpoint:] = parentB.getDNA()[midpoint:]

		return child

	def mutate(self, pop):
		for x in pop.getPopulation():
			if random.random() <= MUTATION_RATE:
				x.getDNA()[random.randrange(0, INDIVIDUAL_SIZE)] = random.choice(KEYS)

	def evolve(self, pop):
		self.selectTournamentPopulation(pop)
		self.reproduction(pop)

def printPopulation(pop, genNumber):
	print("==========================================================")
	print("Generation #", genNumber, "| Fittest individual fitness: ", pop.getPopulation()[0].fitness)
	print("Target phrase:", TARGET)
	print("==========================================================")
	for i, x in enumerate(pop.getPopulation()):
		print("Individual #", i, ":", ''.join(x.getDNA()), "| Fitness: ", x.fitness)
	print()

def main():
    # generate initial population of size POPULATION_SIZE
	population = Population(POPULATION_SIZE)
	algo = GeneticAlgorithm()

	generationNumber = 0
	while True:
		population.getPopulation().sort(key = lambda x: x.fitness, reverse = True)
		printPopulation(population, generationNumber)

		if population.getPopulation()[0].fitness >= 1:
			break	
		algo.evolve(population)
		generationNumber += 1

	print("Simulation terminated, target reached")
	print("Target: {} | Fitness: {}".format(population.getPopulation()[0] , population.getPopulation()[0].fitness))

if __name__ == "__main__":
	main()

