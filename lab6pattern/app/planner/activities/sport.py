from .base import BaseActivity
from ...db.models import Activity

class Sport(BaseActivity):
    def get_activity(self) -> Activity:
        return Activity(
            name="Indoor Sport",
            type="sport",
            priority=4,
            time_slot="Evening"
        )