from ..template.base import DroneMission

class Rescue(DroneMission):
    def perform_payload_action(self):
        print("Searching for survivors...")
