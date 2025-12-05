from abc import ABC, abstractmethod

class DroneMission(ABC):
    def __init__(self, config, controller, environment, strategy, chain):
        self.config = config
        self.controller = controller
        self.environment = environment
        self.strategy = strategy
        self.chain = chain
        self.navigate_to_area()
        self.environment.subscribe(self._on_event)

    def execute_mission(self):
        self.load_config()
        self.setup_event_subscriptions()
        self.analyze_environment()
        self.perform_payload_action()
        self.collect_and_store_data()
        self.return_to_base()
        self.postprocess_results()

        return {"status": "DONE"}

    def _on_event(self, event):
        if self.strategy:
            self.strategy.react(self, event)

    def request_fail_safe(self, issue_type, data):
        self.chain.handle(self, {"type": issue_type, "data": data})

    def load_config(self): pass
    def setup_event_subscriptions(self): pass
    def analyze_environment(self): pass
    def preflight_check(self): pass

    def analyze_environment(self):
        # ДОДАТИ ЦЕЙ РЯДОК:
        self.environment.start()
        pass

    def navigate_to_area(self):
        self.controller.impl.takeoff()
        self.controller.goto(self.config['target_area'])

    @abstractmethod
    def perform_payload_action(self): ...

    def collect_and_store_data(self): pass

    def return_to_base(self):
        self.controller.goto(self.config['base_area'])  # <- словниковий доступ
        self.controller.impl.land()

    def postprocess_results(self): pass
