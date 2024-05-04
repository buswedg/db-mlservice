from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils.mixins.models.atoms import TimestampMixin


class Endpoint(TimestampMixin, models.Model):
    """
    The Endpoint object represents ML API endpoint.

    Attributes:
        name: The name of the endpoint, it will be used in API URL,
        owner: The string with owner name,
    """
    name = models.CharField(_('Name'), max_length=128)
    owner = models.CharField(_('Owner'), max_length=128)


class MLAlgorithm(TimestampMixin, models.Model):
    """
    The MLAlgorithm represent the ML algorithm object.

    Attributes:
        parent_endpoint: The reference to the Endpoint.
        name: The name of the algorithm.
        description: The short description of how the algorithm works.
        code: The code of the algorithm.
        version: The version of the algorithm similar to software versioning.
        owner: The name of the owner.
    """
    parent_endpoint = models.ForeignKey(
        Endpoint,
        related_name='ml_algorithm',
        verbose_name=_('Parent Endpoint'),
        on_delete=models.CASCADE
    )

    name = models.CharField(_('Name'), max_length=128)
    description = models.CharField(_('Description'), max_length=1000)
    code = models.CharField(_('Code'), max_length=50000)
    version = models.CharField(_('Version'), max_length=128)
    owner = models.CharField(_('Owner'), max_length=128)


class MLAlgorithmStatus(TimestampMixin, models.Model):
    """
    The MLAlgorithmStatus represent status of the MLAlgorithm which can change during the time.

    Attributes:
        parent_endpoint: The reference to corresonding Endpoint.
        status: The status of algorithm in the endpoint. Can be: testing, staging, production, ab_testing.
        created_by: The name of creator.
        created_at: The date of status creation.
        parent_mlalgorithm: The reference to corresponding MLAlgorithm.
    """
    parent_mlalgorithm = models.ForeignKey(
        MLAlgorithm,
        related_name='ml_algorithm_status',
        verbose_name=_('Parent ML Algorithm'),
        on_delete=models.CASCADE,
    )

    status = models.CharField(_('Status'), max_length=128)
    active = models.BooleanField(_('Active?'))
    created_by = models.CharField(_('Created By'), max_length=128)


class MLAlgorithmRequest(TimestampMixin, models.Model):
    """
    The MLAlgorithmRequest will keep information about all requests to ML algorithms.

    Attributes:
        parent_mlalgorithm: The reference to MLAlgorithm used to compute response.
        input_data: The input data to ML algorithm in JSON format.
        response: The response of the ML algorithm in JSON format.
        feedback: The feedback about the response in JSON format.
    """
    parent_mlalgorithm = models.ForeignKey(
        MLAlgorithm,
        related_name='ml_algorithm_request',
        verbose_name=_('Parent ML Algorithm'),
        on_delete=models.CASCADE
    )

    input_data = models.CharField(_('Input Data'), max_length=10000)
    full_response = models.CharField(_('Full Response'), max_length=10000)
    response = models.CharField(_('Response'), max_length=10000)
    feedback = models.CharField(_('Feedback'), max_length=10000, blank=True, null=True)


class ABTest(TimestampMixin, models.Model):
    """
    The ABTest will keep information about A/B tests.
    Attributes:
        parent_mlalgorithm_1: The reference to the first corresponding MLAlgorithm.
        parent_mlalgorithm_2: The reference to the second corresponding MLAlgorithm.
        title: The title of test.
        created_by: The name of creator.
        ended_at: The date of test stop.
        summary: The description with test summary, created at test stop.
    """
    parent_mlalgorithm_1 = models.ForeignKey(
        MLAlgorithm,
        related_name='ab_test_algorithm_1',
        verbose_name=_('Parent ML Algorithm 1'),
        on_delete=models.CASCADE
    )
    parent_mlalgorithm_2 = models.ForeignKey(
        MLAlgorithm,
        related_name='ab_test_algorithm_2',
        verbose_name=_('Parent ML Algorithm 2'),
        on_delete=models.CASCADE
    )

    title = models.CharField(_('Title'), max_length=10000)
    created_by = models.CharField(_('Created By'), max_length=128)
    ended_at = models.DateTimeField(_('Ended At'), blank=True, null=True)
    summary = models.CharField(_('Summary'), max_length=10000, blank=True, null=True)
