import random
import math
import antennas as antenna
import pdb

def start_population(pop_size, side_length, antenna_qty, min_distance, max_distance):
    population = []

    for _ in range(pop_size):
        individual = []

        # posição aleatória
        individual.append((random.uniform(0, side_length), random.uniform(0, side_length)))

        for _ in range(1, antenna_qty):
            while True:
                new_x = random.uniform(0, side_length)
                new_y = random.uniform(0, side_length)
                new_position = (new_x, new_y)

                # Verificar se a nova posição respeita a distância mínima e maxima em relação às antenas já posicionadas
                if all(distance(new_position, individual[j]) <= max_distance for j in range(len(individual))):
                    if all(distance(new_position, individual[j]) >= min_distance for j in range(len(individual))): 
                        individual.append(new_position)
                        break

        population.append(individual)

    return population

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def calculate_fitness(individual, side_length, range_radius):
    antenna_positions = [(ind[0], ind[1]) for ind in individual]

    # Executa primeiro o plotting para gerar a imagem
    antenna.plot_antennas(antenna_positions, side_length, range_radius)

    # Depois calcula a área em verde (sem cobertura pelas antenas)
    return antenna.calculate_uncovered_area()

def selection(population, fitness_pop):
    parents = []
    for _ in range(2):
        # Seleciona 3 indivíduos aleatórios
        candidates = random.sample(list(enumerate(population)), 3)

        # Seleciona o melhor dos 3
        parent_index = max(candidates, key=lambda x: fitness_pop[x[0]])[0]
        parents.append(population[parent_index])
    return parents

def crossover(parent_1, parent_2, antenna_qty):
    cut = random.randint(1, antenna_qty - 1)
    son_1 = parent_1[:cut] + parent_2[cut:]
    son_2 = parent_2[:cut] + parent_1[cut:]
    return son_1, son_2

# Função de mutação respeitando a distância mínima e maxima entre antenas
def mutation(individual, population, mutation_probability, min_distance, max_distance):
    # Não sofre mutação se o número sorteado estiver abaixo da probabilidade configurada
    if random.random() > mutation_probability:
        return individual

    mutated = False
    antenna_index = random.randint(1, 3)

    # Pega outra antena aleatória da população respeitando a regra de distância
    while mutated == False:
        randomized_index = random.randrange(len(population))

        for new_position in population[randomized_index]:
            if (min_distance <= distance(individual[antenna_index], new_position) <= max_distance):
                individual[antenna_index] = new_position
                mutated = True

    return individual

def elitism(elitism_qty, population_qty, population, fitness_pop):
    elitism_index = sorted(range(population_qty), key=lambda x: fitness_pop[x])[:elitism_qty]
    new_population = [population[indice] for indice in elitism_index]

    return new_population
