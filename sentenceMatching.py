import string
import random

POPULATION_SIZE = 30
NO_OF_PARENTS = 2
CHANCE_OF_MUTATION = 0.1
valid_chars = string.ascii_lowercase + ' ' + string.digits
NUMBER_OF_GEN = 0

# The final sentence to be generated
sentence = "i love programming"
SENTENCE_LENGTH = len(sentence)



def generate_random_candidate(size):
	""" Generate a random candidate """
	return ''.join(random.choice(valid_chars) for _ in range(size))

def generate_random_population(size):
	""" generate a random set of cadidates for starting out """
	first_population = [generate_random_candidate(size=size) for _ in range(POPULATION_SIZE)]
	return first_population

def calculate_fitness(candidate, ideal):
	""" calculate fitness of individual candidates by comparing them to the end result """
	fitness_score = 0
	for i in range(len(ideal)):
		if candidate[i] == ideal[i]:
			fitness_score += 1
	return fitness_score

def select_fittest(fitness_dict):
	""" select the top fittest candidates by sorting them with respect to their fitness """
	sorted_dict = sorted(fitness_dict, key=fitness_dict.get, reverse=True)
	return sorted_dict[0:NO_OF_PARENTS]

def selection_process(population, ideal):
	""" The controller function for doing fitness calculation and selecting the fittest """
	global fitness_dict
	fitness_dict = dict()
	for candidate in population:
		fitness_score = calculate_fitness(candidate=candidate, ideal=ideal)
		fitness_dict[candidate] = fitness_score

	fittest_candidates = select_fittest(fitness_dict)
	return fittest_candidates

def generate_population(selected_candidates):
	""" generate population by crossing the fittest candidates and sometimes perform mutation """
	new_population = []
	for i in range(POPULATION_SIZE):
		new_candidate = ''
		for j in range(SENTENCE_LENGTH):
			mutation_decision = random.random()
			if mutation_decision > CHANCE_OF_MUTATION:
				candidate_parent = random.choice(selected_candidates)
				new_candidate += candidate_parent[j]
			else:
				new_candidate += random.choice(valid_chars)
		new_population.append(new_candidate)
	return new_population



	
# initialize the population list with random values
population = generate_random_population(size=SENTENCE_LENGTH)

# loop until the sentence is generated
while True:

	NUMBER_OF_GEN += 1

	# perform fitness calculation and selection
	selected_candidates = selection_process(population=population, ideal=sentence)

	# perform breeding and mutation
	population = generate_population(selected_candidates)

	# gradually anneal(reduce) the chance of mutation
	CHANCE_OF_MUTATION -= (CHANCE_OF_MUTATION - 0.001)/20000

	# Stuff for printing helpful stats
	if NUMBER_OF_GEN % 10 == 0:
		print("Generation {0}: {1}".format(NUMBER_OF_GEN, selected_candidates[0]))
	if NUMBER_OF_GEN % 1000 == 0:
		curr_fitness = fitness_dict[selected_candidates[0]] / SENTENCE_LENGTH
		print("Generation {0}: Fitness = {1}".format(NUMBER_OF_GEN, curr_fitness))
		input("Press Enter to Continue")
	if selected_candidates[0] == sentence:
		print("Generation {0}: {1}".format(NUMBER_OF_GEN, selected_candidates[0]))
		print("Successfully Generated sentence: {0}".format(selected_candidates[0]))
		break

