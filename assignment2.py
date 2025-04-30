from search import *
from random import randint
from assignment2aux import *

def read_tiles_from_file(filename):
    lines = [line.rstrip('\n') for line in open(filename, 'r').readlines()]
    character_to_tile = {' ': (), 'i': (0,), 'L': (0, 1), 'I': (0, 2), 'T': (0, 1, 2)}
    return tuple(tuple(character_to_tile[character] for character in line) for line in lines)

class KNetWalk(Problem):
    def __init__(self, tiles):
        if type(tiles) is str:
            self.tiles = read_tiles_from_file(tiles)
        else:
            self.tiles = tiles
        height = len(self.tiles)
        width = len(self.tiles[0])
        self.max_fitness = sum(sum(len(tile) for tile in row) for row in self.tiles)
        super().__init__(self.generate_random_state())

    def generate_random_state(self):
        height = len(self.tiles)
        width = len(self.tiles[0])
        return [randint(0, 3) for _ in range(height) for _ in range(width)]

    def actions(self, state):
        height = len(self.tiles)
        width = len(self.tiles[0])
        return [(i, j, k) for i in range(height) for j in range(width) for k in [0, 1, 2, 3] if state[i * width + j] != k]

    def result(self, state, action):
        pos = action[0] * len(self.tiles[0]) + action[1]
        return state[:pos] + [action[2]] + state[pos + 1:]

    def goal_test(self, state):
        return self.value(state) == self.max_fitness

    def value(self, state):
        height = len(self.tiles)
        width = len(self.tiles[0])
        fitness = 0
        
        for i in range(height):
            for j in range(width):
                current_tile = self.tiles[i][j]
                current_orientation = state[i * width + j]
                
                # Calculate the oriented connections for current tile
                oriented_connections = tuple((con + current_orientation) % 4 for con in current_tile)
                
                # Check all four possible neighbors
                for direction in oriented_connections:
                    ni, nj = i, j  # neighbor coordinates
                    
                    if direction == 0:    # right
                        nj += 1
                    elif direction == 1:  # up
                        ni -= 1
                    elif direction == 2:  # left
                        nj -= 1
                    elif direction == 3:  # down
                        ni += 1
                    
                    # Check if neighbor is within bounds
                    if 0 <= ni < height and 0 <= nj < width:
                        neighbor_tile = self.tiles[ni][nj]
                        neighbor_orientation = state[ni * width + nj]
                        
                        # Calculate the oriented connections for neighbor tile
                        neighbor_oriented = tuple((con + neighbor_orientation) % 4 for con in neighbor_tile)
                        
                        # Check if neighbor has a connection back to current tile
                        opposite_dir = (direction + 2) % 4
                        if opposite_dir in neighbor_oriented:
                            fitness += 1
        
        return fitness

# Task 2
# Configure an exponential schedule for simulated annealing.
sa_schedule = exp_schedule(k=20, lam=0.005, limit=1000)

# Task 3
# Configure parameters for the genetic algorithm.
pop_size = 100
num_gen = 1000
mutation_prob = 0.1

def local_beam_search(problem, population):
    while True:
        # Check if any state in population is a goal state
        for state in population:
            if problem.goal_test(state):
                return state
        
        # Generate all successors
        successors = []
        for state in population:
            for action in problem.actions(state):
                successor = problem.result(state, action)
                successors.append((problem.value(successor), successor))
        
        # Sort successors by fitness in descending order
        successors.sort(reverse=True, key=lambda x: x[0])
        
        # Check if no improvement
        if len(population) > 0:
            current_best = max(problem.value(state) for state in population)
            if len(successors) > 0 and successors[0][0] <= current_best:
                return max(population, key=lambda state: problem.value(state))
        
        # Select top k successors (where k is the original population size)
        if len(successors) == 0:
            return max(population, key=lambda state: problem.value(state))
        
        population = [state for (val, state) in successors[:len(population)]]

def stochastic_beam_search(problem, population, limit=1000):
    # Task 5
    # Implement stochastic beam search.
    # Return a goal state if found in the population.
    # Return the fittest state in the population if the generation limit is reached.
    # Replace the line below with your code.
    raise NotImplementedError

if __name__ == '__main__':

    network = KNetWalk('assignment2config.txt')
    visualise(network.tiles, network.initial)

    # Task 1 test code
    '''
    run = 0
    method = 'hill climbing'
    while True:
        network = KNetWalk('assignment2config.txt')
        state = hill_climbing(network)
        if network.goal_test(state):
            break
        else:
            print(f'{method} run {run}: no solution found')
            print(f'best state fitness {network.value(state)} out of {network.max_fitness}')
            visualise(network.tiles, state)
        run += 1
    print(f'{method} run {run}: solution found')
    visualise(network.tiles, state)
    '''

    # Task 2 test code
    '''
    run = 0
    method = 'simulated annealing'
    while True:
        network = KNetWalk('assignment2config.txt')
        state = simulated_annealing(network, schedule=sa_schedule)
        if network.goal_test(state):
            break
        else:
            print(f'{method} run {run}: no solution found')
            print(f'best state fitness {network.value(state)} out of {network.max_fitness}')
            visualise(network.tiles, state)
        run += 1
    print(f'{method} run {run}: solution found')
    visualise(network.tiles, state)
    '''

    # Task 3 test code
    '''
    run = 0
    method = 'genetic algorithm'
    while True:
        network = KNetWalk('assignment2config.txt')
        height = len(network.tiles)
        width = len(network.tiles[0])
        state = genetic_algorithm([network.generate_random_state() for _ in range(pop_size)], network.value, [0, 1, 2, 3], network.max_fitness, num_gen, mutation_prob)
        if network.goal_test(state):
            break
        else:
            print(f'{method} run {run}: no solution found')
            print(f'best state fitness {network.value(state)} out of {network.max_fitness}')
            visualise(network.tiles, state)
        run += 1
    print(f'{method} run {run}: solution found')
    visualise(network.tiles, state)
    '''

    # Task 4 test code
    '''
    run = 0
    method = 'local beam search'
    while True:
        network = KNetWalk('assignment2config.txt')
        height = len(network.tiles)
        width = len(network.tiles[0])
        state = local_beam_search(network, [network.generate_random_state() for _ in range(100)])
        if network.goal_test(state):
            break
        else:
            print(f'{method} run {run}: no solution found')
            print(f'best state fitness {network.value(state)} out of {network.max_fitness}')
            visualise(network.tiles, state)
        run += 1
    print(f'{method} run {run}: solution found')
    visualise(network.tiles, state)
    '''

    # Task 5 test code
    '''
    run = 0
    method = 'stochastic beam search'
    while True:
        network = KNetWalk('assignment2config.txt')
        height = len(network.tiles)
        width = len(network.tiles[0])
        state = stochastic_beam_search(network, [network.generate_random_state() for _ in range(100)])
        if network.goal_test(state):
            break
        else:
            print(f'{method} run {run}: no solution found')
            print(f'best state fitness {network.value(state)} out of {network.max_fitness}')
            visualise(network.tiles, state)
        run += 1
    print(f'{method} run {run}: solution found')
    visualise(network.tiles, state)
    '''
