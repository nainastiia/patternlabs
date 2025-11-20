from .base import BaseActivity
from ...db.models import Activity

class Hiking(BaseActivity):
    def get_activity(self) -> Activity:
        return Activity(
            name="Hiking",
            type="outdoor",
            priority=4,
            time_slot="Morning"
        )