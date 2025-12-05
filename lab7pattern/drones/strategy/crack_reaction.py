from .base import ReactionStrategy

class CrackReaction(ReactionStrategy):
    def react(self, mission, reading):
        if reading["data"]["count"] > 3:
            mission.request_fail_safe("emergency", reading)
            return True
        return False
