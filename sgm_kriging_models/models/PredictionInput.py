from pydantic import BaseModel


class ModelInput(BaseModel):
    cooling_time: float
    cylinder_temperature: float
    holding_pressure_time: float
    injection_volume_flow: float

class MaxWarpageInput(ModelInput):
    pass


class AvgShrinkageInput(ModelInput):
    pass


class CycleTimeInput(ModelInput):
    pass
