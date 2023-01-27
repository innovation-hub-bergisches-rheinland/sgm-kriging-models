from pydantic import BaseModel


class MaxWarpageInput(BaseModel):
    cylinder_temperature: float
    holding_pressure_time: float
    cooling_time: float


class AvgVolumeShrinkageInput(BaseModel):
    cylinder_temperature: float
    holding_pressure_time: float


class CycleTimeInput(BaseModel):
    cooling_time: float
    holding_pressure_time: float
