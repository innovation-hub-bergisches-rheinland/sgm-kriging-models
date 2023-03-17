from pydantic import BaseModel


class MaxWarpageOutput(BaseModel):
    max_warpage: float


class CycleTimeOutput(BaseModel):
    cycle_time: float


class AvgShrinkageOutput(BaseModel):
    avg_shrinkage: float
