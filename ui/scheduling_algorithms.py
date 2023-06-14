import random
import copy


class GeneticAlgorithm:
    def __init__(self, teachers, rooms, groups, pop_size):
        self.teachers = teachers
        self.rooms = rooms
        self.groups = groups
        self.pop_size = pop_size

    def init_population(self):
        population = []
        for _ in range(self.pop_size):
            schedule = [[[[None, None, None] for _ in range(5)] for _ in range(5)] for _ in range(len(self.groups))]  # Each cell will have [Teacher, Subject, Room]
            for group_index, group in enumerate(self.groups):
                for day in range(5):
                    for slot in range(5):
                        available_teachers = [teacher for teacher in self.teachers if teacher.availability[day][slot]]
                        if not available_teachers:
                            continue
                        teacher = random.choice(available_teachers)
                        subject = random.choice(teacher.subjects)
                        room = random.choice([room for room in rooms if room.capacity >= group.size])
                        schedule[group_index][day][slot] = [teacher, subject, room]
            population.append(schedule)
        return population

    def fitness(self, schedule):
        return sum(1 for group in schedule for day in group for slot in day if slot[0] is not None)

    def select_parents(self, population):
        tournament_size = 5
        tournament = random.sample(population, tournament_size)
        parent1 = max(tournament, key=self.fitness)
        tournament.remove(parent1)
        parent2 = max(tournament, key=self.fitness)
        return parent1, parent2

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(0, 4)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    def mutate(self, schedule):
        mutated_schedule = copy.deepcopy(schedule)
        group_index, day, slot = random.randint(0, len(self.groups) - 1), random.randint(0, 4), random.randint(0, 4)
        available_teachers = [teacher for teacher in self.teachers if teacher.availability[day][slot]]
        if not available_teachers:
            return mutated_schedule
        teacher = random.choice(available_teachers)
        subject = random.choice(teacher.subjects)
        room = random.choice([room for room in self.rooms if room.capacity >= self.groups[group_index].size])
        mutated_schedule[group_index][day][slot] = [teacher, subject, room]
        return mutated_schedule

    def evolve_population(self, population):
        new_population = []
        while len(new_population) < len(population):
            parent1, parent2 = self.select_parents(population)
            child1, child2 = self.crossover(parent1, parent2)
            if random.random() < 0.1:  # mutation probability
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
            new_population.extend([child1, child2])
        return new_population

    def generate(self):
        population = self.init_population()
        for _ in range(100):  # number of generations
            population = self.evolve_population(population)
        # sort final population by fitness
        population.sort(key=self.fitness, reverse=True)
        return population[0]  # return the best schedule

    def print_schedule(self, schedule):
        for group_index, group in enumerate(schedule):
            print(f"Group: {self.groups[group_index].name}")
            for day_index, day in enumerate(group):
                print(f"Day {day_index + 1}:")
                for slot_index, slot in enumerate(day):
                    if slot[0] is not None:
                        print(f"Slot {slot_index + 1}: Teacher - {slot[0].name}, Subject - {slot[1]}, Room - {slot[2].name}")
                    else:
                        print(f"Slot {slot_index + 1}: Free")
                print()
            print()
