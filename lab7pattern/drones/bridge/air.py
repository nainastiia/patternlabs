from .base import MovementImplementor

class AirPlatform(MovementImplementor):
    def takeoff(self): print("[AIR] takeoff")
    def land(self): print("[AIR] land")
    def move_to(self, coord): print(f"[AIR] moving to {coord}")
    def adjust_course(self, vector): print(f"[AIR] adjust {vector}")
    def hold_position(self): print("[AIR] hold")
    def set_mode(self, mode): print(f"[AIR] mode {mode}")
    def broadcast(self, message): print(f"[AIR] broadcast: {message}")
