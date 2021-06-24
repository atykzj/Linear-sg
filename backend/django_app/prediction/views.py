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


# Create your views here.
# Class based view to predict based on IRIS model
class Style_Model_Predict(APIView):

    # # Check if authenticated
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    throttle_classes = [LimitedRateThrottle]

    def post(self, request, format=None):
        print("Find the name of style.")
        if "data" in request.data:
            data = request.data['data']
        else:
            data = request.data

        img_list = []
        for i in range(len(data)):
            filename = f"00{i}.jpg"
            img_list.append(
                {filename: data[i]}
            )

        # find stacked vector from multiple images
        input_y = inference.stack_img(img_list, "style")

        #prediction
        loaded_style_mlmodel = PredictionConfig.style_mlmodel
        # prediction = inference.predict_image(input_y, loaded_style_mlmodel)
        prediction = loaded_style_mlmodel.predict(input_y)
        predictions = pd.DataFrame(prediction, columns=class_names)
        sorted_cats = predictions.sum().sort_values(ascending=False).index
        output = 'Your prefered style is ' + sorted_cats[0:3][0] + ' with a mix of ' + sorted_cats[0:3][1] + ' and ' +\
                 sorted_cats[0:3][2]

        # # clean up
        # TEMPDIR = tempfile.gettempdir()
        # files = glob.glob(TEMPDIR + '/*')
        # for f in files:
        #     os.remove(f)


        response_dict = {"Results": output,
                         "sorted_cats": sorted_cats}
        print(response_dict)
        return Response(response_dict, status=200)

class Rec_Model_Predict(APIView):

    # # Check if authenticated
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    throttle_classes = [LimitedRateThrottle]

    def post(self, request, format=None):
        print("Find list of similar images.")
        # data in form of list of dict, 'src': link
        if "data" in request.data:
            data = request.data['data']
        else:
            data = request.data

        # Styles
        loaded_Effnet_model = PredictionConfig.Effnet_model

        # print(data.data)
        # Get list of image links
        # img_list = data['data']
        img_list = []

        for i in range(len(data)):
            # print(data[i])
            filename = f"00{i}.jpg"
            img_list.append(
                {filename: data[i]}
            )

        nb_closest_images = 8
        IR = ImageRecommender(loaded_Effnet_model, DB_ROOT)
        IR.load_db_dict()
        # find stacked vector from multiple images, put in the type
        input_y = inference.stack_img(img_list, "rec")

        # extract feature and find closest images
        # Return just the img index
        closest_imgs = IR.find_similar(input_y, nb_closest_images)
        response_dict = {"Results": closest_imgs
        }
        print(response_dict)

        # # clean up
        # TEMPDIR = tempfile.gettempdir()
        # files = glob.glob(TEMPDIR + '/*')
        # for f in files:
        #     os.remove(f)
        return Response(response_dict, status=200)


# Combine both
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
        # data in form of list of dict, 'src': link
        if "data" in request.data:
            data = request.data['data']
        else:
            data = request.data
        img_list = []

        for i in range(len(data)):
            # print(data[i])
            filename = f"00{i}.jpg"
            img_list.append(
                {filename: data[i]}
            )
        end = timer()
        print('Get request data：' + str(timedelta(seconds=end-start)))

        # Style name
        # find stacked vector from multiple images

        start = timer()
        input_y_style = inference.stack_img(img_list, "style")

        # run style predict
        prediction_stylename = loaded_style_mlmodel.predict(input_y_style)
        predictions_stylename = pd.DataFrame(prediction_stylename, columns=class_names)
        sorted_cats_stylename = predictions_stylename.sum().sort_values(ascending=False).index
        end = timer()
        print('Style Classifier：' + str(timedelta(seconds=end-start)))

        # List of images
        input_y_rec = inference.stack_img(img_list, "rec")
        # extract features
        IR = ImageRecommender(loaded_Effnet_model, DB_ROOT, CLOUD_DIR)
        # find similar

        start = timer()
        IR.load_db_dict()
        end = timer()
        print('Load db: ' + str(timedelta(seconds=end-start)))   
        
        start = timer()
        nb_closest_images = 6
        closest_imgs = IR.find_similar(input_y_rec, nb_closest_images)
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

        


