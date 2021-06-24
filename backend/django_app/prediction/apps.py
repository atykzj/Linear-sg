from django.apps import AppConfig
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
import urllib
import os

# SCIKIT LEARN DOCS FOR RUNNING JOBLIB
# https://scikit-learn.org/stable/modules/model_persistence.html

try:
    style_mlmodel
    Effnet_model
except NameError:
    style_mlmodel = None
    Effnet_model = None

#disable GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
class PredictionConfig(AppConfig):
    CHECK_LOAD_ONCE = False
    name = 'prediction'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MLMODEL_FOLDER = os.path.join(BASE_DIR, 'prediction/models/')


    # Style
    print(f"This is base dir {BASE_DIR}")
    STYLE_MLMODEL_FILE = os.path.join(MLMODEL_FOLDER, 'styleclassifier.h5')
    if style_mlmodel == None:
        try:
            style_mlmodel = tf.keras.models.load_model(STYLE_MLMODEL_FILE)
        except OSError:
            style_mlmodel = tf.keras.models.load_model('models/styleclassifier.h5')

    # init
    if Effnet_model == None:
        Effnet_model = EfficientNetB0(include_top=True, weights="imagenet", classes=1000, classifier_activation="softmax")

    # if feature_dict == None:
    #     feature_dict = urllib.URLopener()
    #     feature_dict.retrieve("https://storage.googleapis.com/linear-static-assets/subset/dict.json", "dict.json")