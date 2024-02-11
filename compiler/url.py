from django.urls import path 
from . import views
from .auth.views import signup
from .auth.views import login
urlpatterns = [
     path("signup", signup, name="signup"),
     path("login", login, name="login"),
     
   # path("execute", core.views.execute_python, name="index"),
]
