from .base import MovementImplementor

class SeaPlatform(MovementImplementor):
    def takeoff(self): print("[SEA] start")
    def land(self): print("[SEA] stop")
    def move_to(self, coord): print(f"[SEA] sailing to {coord}")
    def adjust_course(self, vector): print(f"[SEA] adjust {vector}")
    def hold_position(self): print("[SEA] anchor")
    def set_mode(self, mode): print(f"[SEA] mode {mode}")
    def broadcast(self, message): print(f"[SEA] broadcast: {message}")
