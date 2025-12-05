from ..template.base import DroneMission

class DefectsDetection(DroneMission):
    def perform_payload_action(self):
        print("Detecting cracks...")
