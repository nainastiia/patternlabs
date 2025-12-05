from .base import FailSafeHandler
#обробляє проблему, пов'язану з переходом у ройовий режим або перепризначенням рою
class SwarmReassignHandler(FailSafeHandler):
    def handle(self, mission, issue):
        if issue["type"] == "swarm":
            mission.controller.set_swarm()
            return True
        return super().handle(mission, issue)
