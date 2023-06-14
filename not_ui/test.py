import random
from deap import base, creator, tools


# Define the problem and create a fitness function
def evaluate(individual):
    # Calculate the fitness score of the individual
    fitness_score = 0

    # Iterate through each day of the schedule
    for day_index, day in enumerate(individual):
        lectures_scheduled = []
        # Check if each teacher is available during their scheduled lecture
        for lecture in day:
            day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            if not lecture:
                continue
            teacher = lecture[0]
            subject = lecture[1]
            timeslot = lecture[2]
            day_name = day_names[day_index]
            lecture_info = (teacher, subject, timeslot, day_name)
            if not is_teacher_available(lecture_info):
                fitness_score += 1
            if timeslot in lectures_scheduled:
                fitness_score += 1
            lectures_scheduled.append(timeslot)

        # Check if the maximum number of lectures per day is exceeded
        if has_max_lectures_per_day(day):
            fitness_score += 1

        # Check if there are gaps between lectures
        if has_no_gaps(day):
            fitness_score += 1

    return (fitness_score,)


day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
teachers = ["John", "Mary", "Bob"]
subjects = ["Math", "English", "History"]
timeslots = ["9:00-10:30", "10:45-12:15", "1:00-2:30", "2:45-4:15"]
# Define the individuals
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
toolbox.register("lecture", lambda: (
random.choice(teachers), random.choice(subjects), random.choice(timeslots), random.choice(day_names)))
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.lecture, n=5)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Define the genetic operators
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.1)


# Define the constraints
# Define the constraints
def is_teacher_available(day):
    teacher_availability = {"John": ["Monday 9.00-10.30", "Monday 10.45-12.15"],
                            "Mary": ["Monday 10.45-12.15", "Tuesday 9.00-10.30"],
                            "Bob": ["Monday 9.00-10.30", "Tuesday 10.45-12.15"]}
    for lecture in day:
        if lecture and lecture[0] in teacher_availability:
            lecture_time = lecture[2]
            if lecture_time not in teacher_availability[lecture[0]]:
                return False
    return True


def has_max_lectures_per_day(day):
    # Returns True if the maximum number of lectures per day is not exceeded, and False otherwise
    max_lectures_per_day = 5
    return sum(1 for lecture in day if lecture) > max_lectures_per_day


def has_no_gaps(day):
    # Returns True if there are no gaps between lectures, and False otherwise
    return not any(day[i] and not day[i + 1] for i in range(len(day) - 1))


def has_no_same_lectures_in_a_row(day):
    # Returns True if there are no two same lectures in a row, and False otherwise
    for i in range(len(day) - 1):
        if day[i] and day[i + 1] and day[i] == day[i + 1]:
            return False
    return True


# Implement the algorithm
def main():
    # Initialize the population of individuals
    population = toolbox.population(n=100)
    # Evaluate the fitness of each individual
    fitnesses = list(map(evaluate, population))
    # Assign the fitness to each individual
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    # Repeat the evolution process until a satisfactory solution is found
    for generation in range(100):
        # Select the fittest individuals from the population using tournament selection
        selected = tools.selTournament(population, k=len(population), tournsize=3)
        # Create a copy of the selected individuals
        offspring = [toolbox.clone(ind) for ind in selected]

        # Apply crossover and mutation operators to create new individuals
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < 0.5:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        for mutant in offspring:
            if random.random() < 0.2:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the fitness of the new individuals
        new_fitnesses = list(map(evaluate, offspring))
        for ind, fit in zip(offspring, new_fitnesses):
            ind.fitness.values = fit

        # Replace the weakest individuals in the population with the new individuals
        population[:] = tools.selBest(selected + offspring, k=len(population))

        # Check if a satisfactory solution is found
        if any(ind.fitness.values[0] == 0 for ind in population):
            break

    # Output the best individual as the schedule
    best_ind = tools.selBest(population, k=1)[0]
    print("Best schedule:", best_ind)
    print("Fitness score:", best_ind.fitness.values[0])


if __name__ == "__main__":
    main()