import os

from django.apps import AppConfig
import tensorflow as tf
from tensorflow.keras.models import Model
# SCIKIT LEARN DOCS FOR RUNNING JOBLIB
# https://scikit-learn.org/stable/modules/model_persistence.html

try:
    mlmodel
    
except NameError:
    mlmodel = None

#disable GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
class PredictionConfig(AppConfig):
    CHECK_LOAD_ONCE = False
    name = 'prediction'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MLMODEL_FOLDER = os.path.join(BASE_DIR, 'prediction/models/')

    print(f"This is base dir {BASE_DIR}")
    MODEL_FILE = os.path.join(MLMODEL_FOLDER, 'style.h5')
    if mlmodel == None:
        mlmodel = tf.keras.models.load_model(MODEL_FILE)