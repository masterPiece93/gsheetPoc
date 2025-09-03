# urls

from django.urls import path
from . import views

app_name = "gsheets" # this key is used when you refer an endpoint by `reverse`

urlpatterns = [
    path('', views.index, name='index'),
    path('sheet/', views.read_sheet_data, name='sheet')
    # Add more app-specific URL patterns here
]