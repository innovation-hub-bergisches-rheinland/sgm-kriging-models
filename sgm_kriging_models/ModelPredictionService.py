import numpy as np
import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects import numpy2ri
from rpy2.robjects import pandas2ri
from models.ParameterInput import ParameterInput
from models.TargetFunctions import TargetFunctions
from models.PredictionOutput import CycleTimeOutput
from models.PredictionOutput import AvgVolumeShrinkageOutput
from models.PredictionOutput import MaxWarpageOutput
from models.PredictionInput import CycleTimeInput
from models.PredictionInput import AvgVolumeShrinkageInput
from models.PredictionInput import MaxWarpageInput
from pydantic import BaseModel



class ModelPredictionServiceOut(BaseModel):
    trained: bool

class ModelPredictionService:

    trained: bool = False

    def get_model_prediction_service_out(self)->ModelPredictionServiceOut:
        return ModelPredictionServiceOut(trained=self.trained)

    def train(self, raw_data: dict):
        r = robjects.r
        source_kriging_r = "./sgm_kriging_models/Rscripts/kriging.R"
        r.source(source_kriging_r)

        training_data = pd.DataFrame(raw_data)
        with robjects.default_converter + pandas2ri.converter:
            training_data = robjects.conversion.get_conversion().py2rpy(training_data)
        self.modelCycleTime = robjects.r["trainCycleTime"](training_data)
        self.modelAvgVolumeShrinkage = robjects.r["trainAvgVolumeShrinkage"](training_data)
        self.modelMaxWarpage = robjects.r["trainMaxWarpage"](training_data)
        # pandas2ri.deactivate

        self.modelPrediction = robjects.r["modelPrediction"]
        self.trained = True


    def predict_all(self, x: ParameterInput) -> TargetFunctions:
        cycle_time_input = CycleTimeInput(
            cooling_time=x.cooling_time,
            holding_pressure_time=x.holding_pressure_time)
        avg_volume_shrinkage_input = AvgVolumeShrinkageInput(
            holding_pressure_time=x.holding_pressure_time,
            cylinder_temperature=x.cylinder_temperature)
        max_warpage_input = MaxWarpageInput(
            cooling_time=x.cooling_time,
            cylinder_temperature=x.cylinder_temperature,
            holding_pressure_time=x.holding_pressure_time)

        return TargetFunctions(
            cycle_time=self.cycle_time_prediction(cycle_time_input).cycle_time,
            avg_volume_shrinkage=self.avg_volume_shrinkage_prediction(
                avg_volume_shrinkage_input).avg_volume_shrinkage,
            max_warpage=self.max_warpage_prediction(max_warpage_input).max_warpage
        )

    def cycle_time_prediction(self, vec: CycleTimeInput) -> CycleTimeOutput:
        """
        x1: cooling_time
        x2: holding_pressure_time
        """
        x = np.array([vec.cooling_time, vec.holding_pressure_time])
        return CycleTimeOutput(cycle_time=self._eval(self.modelCycleTime, x))

    def avg_volume_shrinkage_prediction(self,
                                        vec: AvgVolumeShrinkageInput) \
            -> AvgVolumeShrinkageOutput:
        """
        x1: holding_pressure_time
        x2: cylinder_temperature
        """
        x = np.array([vec.holding_pressure_time, vec.cylinder_temperature])
        return AvgVolumeShrinkageOutput(avg_volume_shrinkage=self._eval(self.modelAvgVolumeShrinkage, x))

    def max_warpage_prediction(self, vec: MaxWarpageInput) -> MaxWarpageOutput:
        """
        x1: cooling_time
        x2: cylinder_temperature
        x3: holding_pressure_time
        """
        x = np.array([vec.cooling_time, vec.cylinder_temperature,
                     vec.holding_pressure_time])
        return MaxWarpageOutput(max_warpage=self._eval(self.modelMaxWarpage, x))

    def _eval(self, model, x) -> float:
        with robjects.default_converter + numpy2ri.converter:
            y_est = self.modelPrediction(model,x)
        return y_est
