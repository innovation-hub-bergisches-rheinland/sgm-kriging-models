import logging
import models.PredictionInput as PredictionInput
import models.PredictionOutput as PredictionOutput
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.ParameterInput import ParameterInput
from models.TargetFunctions import TargetFunctions
from models.TrainModel import RawData
from ModelPredictionService import ModelPredictionService, ModelPredictionServiceOut


app = FastAPI()
model_prediction_service = ModelPredictionService()
logging.basicConfig(level=logging.INFO)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/train-model", response_model=ModelPredictionServiceOut)
async def train_model(x: RawData):
    model_prediction_service.train(x.dict())
    return model_prediction_service.get_model_prediction_service_out()


@app.get("/api/training-status", response_model=ModelPredictionServiceOut)
async def training_status():
    return model_prediction_service.get_model_prediction_service_out()


@app.post("/api/predict-all", response_model=TargetFunctions)
async def predict_all(x: ParameterInput):
    return model_prediction_service.predict_all(x)


@app.post("/api/predict-cycle-time", response_model=PredictionOutput.CycleTimeOutput)
async def predict_cycle_time(x: PredictionInput.CycleTimeInput):
    return model_prediction_service.cycle_time_prediction(x)


@app.post("/api/predict-avg-volume-shrinkage", response_model=PredictionOutput.AvgVolumeShrinkageOutput)
async def predict_avg_volume_shrinkage(x: PredictionInput.AvgVolumeShrinkageInput):
    return model_prediction_service.avg_volume_shrinkage_prediction(x)


@app.post("/api/predict-max-warpage", response_model=PredictionOutput.MaxWarpageOutput)
async def predict_max_warpage(x: PredictionInput.MaxWarpageInput):
    return model_prediction_service.max_warpage_prediction(x)
