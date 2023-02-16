import unittest
import rpy2
import src.ModelPredictionService as mps
import src.models.ParameterInput as pi
import src.models.PredictionInput as ppi
import src.models.PredictionOutput as ppo
import src.models.TargetFunctions as tf
import src.main as api
import pandas as pd
from src.models.TrainModel import RawData

class TestModelPredictionService(unittest.TestCase):
    
    rpy2.robjects.r['options'](warn=-1)
    example_input = pi.ParameterInput(clamping_force=100, closing_force=10, closing_speed=150, cooling_time=58, cylinder_temperature=214, dosing_speed=10, holding_pressure=226, holding_pressure_time=6, injection_volume_flow=10, lead_temperature=20, opening_speed=150)
    raw_data = pd.read_csv('test/data/Versuchsdaten_v01_complete.CSV', sep=';', decimal='.').to_dict('list')
    model_predictions = mps.ModelPredictionService()
    
    def test_model_prediction(self):
        self.assertFalse(self.model_predictions.trained)
        
    def test_model_prediction_train(self):
        self.model_predictions.train(self.raw_data)
        self.assertTrue(self.model_predictions.trained)
        
    def test_predict_all(self):
        response:tf.TargetFunctions = self.model_predictions.predict_all(self.example_input)
        self.assertEqual(response, tf.TargetFunctions(cycle_time=77.39477510571808, avg_volume_shrinkage=13.663473795309102, max_warpage=0.6353053701601542))
        
    def test_predict_cycle_time(self):
        cycle_time_input = ppi.CycleTimeInput(cooling_time=self.example_input.cooling_time, holding_pressure_time=self.example_input.holding_pressure_time)
        response = self.model_predictions.cycle_time_prediction(cycle_time_input)
        self.assertEqual(response, ppo.CycleTimeOutput(cycle_time=77.39477510571808))
        
        
class TestRESTAPI(unittest.IsolatedAsyncioTestCase):
    rpy2.robjects.r['options'](warn=-1)
    example_input = pi.ParameterInput(clamping_force=100, closing_force=10, closing_speed=150, cooling_time=58, cylinder_temperature=214, dosing_speed=10, holding_pressure=226, holding_pressure_time=6, injection_volume_flow=10, lead_temperature=20, opening_speed=150)
    raw_data = pd.read_csv('test/data/Versuchsdaten_v01_complete.CSV', sep=';', decimal='.').to_dict('list')
    
    async def test_train_model(self):
        self.assertEqual(
            await api.train_model(
                RawData(
                    avg_volume_shrinkage=self.raw_data['avg_volume_shrinkage'],
                    cooling_time=self.raw_data['cooling_time'],
                    cycle_time=self.raw_data['cycle_time'],
                    cylinder_temperature=self.raw_data['cylinder_temperature'],
                    holding_pressure_time=self.raw_data['holding_pressure_time'],
                    max_warpage=self.raw_data['max_warpage']
                )),
            mps.ModelPredictionServiceOut(trained=True))
        
    async def test_predict_all(self):
        await api.train_model(
                RawData(
                    avg_volume_shrinkage=self.raw_data['avg_volume_shrinkage'],
                    cooling_time=self.raw_data['cooling_time'],
                    cycle_time=self.raw_data['cycle_time'],
                    cylinder_temperature=self.raw_data['cylinder_temperature'],
                    holding_pressure_time=self.raw_data['holding_pressure_time'],
                    max_warpage=self.raw_data['max_warpage']
                ))
        self.assertEqual(
            await api.predict_all(self.example_input),
            tf.TargetFunctions(cycle_time=77.39477510571808, avg_volume_shrinkage=13.663473795309102, max_warpage=0.6353053701601542))
        
    async def test_predict_max_warpage(self):
        await api.train_model(
                RawData(
                    avg_volume_shrinkage=self.raw_data['avg_volume_shrinkage'],
                    cooling_time=self.raw_data['cooling_time'],
                    cycle_time=self.raw_data['cycle_time'],
                    cylinder_temperature=self.raw_data['cylinder_temperature'],
                    holding_pressure_time=self.raw_data['holding_pressure_time'],
                    max_warpage=self.raw_data['max_warpage']
                ))
        self.assertEqual(
            await api.predict_max_warpage(
                ppi.MaxWarpageInput(
                    cylinder_temperature=self.example_input.cylinder_temperature,
                    holding_pressure_time=self.example_input.holding_pressure_time,
                    cooling_time=self.example_input.cooling_time)),
            ppo.MaxWarpageOutput(max_warpage=0.6353053701601542))
        
        
if __name__ == '__main__':
    unittest.main()