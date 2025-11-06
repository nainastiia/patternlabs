import math

class Port:
    def __init__(self, id_: int, latitude: float, longitude: float):
        self.id_ = id_
        self.latitude = latitude
        self.longitude = longitude
        self.containers = []
        self.history = []
        self.current = []

    def incoming_ship(self, ship):
        if ship not in self.current:
            self.current.append(ship)

    def outgoing_ship(self, ship):
        if ship not in self.history:
            self.history.append(ship)
        if ship in self.current:
            self.current.remove(ship)

    def get_distance(self, other) -> float:
        # формула гаверсину
        r: int = 6371  # км
        lat1 = math.radians(self.latitude)
        lon1 = math.radians(self.longitude)
        lat2 = math.radians(other.latitude)
        lon2 = math.radians(other.longitude)

        dlat: float = lat2 - lat1
        dlon: float = lon2 - lon1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return r * c
