from django.urls import path
import prediction.views as views

urlpatterns = [
    path('style/', views.Rec_Style_Model_Predict().as_view(), name = 'api_predict'),
    path('status/', views.Status_Check().as_view(), name = 'api_predict'),
    path('color/', views.Color().as_view(), name='api_predict'),
]