from pydantic import BaseModel


class MaxWarpageOutput(BaseModel):
    max_warpage: float


class CycleTimeOutput(BaseModel):
    cycle_time: float


class AvgVolumeShrinkageOutput(BaseModel):
    avg_volume_shrinkage: float
