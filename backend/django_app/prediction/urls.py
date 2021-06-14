from django.urls import path
import prediction.views as views

urlpatterns = [
    path('predic/', views.IRIS_Model_Predict.as_view(), name = 'api_predict'),
    path('predict/', views.Style_Model_Predict().as_view(), name = 'api_predict'),
    path('recommend/', views.Rec_Model_Predict().as_view(), name = 'api_predict'),
]