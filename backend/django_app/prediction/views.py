from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from prediction.apps import PredictionConfig
import pandas as pd
import os
from prediction.mlmodel import inference

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

# Create your views here.
# Class based view to predict based on IRIS model
class IRIS_Model_Predict(APIView):

    # # Check if authenticated
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        keys = []
        values = []
        for key in data:
            keys.append(key)
            values.append(data[key])
        X = pd.Series(values).to_numpy().reshape(1, -1)
        loaded_mlmodel = PredictionConfig.mlmodel
        y_pred = loaded_mlmodel.predict(X)
        y_pred = pd.Series(y_pred)
        target_map = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}
        y_pred = y_pred.map(target_map).to_numpy()
        response_dict = {"Predicted Iris Species": y_pred[0]}
        return Response(response_dict, status=200)

# Create your views here.
# Class based view to predict based on IRIS model
class Style_Model_Predict(APIView):

    # # Check if authenticated
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    print("This is sstyles")

    def post(self, request, format=None):
        # data in form of list of dict, 'src': link
        data = request.data

        # Styles
        loaded_style_mlmodel = PredictionConfig.style_mlmodel

        print(data)
        img_list = []
        for i in range(len(data)):
            filename = f"00{i}.jpg"
            img_list.append(
                {filename: data[i]['src']}
            )
        # find stacked vector from multiple images
        input_y = inference.stack_img(img_list)
        #prediction
        loaded_style_mlmodel = PredictionConfig.style_mlmodel
        # prediction = inference.predict_image(input_y, loaded_style_mlmodel)
        prediction = loaded_style_mlmodel.predict(input_y)
        predictions = pd.DataFrame(prediction, columns=class_names)
        sorted_cats = predictions.sum().sort_values(ascending=False).index
        output = 'Your prefered style is ' + sorted_cats[0:3][0] + ' with a mix of ' + sorted_cats[0:3][1] + ' and ' +\
                 sorted_cats[0:3][2]
        # clean up
        for i in img_list:
            for k in i:
                os.remove(k)

        response_dict = {"Predicted Iris Species":output,
                         "Results": output,
                         "sorted_cats": sorted_cats}
        return Response(response_dict, status=200)
