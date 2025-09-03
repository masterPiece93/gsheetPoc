# urls

from django.urls import path
from . import views

app_name = "gauth" # this key is used when you refer an endpoint by `reverse`

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name="login"),
    path('signin-google', views.callback, name="callback"),

    # Add more app-specific URL patterns here
]

# NOTE : `/` at the end of the route will be taken in cosideration while redirected .
# # if you have strict slashes issues , do take care where to put the `/` or not .