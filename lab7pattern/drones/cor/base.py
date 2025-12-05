class FailSafeHandler:
    def __init__(self, next_handler=None):
        self.next = next_handler

    def handle(self, mission, issue):#для обробки запиту (проблеми)
        if self.next:
            return self.next.handle(mission, issue)
        return False
