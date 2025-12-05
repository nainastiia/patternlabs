from ..template.base import DroneMission

class Agriculture(DroneMission):
    def perform_payload_action(self):
        print("Monitoring crops...")
