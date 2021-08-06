from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


import os
import pandas as pd

from .throttles import LimitedRateThrottle, BurstRateThrottle
from prediction.apps import PredictionConfig
from prediction.helper import inference
from prediction.helper.recommender import ImageRecommender
from tensorflow.keras.models import Model
from timeit import default_timer as timer
from datetime import timedelta

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# predefine class names
class_names = ['Contemporary',
 'Eclectic',
 'Industrial',
 'Minimalistic',
 'Modern',
 'Retro',
 'Scandinavian',
 'Traditional',
 'Transitional',
 'Vintage']

# Load db from models folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_ROOT = os.path.join(BASE_DIR, 'prediction/models/')

# base_dir for cloud bucket
CLOUD_DIR = 'https://storage.googleapis.com/linear-static-assets/subset/'
CLOUD_DIR2 = 'https://storage.googleapis.com/linear-static-assets/palettes/'

class Status_Check(APIView):
    """Checking status, ensures app is running before predictions

        Parameters:
        APIView (class): is a class object template and add content to it.

        Returns:
        Response (class): returns a response API class within the APIView class.
    """
    def post(self, request=None, format=None):
        """Add String to check the object.

        Parameters:

        Returns:
        Response (class): returns a response object within the APIView class.
        """
        response_dict = {
            "Status": "Instance running.",
        }
        return Response(response_dict, status=200)

class Rec_Style_Model_Predict(APIView):
    """Run recommender model on input data and return results.

        Parameters:
        APIView (class): is a class object template and add content to it.

        Returns:
        Response (class): returns a response API class within the APIView class.
    """
    throttle_classes = [LimitedRateThrottle]

    def post(self, request, format=None):
        """Given input data of links of images, do preprocessing and inference.

        Parameters:
        request (dictionary): is a dict of Strings of links of images.

        Returns:
        Response (class): returns a response object within the APIView class.
        """
        # Load Models   
        start = timer()
        mlmodel = PredictionConfig.mlmodel
        rec_model = Model(inputs=mlmodel.input, outputs=mlmodel.layers[-2].output)

        if "data" in request.data:
            img_list = request.data['data']
        else:
            img_list = request.data

        # Predict Classes
        # Stack_img and get kmeans centroids
        input_y, rgb_list, hex_list = inference.stack_img(img_list)
        prediction_stylename = mlmodel.predict(input_y)
        predictions_stylename = pd.DataFrame(prediction_stylename, columns=class_names)
        sorted_cats_stylename = predictions_stylename.sum().sort_values(ascending=False).index
        end = timer()
        print('Style Classifier：' + str(timedelta(seconds=end-start)))

        # Image and Palette Recommender
        start =  timer()
        IR = ImageRecommender(rec_model, DB_ROOT, CLOUD_DIR)
        IR.load_db_dict('render.json')
        closest_style = IR.find_similar(input_y)
    
        PR = ImageRecommender(rec_model, DB_ROOT, CLOUD_DIR2)
        PR.load_db_dict('palette.json')
        closest_palette = PR.find_similar(input_y)
    
        response_dict = {
            "Category": sorted_cats_stylename,
            "Image": closest_style,
            "Palette": closest_palette,
            "rgb": rgb_list,
            "hex": hex_list
                         }
        end = timer()       

        print('Recommender: ' + str(timedelta(seconds=end-start)))          
        return Response(response_dict, status=200)

# Class status
class Color(APIView):
    """Run Color recommender model on input data and return results.

        Parameters:
        APIView (class): is a class object template and add content to it.

        Returns:
        Response (class): returns a response API class within the APIView class.
    """
    def post(self, request=None, format=None):
        """Given input data of links of images, do preprocessing and inference.

        Parameters:
        request (dictionary): is a dict of Strings of links of images.

        Returns:
        Response (class): returns a response object within the APIView class.
        """

        start_all =  timer()

        # data in form of list of dict, 'src': link
        if "data" in request.data:
            data = request.data['data']
        else:
            data = request.data
        rgb_list, hex_list = [], []

        # Define a function for the mapping
        rgb2hex = lambda r, g, b: '#%02x%02x%02x' % (r, g, b)

        for i in range(len(data)):
            temp_color = inference.faiss_kmeans(data[i])
            B = (temp_color*255).astype(int)  # convert to int
            rgb_list.append(B)
            hex_list.append(
                [rgb2hex(*B[i, :]) for i in range(B.shape[0])]
            )

        response_dict = {
            "rgb": rgb_list,
            "hex": hex_list
        }
        return Response(response_dict, status=200)
