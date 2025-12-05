from fastapi import APIRouter
from ..factory.mission_factory import MissionFactory

router = APIRouter()
factory = MissionFactory()#екземпляр фабрики місій

@router.post("/mission/run")
def run_mission(cfg: dict):
    mission = factory.create_from_dict(cfg)
    result = mission.execute_mission()
    return {"mission_id": cfg["mission_id"], "result": result}

@router.get("/mission/status/{mid}")
def status(mid: str):
    return {"mission_id": mid, "status": "completed"}

@router.get("/mission/result/{mid}")
def result(mid: str):
    return {"mission_id": mid, "result": "OK"}
