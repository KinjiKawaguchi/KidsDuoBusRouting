class Student:
    def __init__(self, name, address, dismissal_time):
        self.name = name
        self.address = address
        self.dismissal_time = dismissal_time

    def get_name(self):
        return self.name

    def get_address(self):
        return self.address

    def get_dismissal_time(self):
        return self.dismissal_time

    def set_address(self, new_address):
        self.address = new_address

    def set_dismissal_time(self, new_dismissal_time):
        self.dismissal_time = new_dismissal_time