from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

# --- Вхідні Моделі ---

class WorkingHours(BaseModel):#представлення робочих годин
    start: int = Field(..., ge=0, le=23, description="Start hour (0-23)")
    end: int = Field(..., ge=0, le=23, description="End hour (0-23)")

class UserPreferences(BaseModel):#уподобань користувача
    preferred_types: List[str] = Field(default=["outdoor", "productive"])
    avoid_types: List[str] = Field(default=["sport"])
    working_hours: Optional[WorkingHours] = None#Необов'язкове поле `WorkingHours`
    weekend_mode: bool = Field(default=False, description="If true, prioritizes relaxation/fun.")

# --- Моделі Системи та Плану ---

class Activity(BaseModel):#рекомендованої активності
    name: str
    type: str = Field(description="e.g., indoor, outdoor, productive, sport")
    priority: int = Field(default=1, ge=1, le=10, description="Higher means more recommended")
    time_slot: str = Field(default="Any") # E.g., "Morning", "Afternoon"

class WeatherData(BaseModel):#даних про погоду
    condition: str = Field(description="e.g., Sunny, Rainy, Cloudy, Snowy")
    temperature: float
    description: str
    location: str

class ActivityPlan(BaseModel):#фінального плану активностей
    date: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    location: str
    weather: WeatherData
    activities: List[Activity]
    user_id: str
    created_at: datetime = Field(default_factory=datetime.now)

# --- Допоміжна Модель для MongoDB ---
class UserPreferencesDB(BaseModel):#зберігання уподобань у MongoDB
    user_id: str
    preferences: UserPreferences