import inspect

from apps.ml.deployments.income_classifier.et_classifier import ETClassifier
from apps.ml.deployments.income_classifier.rf_classifier import RFClassifier
from apps.ml.registry import MLRegistry


try:
    registry = MLRegistry()

    rf = RFClassifier()
    registry.add_algorithm(
        endpoint_name='income_classifier',
        algorithm_object=rf,
        algorithm_name='random forest',
        algorithm_status='production',
        algorithm_version='0.1',
        owner='buswedg',
        algorithm_description='Random Forest with simple pre- and post-processing.',
        algorithm_code=inspect.getsource(RFClassifier)
    )

    et = ETClassifier()
    registry.add_algorithm(
        endpoint_name='income_classifier',
        algorithm_object=et,
        algorithm_name='extra trees',
        algorithm_status='testing',
        algorithm_version='0.1',
        owner='buswedg',
        algorithm_description='Extra Trees with simple pre- and post-processing.',
        algorithm_code=inspect.getsource(ETClassifier)
    )

    print('Successfully loaded all algorithms to the registry')

except Exception as e:
    print('Exception while loading the algorithms to the registry:', str(e))
