from django.urls import path 
from . import views
from .auth.views import signup
from .auth.views import login
from .auth.views import get_user_data
from .core.views import execute_code
from .core.views import get_user_last_code
urlpatterns = [
     path("signup", signup, name="signup"),
     path("login", login, name="login"),
     path("user/get-user-data", get_user_data, name="get-user-data"),
     path("execute/code", execute_code, name="code-execute"),
     path("execute/get-code", get_user_last_code, name="code-execute")
]
     

