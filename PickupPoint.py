class PickupPoint:
    _id = 0
    def __init__(self,name,address):
        self.id = PickupPoint._id
        self.name = name
        self.address = address
        PickupPoint._id += 1