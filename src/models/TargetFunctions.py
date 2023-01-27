from pydantic import BaseModel


class TargetFunctions(BaseModel):
    cycle_time: float
    avg_volume_shrinkage: float
    max_warpage: float
