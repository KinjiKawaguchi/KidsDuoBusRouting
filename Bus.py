import Student

MAX = 10

class Bus:
    _id = 0
    def __init__(self):
        self.id = Bus._id
        name = ''
        self.max_passenger = MAX
        self.passengers = []
        self.route = []
        Bus._id += 1

    def pick(student):
        pass
    def drop(student):
        pass
    def is_empty(self):
        return not self.passengers
    def is_full(self):
        return len(self.passengers) >= self.max_passenger