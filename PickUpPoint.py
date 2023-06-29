class PickUpPoint:
    _id = 0
    def __init__(self,name,address):
        self.id = PickUpPoint._id
        self.name = name
        self.address = address
        PickUpPoint._id += 1