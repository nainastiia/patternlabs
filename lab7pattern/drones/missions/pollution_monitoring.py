from ..template.base import DroneMission

class PollutionMonitoring(DroneMission):
    def perform_payload_action(self):
        print("Monitoring pollution levels...")
