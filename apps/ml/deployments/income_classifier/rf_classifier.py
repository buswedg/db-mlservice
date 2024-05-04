import os

import joblib
from django.conf import settings

from .helpers import Helpers

ARTIFACTS_DIR = os.path.join(settings.BASE_DIR, 'artifacts')
DEPLOYMENT = "income_classifier"

ARTIFACTS_PATH = os.path.join(ARTIFACTS_DIR, DEPLOYMENT)


class RFClassifier(Helpers):
    def __init__(self):
        self.values_fill_missing = joblib.load(os.path.join(ARTIFACTS_PATH, 'train_mode.joblib'))
        self.encoders = joblib.load(os.path.join(ARTIFACTS_PATH, 'encoders.joblib'))
        self.model = joblib.load(os.path.join(ARTIFACTS_PATH, 'rf_classifier.joblib'))
