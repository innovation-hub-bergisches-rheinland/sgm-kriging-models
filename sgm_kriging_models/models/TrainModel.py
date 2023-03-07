from pydantic import BaseModel
from typing import List


class RawData(BaseModel):
    avg_volume_shrinkage: List[float]
    cooling_time: List[float]
    cycle_time: List[float]
    cylinder_temperature: List[float]
    holding_pressure_time: List[float]
    max_warpage: List[float]
    
