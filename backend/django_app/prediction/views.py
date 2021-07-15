from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .throttles import LimitedRateThrottle, BurstRateThrottle

from prediction.apps import PredictionConfig
import pandas as pd
import os
from prediction.helper import inference
from prediction.helper.recommender import ImageRecommender

from timeit import default_timer as timer
from datetime import timedelta

import numpy as np

# Access temporary files
import tempfile
import glob

# predefine class names
class_names = ['Contemporary',
 'Eclectic',
 'Industrial',
 'Kitchen',
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


class Status_Check(APIView):
    """Checking status, ensures app is running before predictions"""
    def post(self, request=None, format=None):

        response_dict = {
            "Status": "Instance running.",
        }
        return Response(response_dict, status=200)

class Rec_Style_Model_Predict(APIView):
    # # Check if authenticated
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    throttle_classes = [LimitedRateThrottle]

    def post(self, request, format=None):
        start_all =  timer()

        # Load Models   
        start = timer()
        loaded_Effnet_model = PredictionConfig.Effnet_model
        loaded_style_mlmodel = PredictionConfig.style_mlmodel
        end = timer()
        print('loading model time： '+ str(timedelta(seconds=end-start)))

        # Get request data
        start = timer()
        img_list = request.data
        end = timer()
        print('Get request data：' + str(timedelta(seconds=end-start)))

        # Predict Classes
        start = timer()
        input_y = inference.stack_img(img_list)
        prediction_stylename = loaded_style_mlmodel.predict(input_y)
        predictions_stylename = pd.DataFrame(prediction_stylename, columns=class_names)
        sorted_cats_stylename = predictions_stylename.sum().sort_values(ascending=False).index
        end = timer()
        print('Style Classifier：' + str(timedelta(seconds=end-start)))

        ##—————————————————————————————————————————————————————————————————————————————————————————————————————————###
        start = timer()
        IR = ImageRecommender(loaded_Effnet_model, DB_ROOT, CLOUD_DIR)
        end = timer()
        print('Load db: ' + str(timedelta(seconds=end-start)))  

        start = timer()
        closest_imgs = IR.find_similar(input_y)
        response_dict = {
            "Category": sorted_cats_stylename,
            "Image": closest_imgs,
                         }
        end = timer()       

        print('Recommender: ' + str(timedelta(seconds=end-start)))          
        end_all =  timer()
        print('Total time: ' + str(timedelta(seconds=end_all-start_all)))   
        print(response_dict)

        return Response(response_dict, status=200)

# Class status
class Color(APIView):
    def post(self, request=None, format=None):

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
