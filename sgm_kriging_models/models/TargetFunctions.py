from pydantic import BaseModel


class TargetFunctions(BaseModel):
    cycle_time: float
    avg_shrinkage: float
    max_warpage: float
