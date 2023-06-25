from apps.endpoints.models import Endpoint, MLAlgorithm, MLAlgorithmStatus


class MLRegistry:
    def __init__(self):
        self.endpoints = {}

    def add_algorithm(self, endpoint_name, algorithm_object, algorithm_name,
                      algorithm_status, algorithm_version, owner,
                      algorithm_description, algorithm_code):

        endpoint, _ = Endpoint.objects.get_or_create(name=endpoint_name, owner=owner)

        ml_algorithm, created = MLAlgorithm.objects.get_or_create(
            name=algorithm_name,
            description=algorithm_description,
            code=algorithm_code,
            version=algorithm_version,
            owner=owner,
            parent_endpoint=endpoint
        )

        if created:
            status = MLAlgorithmStatus(
                status=algorithm_status,
                created_by=owner,
                parent_mlalgorithm=ml_algorithm,
                active=True
            )
            status.save()

        self.endpoints[ml_algorithm.id] = algorithm_object
