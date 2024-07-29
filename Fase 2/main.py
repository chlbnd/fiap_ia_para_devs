import antennas as an
import genetic_algorithm as ga

NUM_ANTENAS = 4
NUM_POPULACAO = 10
NUM_GERACOES = 10
NUM_ELITISMO = 3
AREA_LADO = 400

RAIO_ALCANCE = 100
DISTANCIA_MIN = 100
DISTANCIA_MAX = 300

PROB_MUTACAO = 0.5

def genetic_algorithm(pop_size, generation_qty):
    population = ga.start_population(pop_size, AREA_LADO, NUM_ANTENAS, DISTANCIA_MIN, DISTANCIA_MAX)

    fitness_pop = []

    for generation in range(generation_qty):
        # Avaliação da população
        fitness_pop = [ga.calculate_fitness(individual, AREA_LADO, RAIO_ALCANCE) for individual in population]

        # Se a cobertura do terreno já estiver completa
        if any(x == 0 for x in fitness_pop):
            break

        print(f'Geração: {generation + 1} - Fitness da população: {fitness_pop}')

        parents = [ga.selection(population, fitness_pop) for _ in range(pop_size // 2)]

        # Inicia a nova população com elitismo
        new_population = ga.elitism(NUM_ELITISMO, NUM_POPULACAO, population, fitness_pop)

        # Criando nova geração aplicando crossover e mutação
        for parent_1, parent_2 in parents:
            son_1, son_2 = ga.crossover(parent_1, parent_2, NUM_ANTENAS)

            son_1 = ga.mutation(son_1, population, PROB_MUTACAO, DISTANCIA_MIN, DISTANCIA_MAX)
            new_population.append(son_1)

            if (len(new_population) >= NUM_POPULACAO):
                break

            son_2 = ga.mutation(son_2, population, PROB_MUTACAO, DISTANCIA_MIN, DISTANCIA_MAX)
            new_population.append(son_2)

        # Substituição da população antiga pela nova geração
        population = new_population

    # Retornar a melhor solução encontrada
    best_index = min(range(pop_size), key=lambda x: fitness_pop[x])
    print(f"Melhor fitness calculado: {fitness_pop[best_index]}")
    return population[best_index]

def print_result(solution):
    print("Melhor solução encontrada:")
    for i, position in enumerate(solution):
        print(f"Antena {i+1}: ({position[0]:.2f}, {position[1]:.2f})")

best_solution = genetic_algorithm(pop_size=NUM_POPULACAO, generation_qty=NUM_GERACOES)

print_result(best_solution)
an.plot_antennas(best_solution, AREA_LADO, RAIO_ALCANCE, show_plot=True)
