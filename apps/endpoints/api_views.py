import datetime
import json

from django.db import transaction
from django.db.models import F, Q
from numpy.random import rand
from rest_framework import views, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.generics import ListAPIView
from apps.endpoints.models import ABTest, Endpoint, MLAlgorithm, MLAlgorithmStatus, MLAlgorithmRequest
from apps.endpoints.serializers import ABTestSerializer, EndpointSerializer, MLAlgorithmSerializer, \
    MLAlgorithmRequestSerializer, MLAlgorithmStatusSerializer
from apps.ml.registration import registry


def deactivate_other_statuses(instance):
    old_statuses = MLAlgorithmStatus.objects.filter(
        parent_mlalgorithm=instance.parent_mlalgorithm,
        created_at__lt=instance.created_at,
        active=True
    )

    for i in range(len(old_statuses)):
        old_statuses[i].active = False

    MLAlgorithmStatus.objects.bulk_update(old_statuses, ['active'])


class BaseListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    queryset = None

    def get_queryset(self):
        query_params = self.request.query_params
        filter_kwargs = {param: value for param, value in query_params.items()}
        return self.queryset.filter(**filter_kwargs)


class EndpointAPIView(BaseListAPIView):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointSerializer


class MLAlgorithmAPIView(BaseListAPIView):
    queryset = MLAlgorithm.objects.all()
    serializer_class = MLAlgorithmSerializer


class MLAlgorithmRequestAPIView(BaseListAPIView):
    queryset = MLAlgorithmRequest.objects.all()
    serializer_class = MLAlgorithmRequestSerializer


class MLAlgorithmStatusAPIView(BaseListAPIView):
    queryset = MLAlgorithmStatus.objects.all()
    serializer_class = MLAlgorithmStatusSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    instance = serializer.save(active=True)
                    deactivate_other_statuses(instance)
            except Exception as e:
                raise APIException(str(e))

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PredictAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request, endpoint_name, format=None):
        algorithm_status = request.query_params.get('status', 'production')
        algorithm_version = request.query_params.get('version')

        algs = MLAlgorithm.objects.filter(
            parent_endpoint__name=endpoint_name,
            ml_algorithm_status__status=algorithm_status,
            ml_algorithm_status__active=True
        )

        if algorithm_version is not None:
            algs = algs.filter(version=algorithm_version)

        if len(algs) == 0:
            return Response(
                {'status': 'Error', 'message': 'ML algorithm is not available'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(algs) != 1 and algorithm_status != "ab_testing":
            return Response(
                {'status': 'Error',
                 'message': 'ML algorithm selection is ambiguous. Please specify algorithm version.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        alg_index = 0
        if algorithm_status == "ab_testing":
            alg_index = 0 if rand() < 0.5 else 1

        algorithm_object = registry.endpoints[algs[alg_index].id]
        prediction = algorithm_object.compute_prediction(request.data)

        label = prediction['label'] if "label" in prediction else "error"
        ml_request = MLAlgorithmRequest(
            input_data=json.dumps(request.data),
            full_response=prediction,
            response=label,
            feedback='',
            parent_mlalgorithm=algs[alg_index],
        )
        ml_request.save()

        prediction['request_id'] = ml_request.id

        return Response(prediction)


class StartABTestAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = ABTestSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    instance = serializer.save()

                    # update status for first algorithm
                    status_1 = MLAlgorithmStatus(
                        status='ab_testing',
                        created_by=instance.created_by,
                        parent_mlalgorithm=instance.parent_mlalgorithm_1,
                        active=True)
                    status_1.save()
                    deactivate_other_statuses(status_1)

                    # update status for second algorithm
                    status_2 = MLAlgorithmStatus(
                        status='ab_testing',
                        created_by=instance.created_by,
                        parent_mlalgorithm=instance.parent_mlalgorithm_2,
                        active=True)
                    status_2.save()
                    deactivate_other_statuses(status_2)

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StopABTestAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request, ab_test_id, format=None):
        try:
            ab_test = ABTest.objects.get(pk=ab_test_id)

            if ab_test.ended_at is not None:
                return Response({'message': 'AB Test already finished.'})

            date_now = datetime.datetime.now()

            # alg #1 accuracy
            all_responses_1 = MLAlgorithmRequest.objects.filter(
                parent_mlalgorithm=ab_test.parent_mlalgorithm_1,
                created_at__gt=ab_test.created_at,
                created_at__lt=date_now
            ).count()

            correct_responses_1 = MLAlgorithmRequest.objects.filter(
                parent_mlalgorithm=ab_test.parent_mlalgorithm_1,
                created_at__gt=ab_test.created_at,
                created_at__lt=date_now,
                response=F('feedback')
            ).count()

            accuracy_1 = correct_responses_1 / float(all_responses_1)
            print(all_responses_1, correct_responses_1, accuracy_1)

            # alg #2 accuracy
            all_responses_2 = MLAlgorithmRequest.objects.filter(
                parent_mlalgorithm=ab_test.parent_mlalgorithm_2,
                created_at__gt=ab_test.created_at,
                created_at__lt=date_now
            ).count()

            correct_responses_2 = MLAlgorithmRequest.objects.filter(
                parent_mlalgorithm=ab_test.parent_mlalgorithm_2,
                created_at__gt=ab_test.created_at,
                created_at__lt=date_now,
                response=F('feedback')
            ).count()

            accuracy_2 = correct_responses_2 / float(all_responses_2)
            print(all_responses_2, correct_responses_2, accuracy_2)

            # select algorithm with higher accuracy
            alg_id_1, alg_id_2 = ab_test.parent_mlalgorithm_1, ab_test.parent_mlalgorithm_2
            if accuracy_1 < accuracy_2:
                alg_id_1, alg_id_2 = alg_id_2, alg_id_1

            # update status for first algorithm
            status_1 = MLAlgorithmStatus(
                status='production',
                created_by=ab_test.created_by,
                parent_mlalgorithm=alg_id_1,
                active=True
            )
            status_1.save()
            deactivate_other_statuses(status_1)

            # update status for second algorithm
            status_2 = MLAlgorithmStatus(
                status='testing',
                created_by=ab_test.created_by,
                parent_mlalgorithm=alg_id_2,
                active=True
            )
            status_2.save()
            deactivate_other_statuses(status_2)

            summary = "Algorithm #1 accuracy: {}, Algorithm #2 accuracy: {}".format(accuracy_1, accuracy_2)
            ab_test.ended_at = date_now
            ab_test.summary = summary
            ab_test.save()

            return Response({'message': 'AB Test finished.', 'summary': summary})

        except Exception as e:
            return Response(
                {'status': 'Error', 'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
