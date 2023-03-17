import numpy as np
import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects import numpy2ri
from rpy2.robjects import pandas2ri
from models.ParameterInput import ParameterInput
from models.TargetFunctions import TargetFunctions
from models.PredictionOutput import CycleTimeOutput
from models.PredictionOutput import AvgShrinkageOutput
from models.PredictionOutput import MaxWarpageOutput
from models.PredictionInput import AvgShrinkageInput
from models.PredictionInput import CycleTimeInput
from models.PredictionInput import MaxWarpageInput
from models.PredictionInput import ModelInput
from pydantic import BaseModel


class ModelPredictionServiceOut(BaseModel):
    trained: bool


class ModelPredictionService:

    trained: bool = False

    def get_model_prediction_service_out(self) -> ModelPredictionServiceOut:
        return ModelPredictionServiceOut(trained=self.trained)

    def train(self, raw_data: dict):
        r = robjects.r
        source_kriging_r = "./sgm_kriging_models/Rscripts/kriging.R"
        r.source(source_kriging_r)

        training_data = pd.DataFrame(raw_data)
        with pandas2ri.converter.context():
            training_data = robjects.conversion.get_conversion().py2rpy(training_data)
        self.modelCycleTime = robjects.r["trainCycleTime"](training_data)
        self.modelAvgShrinkage = robjects.r["trainAvgShrinkage"](
            training_data)
        self.modelMaxWarpage = robjects.r["trainMaxWarpage"](training_data)
        # pandas2ri.deactivate

        self.modelPrediction = robjects.r["modelPrediction"]
        self.trained = True

    def predict_all(self, x: ParameterInput) -> TargetFunctions:
        model_input = ModelInput(
            cooling_time=x.cooling_time,
            cylinder_temperature=x.cylinder_temperature,
            holding_pressure_time=x.holding_pressure_time,
            injection_volume_flow=x.injection_volume_flow)

        return TargetFunctions(
            cycle_time=self.cycle_time_prediction(model_input).cycle_time,
            avg_shrinkage=self.avg_shrinkage_prediction(
                model_input).avg_shrinkage,
            max_warpage=self.max_warpage_prediction(
                model_input).max_warpage
        )

    def cycle_time_prediction(self, vec: CycleTimeInput) -> CycleTimeOutput:
        """
        x1: cooling_time
        x2: holding_pressure_time
        """
        x = np.array([vec.cooling_time, vec.cylinder_temperature, vec.holding_pressure_time, vec.injection_volume_flow])
        return CycleTimeOutput(cycle_time=self._eval(self.modelCycleTime, x))

    def avg_shrinkage_prediction(self,
                                        vec: AvgShrinkageInput) \
            -> AvgShrinkageOutput:
        """
        x1: holding_pressure_time
        x2: cylinder_temperature
        """
        x = np.array([vec.cooling_time, vec.cylinder_temperature, vec.holding_pressure_time, vec.injection_volume_flow])
        return AvgShrinkageOutput(avg_shrinkage=self._eval(self.modelAvgShrinkage, x))

    def max_warpage_prediction(self, vec: MaxWarpageInput) -> MaxWarpageOutput:
        """
        x1: cooling_time
        x2: cylinder_temperature
        x3: holding_pressure_time
        """
        x = np.array([vec.cooling_time, vec.cylinder_temperature, vec.holding_pressure_time, vec.injection_volume_flow])
        return MaxWarpageOutput(max_warpage=self._eval(self.modelMaxWarpage, x))

    def _eval(self, model, x) -> float:
        with numpy2ri.converter.context():
            y_est = self.modelPrediction(model, x)
        return y_est
