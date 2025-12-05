from ..bridge.controller import DroneController
from ..bridge.air import AirPlatform
from ..bridge.sea import SeaPlatform
from ..bridge.surface import SurfacePlatform

from ..environment.air_env import AirEnvironment
from ..environment.sea_env import SeaEnvironment
from ..environment.surface_env import SurfaceEnvironment

from ..strategy.wave_reaction import WaveReaction
from ..strategy.wind_reaction import WindReaction
from ..strategy.crack_reaction import CrackReaction

from ..missions.sea_exploration import SeaExploration
from ..missions.agriculture import Agriculture
from ..missions.defects_detection import DefectsDetection
from ..missions.rescue import Rescue
from ..missions.pollution_monitoring import PollutionMonitoring

from ..observer.event_bus import EventBus
from ..cor.reroute_handler import ReRouteHandler
from ..cor.adjust_altitude_handler import AdjustAltitudeHandler
from ..cor.emergency_land_handler import EmergencyLandHandler

class MissionFactory:
    def create_from_dict(self, data):#створює об'єкт Місії зі словника конфігурації
        bus = EventBus()#Ініціалізує шину подій

        env_map = {
            "air": AirEnvironment,
            "sea": SeaEnvironment,
            "surface": SurfaceEnvironment
        }

        platform_map = {
            "air": AirPlatform,
            "sea": SeaPlatform,
            "surface": SurfacePlatform
        }

        mission_map = {
            "sea_exploration": SeaExploration,
            "agriculture": Agriculture,
            "defects_detection": DefectsDetection,
            "rescue": Rescue,
            "pollution_monitoring": PollutionMonitoring
        }

        strategy_map = {
            "air": WindReaction(),
            "sea": WaveReaction(),
            "surface": CrackReaction()
        }

        env = env_map[data["environment_type"]](bus)
        impl = platform_map[data["platform_type"]]()
        controller = DroneController(impl)

        chain = ReRouteHandler(
            AdjustAltitudeHandler(
                EmergencyLandHandler()
            )
        )

        mission = mission_map[data["mission_type"]](
            config=data,
            controller=controller,
            environment=env,
            strategy=strategy_map[data["environment_type"]],
            chain=chain
        )

        return mission
