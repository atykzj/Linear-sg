from django.apps import AppConfig
import pandas as pd
from joblib import load
from tensorflow import keras
import tensorflow as tf
import os
import keras
from tensorflow.keras.applications import EfficientNetB0

# SCIKIT LEARN DOCS FOR RUNNING JOBLIB
# https://scikit-learn.org/stable/modules/model_persistence.html

#disable GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

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

    #DB_ROOT = os.path.join(BASE_DIR, 'prediction/db/')
    # DB_ROOT = 'D:\Linear\Linear Repo\Image Classifier\subset'
    DB_ROOT = 'C:\linear\backend\subset'

    # init model
    Effnet_model = EfficientNetB0(include_top=True, weights="imagenet", classes=1000, classifier_activation="softmax")
