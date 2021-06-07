from django.apps import AppConfig
import pandas as pd
from joblib import load
from tensorflow import keras
import tensorflow as tf
import os

# SCIKIT LEARN DOCS FOR RUNNING JOBLIB
# https://scikit-learn.org/stable/modules/model_persistence.html
class PredictionConfig(AppConfig):
    name = 'prediction'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MLMODEL_FOLDER = os.path.join(BASE_DIR, 'prediction/mlmodel/')
    # Iris
    MLMODEL_FILE = os.path.join(MLMODEL_FOLDER, "IRISRandomForestClassifier.joblib")
    mlmodel = load(MLMODEL_FILE)
    # Style
    STYLE_MLMODEL_FILE = os.path.join(MLMODEL_FOLDER, 'styleclassifier.h5')
    style_mlmodel = keras.models.load_model(STYLE_MLMODEL_FILE)