from .base import BaseActivity
from ...db.models import Activity

class Studying(BaseActivity):
    def get_activity(self) -> Activity:
        return Activity(
            name="Studying",
            type="productive",
            priority=5,
            time_slot="Any"
        )