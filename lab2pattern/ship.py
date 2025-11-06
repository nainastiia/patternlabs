from models import Container, HeavyContainer, RefrigeratedContainer, LiquidContainer

class Ship:
    def __init__(self, id_: int, current_port, total_weight_capacity: int,
                 max_all: int, max_heavy: int, max_refrigerated: int,
                 max_liquid: int, fuel_consumption_per_km: float):
        self.id_ = id_
        self.fuel = 0.0
        self.current_port = current_port
        self.total_weight_capacity = total_weight_capacity
        self.max_all = max_all
        self.max_heavy = max_heavy
        self.max_refrigerated = max_refrigerated
        self.max_liquid = max_liquid
        self.fuel_consumption_per_km = fuel_consumption_per_km
        self.containers = []

    def get_current_containers(self):
        return sorted(self.containers, key=lambda c: c.id_)

    def re_fuel(self, new_fuel: float):
        self.fuel += new_fuel
        print(f"Ship {self.id_}: refueled by {new_fuel}, total fuel: {self.fuel:.2f}")

    def load(self, cont: Container) -> bool:
        # обмеження
        if len(self.containers) >= self.max_all:
            print(f"Ship {self.id_}: cannot load container {cont.id_}, max total containers reached")
            return False
        if sum(c.weight for c in self.containers) + cont.weight > self.total_weight_capacity:
            print(f"Ship {self.id_}: cannot load container {cont.id_}, weight limit exceeded")
            return False
        if isinstance(cont, HeavyContainer) and len([c for c in self.containers if isinstance(c, HeavyContainer)]) >= self.max_heavy:
            print(f"Ship {self.id_}: cannot load container {cont.id_}, max heavy containers reached")
            return False
        if isinstance(cont, RefrigeratedContainer) and len([c for c in self.containers if isinstance(c, RefrigeratedContainer)]) >= self.max_refrigerated:
            print(f"Ship {self.id_}: cannot load container {cont.id_}, max refrigerated containers reached")
            return False
        if isinstance(cont, LiquidContainer) and len([c for c in self.containers if isinstance(c, LiquidContainer)]) >= self.max_liquid:
            print(f"Ship {self.id_}: cannot load container {cont.id_}, max liquid containers reached")
            return False

        self.containers.append(cont)
        if cont in self.current_port.containers:
            self.current_port.containers.remove(cont)

        print(f"Ship {self.id_}: loaded container {cont.id_}")
        return True

    def unload(self, cont_id: int) -> bool:
        for idx, c in enumerate(self.containers):
            if c.id_ == cont_id:
                container = self.containers.pop(idx)
                self.current_port.containers.append(container)
                print(f"Ship {self.id_}: unloaded container {cont_id} to Port {self.current_port.id_}")
            else:
                print(f"Ship {self.id_}: cannot unload container {cont_id}, not on ship")
        if not self.containers:
            print(f"Ship {self.id_}: no containers left on board")
            return False
        return True

    def sail_to(self, dest_port) -> bool:
        distance = self.current_port.get_distance(dest_port)
        fuel_need = distance * (self.fuel_consumption_per_km + sum(c.consumption() for c in self.containers))

        print(f"Ship {self.id_}: attempting to sail from Port {self.current_port.id_} to Port {dest_port.id_}")
        print(f"Ship {self.id_}: distance = {distance:.2f}, fuel needed = {fuel_need:.2f}, current fuel = {self.fuel:.2f}")

        if self.fuel >= fuel_need:
            self.fuel -= fuel_need
            print(f"Ship {self.id_}: sailing... fuel left after journey = {self.fuel:.2f}")

            self.current_port.outgoing_ship(self)
            self.current_port = dest_port
            self.current_port.incoming_ship(self)

            print(f"Ship {self.id_}: arrived at Port {dest_port.id_}")
            return True
        else:
            print(f"Ship {self.id_}: Not enough fuel to sail to Port {dest_port.id_}")
            return False

