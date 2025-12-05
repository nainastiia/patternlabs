from .base import ReactionStrategy

class WaveReaction(ReactionStrategy):
    def react(self, mission, reading):
        if reading["data"]["height"] > mission.config.get("thresholds", {}).get("max_wave", 2):
            mission.request_fail_safe("reroute", reading)
            return True
        return False
