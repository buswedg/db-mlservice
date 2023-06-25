from rest_framework import serializers

from apps.endpoints.models import Endpoint, MLAlgorithm, MLAlgorithmStatus, MLAlgorithmRequest, ABTest


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = (
            'id',
            'name',
            'owner',
            'created_at',
        )
        read_only_fields = fields


class MLAlgorithmSerializer(serializers.ModelSerializer):
    current_status = serializers.SerializerMethodField(read_only=True)

    def get_current_status(self, mlalgorithm):
        return MLAlgorithmStatus.objects.filter(parent_mlalgorithm=mlalgorithm).latest('created_at').status

    class Meta:
        model = MLAlgorithm
        fields = (
            'id',
            'name',
            'description',
            'code',
            'version',
            'owner',
            'created_at',
            'parent_endpoint',
            'current_status',
        )
        read_only_fields = fields


class MLAlgorithmRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLAlgorithmRequest
        fields = (
            'id',
            'input_data',
            'full_response',
            'response',
            'feedback',
            'created_at',
            'parent_mlalgorithm',
        )
        read_only_fields = (
            'id',
            'input_data',
            'full_response',
            'response',
            'created_at',
            'parent_mlalgorithm',
        )


class MLAlgorithmStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLAlgorithmStatus
        fields = (
            'id',
            'active',
            'status',
            'created_by',
            'created_at',
            'parent_mlalgorithm',
        )
        read_only_fields = (
            'id',
            'active',
        )


class ABTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ABTest
        fields = (
            'id',
            'title',
            'created_by',
            'created_at',
            'ended_at',
            'summary',
            'parent_mlalgorithm_1',
            'parent_mlalgorithm_2',
        )
        read_only_fields = (
            'id',
            'ended_at',
            'created_at',
            'summary',
        )
