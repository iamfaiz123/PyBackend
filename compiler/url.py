from django.urls import path 
from . import views
from .auth.views import signup
from .auth.views import login
from .auth.views import get_user_data
urlpatterns = [
     path("signup", signup, name="signup"),
     path("login", login, name="login"),
     path("user/get-user-data", get_user_data, name="login"),
     
     
   # path("execute", core.views.execute_python, name="index"),
]
