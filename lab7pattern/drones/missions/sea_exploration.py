from ..template.base import DroneMission

class SeaExploration(DroneMission):
    def perform_payload_action(self):
        print("Scanning sea floor...")
