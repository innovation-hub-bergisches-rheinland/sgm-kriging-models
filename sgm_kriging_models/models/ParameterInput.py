from fastapi import Path
from pydantic import BaseModel


class ParameterInput(BaseModel):
    cylinder_temperature: float = Path(ge=200, le=240)
    holding_pressure_time: float = Path(ge=2, le=10)
    cooling_time: float = Path(ge=5, le=15)
    lead_temperature: float = Path(ge=20, le=50)
    holding_pressure: float = Path(ge=100, le=400)
    clamping_force: float = Path(ge=100, le=500)
    closing_force: float = Path(ge=10, le=30)
    closing_speed: float = Path(ge=150, le=750)
    opening_speed: float = Path(ge=150, le=750)
    injection_volume_flow: float = Path(ge=10, le=30)
    dosing_speed: float = Path(ge=10, le=50)
