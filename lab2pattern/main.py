import json
from models import BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer
from ship import Ship
from port import Port

def main():
    # 1. Читаємо JSON
    with open("input.json") as f:
        data = json.load(f)

    ports = {}
    ships = {}
    containers = {}

    # 2. Створюємо порти
    for p in data["ports"]:
        port = Port(p["ID"], p["latitude"], p["longitude"])
        ports[p["ID"]] = port

    # 3. Створюємо кораблі
    for s in data["ships"]:
        port = ports[s["currentPort"]]
        ship = Ship(
            s["ID"], port,
            total_weight_capacity=s["totalWeightCapacity"],
            max_all=s["maxAll"],
            max_heavy=s["maxHeavy"],
            max_refrigerated=s["maxRefrigerated"],
            max_liquid=s["maxLiquid"],
            fuel_consumption_per_km=s["fuelConsumptionPerKM"]
        )
        ships[s["ID"]] = ship
        port.incoming_ship(ship)

    # 4. Створюємо контейнери
    for c in data["containers"]:
        if "type" not in c:
            if c["weight"] > 3000:
                cont = HeavyContainer(c["ID"], c["weight"])
            else:
                cont = BasicContainer(c["ID"], c["weight"])
        elif c["type"] == "R":
            cont = RefrigeratedContainer(c["ID"], c["weight"])
        elif c["type"] == "L":
            cont = LiquidContainer(c["ID"], c["weight"])
        else:
            raise ValueError(f"Невідомий тип контейнера: {c['type']}")

        containers[c["ID"]] = cont
        # кладемо контейнери у перший порт
        list(ports.values())[1].containers.append(cont)

    # 5. Виконуємо дії
    for action in data["actions"]:
        if action["action"] == "load":
            ship = ships[action["shipID"]]
            cont = containers[action["containerID"]]
            ship.load(cont)
        elif action["action"] == "unload":
            ship = ships[action["shipID"]]
            ship.unload(action["containerID"])
        elif action["action"] == "refuel":
            ship = ships[action["shipID"]]
            ship.re_fuel(action["fuel"])
        elif action["action"] == "sail":
            ship = ships[action["shipID"]]
            dest_port = ports[action["destPortID"]]
            ship.sail_to(dest_port)

    # 6. Формуємо результат
    result = {}
    for port_id, port in ports.items():
        result[f"Port {port.id_}"] = {
            "lat": round(port.latitude, 2),
            "lon": round(port.longitude, 2),
            "basic_container": [c.id_ for c in port.containers if isinstance(c, BasicContainer)],
            "heavy_container": [c.id_ for c in port.containers if isinstance(c, HeavyContainer) and not isinstance(c, (RefrigeratedContainer, LiquidContainer))],
            "refrigerated_container": [c.id_ for c in port.containers if isinstance(c, RefrigeratedContainer)],
            "liquid_container": [c.id_ for c in port.containers if isinstance(c, LiquidContainer)],
            "ships": {
                f"ship {s.id_}": {
                    "fuel_left": round(s.fuel, 2),
                    "basic_container": [c.id_ for c in s.containers if isinstance(c, BasicContainer)],
                    "heavy_container": [c.id_ for c in s.containers if isinstance(c, HeavyContainer) and not isinstance(c, (RefrigeratedContainer, LiquidContainer))],
                    "refrigerated_container": [c.id_ for c in s.containers if isinstance(c, RefrigeratedContainer)],
                    "liquid_container": [c.id_ for c in s.containers if isinstance(c, LiquidContainer)]
                }
                for s in port.current
            }
        }

    # 7. Записуємо у файл
    with open("output.json", "w") as f:
        json.dump(result, f, indent=2)


if __name__ == "__main__":
    main()
