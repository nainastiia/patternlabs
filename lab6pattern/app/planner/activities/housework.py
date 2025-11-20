from .base import BaseActivity
from ...db.models import Activity

class Housework(BaseActivity):
    def get_activity(self) -> Activity:
        return Activity(
            name="HouseWork",
            type="indoor",
            priority=3,
            time_slot="Morning"
        )