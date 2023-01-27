import numpy as np
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from models.ParameterInput import ParameterInput
from models.TargetFunctions import TargetFunctions
from models.PredictionOutput import CycleTimeOutput
from models.PredictionOutput import AvgVolumeShrinkageOutput
from models.PredictionOutput import MaxWarpageOutput
from models.PredictionInput import CycleTimeInput
from models.PredictionInput import AvgVolumeShrinkageInput
from models.PredictionInput import MaxWarpageInput


class ModelPredictionService:

    def __init__(self, filename) -> None:
        r = robjects.r
        source_kriging_r = "./src/Rscripts/kriging.R"
        r.source(source_kriging_r)
        utils = importr('utils')

        # enable r data.frame to pandas and numpy array conversion
        pandas2ri.activate()
        trainingdata = utils.read_csv(file=filename, header=True, sep=";", dec='.')
        trainCycleTime = robjects.r["trainCycleTime"]
        self.modelCycleTime = trainCycleTime(trainingdata)
        trainAvgVolumeShrinkage = robjects.r["trainAvgVolumeShrinkage"]
        self.modelAvgVolumeShrinkage = trainAvgVolumeShrinkage(trainingdata)
        trainMaxWarpage = robjects.r["trainMaxWarpage"]
        self.modelMaxWarpage = trainMaxWarpage(trainingdata)
        pandas2ri.deactivate

        self.modelPrediction = robjects.r["modelPrediction"]

    def predictAll(self, x: ParameterInput) -> TargetFunctions:
        cycleTimeInput = CycleTimeInput(
            cooling_time=x.cooling_time,
            holding_pressure_time=x.holding_pressure_time)
        avgVolumeShrinkageInput = AvgVolumeShrinkageInput(
            holding_pressure_time=x.holding_pressure_time,
            cylinder_temperature=x.cylinder_temperature)
        maxWarpageInput = MaxWarpageInput(
            cooling_time=x.cooling_time,
            cylinder_temperature=x.cylinder_temperature,
            holding_pressure_time=x.holding_pressure_time)

        return TargetFunctions(
            cycle_time=self.cycleTimePrediction(cycleTimeInput),
            avg_volume_shrinkage=self.avgVolumeShrinkagePrediction(
                avgVolumeShrinkageInput),
            max_warpage=self.maxWarpagePrediction(maxWarpageInput)
        )

    def cycleTimePrediction(self, vec: CycleTimeInput) -> CycleTimeOutput:
        """
        x1: cooling_time
        x2: holding_pressure_time
        """
        x = np.array([vec.cooling_time, vec.holding_pressure_time])
        return self._eval(self.modelCycleTime, x)

    def avgVolumeShrinkagePrediction(self,
                                     vec: AvgVolumeShrinkageInput) \
            -> AvgVolumeShrinkageOutput:
        """
        x1: holding_pressure_time
        x2: cylinder_temperature
        """
        x = np.array([vec.holding_pressure_time, vec.cylinder_temperature])
        return self._eval(self.modelAvgVolumeShrinkage, x)

    def maxWarpagePrediction(self, vec: MaxWarpageInput) -> MaxWarpageOutput:
        """
        x1: cooling_time
        x2: cylinder_temperature
        x3: holding_pressure_time
        """
        x = np.array([vec.cooling_time, vec.cylinder_temperature,
                     vec.holding_pressure_time])
        return self._eval(self.modelMaxWarpage, x)

    def _eval(self, model, x: list) -> float:
        pandas2ri.activate()
        yEst = self.modelPrediction(model, np.array(x))
        pandas2ri.deactivate()
        return yEst
