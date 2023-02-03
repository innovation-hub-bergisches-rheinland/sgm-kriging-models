import unittest
import rpy2
import src.ModelPredictionService as mps
import src.models.ParameterInput as pi
import src.models.TargetFunctions as tf
import numpy as np

class TestModelPredictionService(unittest.TestCase):
    
    rpy2.robjects.r['options'](warn=-1)
    example_input = pi.ParameterInput(clamping_force=100, closing_force=10, closing_speed=150, cooling_time=58, cylinder_temperature=214, dosing_speed=10, holding_pressure=226, holding_pressure_time=6, injection_volume_flow=10, lead_temperature=20, opening_speed=150)
    model_predictions = mps.ModelPredictionService('test/data/Versuchsdaten_v01_complete.CSV')
    
    def test_model_prediction(self):
        self.assertIsInstance(self.model_predictions, mps.ModelPredictionService)
        
    def test_predict_all(self):
        response:tf.TargetFunctions = self.model_predictions.predict_all(self.example_input)
        self.assertEqual(response, tf.TargetFunctions(cycle_time=77.39477510571808, avg_volume_shrinkage=13.663473795309102, max_warpage=0.6353053701601542))
        
    def test_predict_cycle_time(self):
        response = self.model_predictions.cycle_time_prediction(self.example_input)
        self.assertEqual(response, np.array([77.39477510571808]))
        
        
if __name__ == '__main__':
    unittest.main()