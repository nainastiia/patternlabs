from .base import FailSafeHandler
#обробляє найбільш критичну проблему — аварійну посадку
class EmergencyLandHandler(FailSafeHandler):
    def handle(self, mission, issue):
        if issue["type"] == "emergency":
            mission.controller.impl.land()
            print("EMERGENCY LANDING")
            return True
        return super().handle(mission, issue)
