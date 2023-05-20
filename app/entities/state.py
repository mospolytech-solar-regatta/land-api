import json
from datetime import datetime

from pydantic import BaseModel

from app import constants
from app.LandAPI.context import AppContext
from app.models.state import State as StateModel


class State(BaseModel):
    created_at: datetime
    controller_watts: int
    time_to_go: int
    controller_volts: float
    MPPT_volts: float
    MPPT_watts: float
    motor_temp: float
    motor_revols: float
    position_lat: float
    position_lng: float
    speed: float = 0
    distance_travelled: float = 0
    laps: int = 0
    lap_point_lat: float = None
    lap_point_lng: float = None
    lap_id: int = None

    class Config:
        orm_mode = True

    @staticmethod
    async def get_current_state(ctx: AppContext):
        cur = await ctx.redis.get(constants.CURRENT_STATE_KEY)
        if cur is None:
            raise FileNotFoundError("Key not found")
        return State(**json.loads(cur))

    async def save(self, ctx: AppContext):
        StateModel.save_from_schema(self, ctx)
