from .base import FailSafeHandler
#обробляє проблему, пов'язану з коригуванням висоти
class AdjustAltitudeHandler(FailSafeHandler):
    def handle(self, mission, issue):
        if issue["type"] == "adjust_altitude":
            mission.controller.adjust_course((0, 0, 1))
            print("Altitude adjusted")
            return True
        return super().handle(mission, issue)
