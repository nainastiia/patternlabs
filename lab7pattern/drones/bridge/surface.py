from .base import MovementImplementor

class SurfacePlatform(MovementImplementor):
    def takeoff(self): print("[GROUND] start")
    def land(self): print("[GROUND] stop")
    def move_to(self, coord): print(f"[GROUND] driving to {coord}")
    def adjust_course(self, vector): print(f"[GROUND] adjust {vector}")
    def hold_position(self): print("[GROUND] idle")
    def set_mode(self, mode): print(f"[GROUND] mode {mode}")
    def broadcast(self, message): print(f"[GROUND] broadcast: {message}")
