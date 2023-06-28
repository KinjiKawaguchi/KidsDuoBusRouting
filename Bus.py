import Student

MAX = 10

class Bus:
    NODEID = 0
    def __init__(self, passengers=None):
        id = NODEID
        name = ''
        self.max_passenger = MAX
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = passengers
        NODEID += 1
    def pick(student):
        pass
    def drop(student):
        pass
    def is_empty(self):
        return not self.passengers
    def is_full(self):
        return len(self.passengers) >= self.MAX_PASSENGERS