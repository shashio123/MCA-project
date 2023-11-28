from django.urls import path
from . import views

urlpatterns = [
    path('manage', views.manage, name='manage'),
    path('manage/footprint/<int:profileid>', views.footprint, name='footprint')
]