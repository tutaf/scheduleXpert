class Teacher:
    def __init__(self, name, availability, subjects):
        self.name = name
        self.availability = availability  # assuming this is a 5x5 2D list
        self.subjects = subjects

    def display_availability(self):
        for i in range(len(self.availability)):
            day = self.availability[i]
            print("Day:", i)
            print("Slots:", self.availability[i])
            print()

    def add_slot(self, day, slot):
        for d in self.availability:
            if d[0] == day:
                d.append(slot)
                break

    def remove_slot(self, day, slot):
        for d in self.availability:
            if d[0] == day and slot in d:
                d.remove(slot)
                break

    def add_subject(self, subject):
        self.subjects.append(subject)

    def remove_subject(self, subject):
        if subject in self.subjects:
            self.subjects.remove(subject)

    def edit_name(self, new_name):
        self.name = new_name
        print("Name updated successfully!")

    def display_info(self):
        print(f"Teacher: {self.name}, subjects {self.subjects}") # TODO: add other info
        # self.display_availability()
        print("\n")


class Group:
    def __init__(self, name, size):
        self.name = name
        self.size = size


class Room:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity

