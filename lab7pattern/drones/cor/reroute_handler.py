from .base import FailSafeHandler
#обробляє проблему, пов'язану зі зміною маршруту
class ReRouteHandler(FailSafeHandler):
    def handle(self, mission, issue):
        if issue["type"] == "reroute":
            mission.controller.hold_position()
            print("Rerouting...")
            return True
        return super().handle(mission, issue)
