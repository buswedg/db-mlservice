import inspect

from django.test import TestCase

from apps.ml.deployments.income_classifier.et_classifier import ETClassifier
from apps.ml.deployments.income_classifier.rf_classifier import RFClassifier
from apps.ml.registry import MLRegistry


class MLTests(TestCase):
    def test_rf_algorithm(self):
        input_data = {
            'age': 37,
            'workclass': 'Private',
            'fnlwgt': 34146,
            'education': 'HS-grad',
            'education-num': 9,
            'marital-status': 'Married-civ-spouse',
            'occupation': 'Craft-repair',
            'relationship': 'Husband',
            'race': 'White',
            'sex': 'Male',
            'capital-gain': 0,
            'capital-loss': 0,
            'hours-per-week': 68,
            'native-country': 'United-States'
        }

        my_alg = RFClassifier()

        response = my_alg.compute_prediction(input_data)
        self.assertEqual('OK', response['status'])
        self.assertTrue('label' in response)
        self.assertEqual('<=50K', response['label'])

    def test_et_algorithm(self):
        input_data = {
            'age': 37,
            'workclass': 'Private',
            'fnlwgt': 34146,
            'education': 'HS-grad',
            'education-num': 9,
            'marital-status': 'Married-civ-spouse',
            'occupation': 'Craft-repair',
            'relationship': 'Husband',
            'race': 'White',
            'sex': 'Male',
            'capital-gain': 0,
            'capital-loss': 0,
            'hours-per-week': 68,
            'native-country': 'United-States'
        }
        my_alg = ETClassifier()

        response = my_alg.compute_prediction(input_data)
        self.assertEqual('OK', response['status'])
        self.assertTrue('label' in response)
        self.assertEqual('<=50K', response['label'])

    def test_registry(self):
        registry = MLRegistry()
        self.assertEqual(len(registry.endpoints), 0)

        endpoint_name = "income_classifier"
        algorithm_object = RFClassifier()
        algorithm_name = "random forest"
        algorithm_status = "production"
        algorithm_version = "0.0.1"
        algorithm_owner = "Piotr"
        algorithm_description = "Random Forest with simple pre- and post-processing"
        algorithm_code = inspect.getsource(RFClassifier)

        registry.add_algorithm(endpoint_name, algorithm_object, algorithm_name,
                               algorithm_status, algorithm_version, algorithm_owner,
                               algorithm_description, algorithm_code)

        self.assertEqual(len(registry.endpoints), 1)
