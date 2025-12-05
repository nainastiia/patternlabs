from .base import ReactionStrategy

class WindReaction(ReactionStrategy):
    def react(self, mission, reading):
        if reading["data"]["speed"] > 15:
            mission.request_fail_safe("adjust_altitude", reading)
            return True
        return False
