from django.urls import path
from .views import RecommendationView

urlpatterns = [
    path('recommendations/<str:user_id>/', RecommendationView.as_view(), name='recommendations'),
]