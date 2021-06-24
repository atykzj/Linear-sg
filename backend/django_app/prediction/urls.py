from django.urls import path
import prediction.views as views

urlpatterns = [
    path('predict/', views.Style_Model_Predict().as_view(), name = 'api_predict'),
    path('recommend/', views.Rec_Model_Predict().as_view(), name = 'api_predict'),
    path('style/', views.Rec_Style_Model_Predict().as_view(), name = 'api_predict'),
]