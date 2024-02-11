import json 
from django.http import JsonResponse
from ..models import User
from django.views.decorators.csrf import csrf_exempt

class UserLogin:
    def __init__(self,email,password):
        self.email = email
        self.password = password

class SignFormValidationError(Exception):
    def __init__(self, message, errorCode,statusCode):
        self.message = message
        self.errorCode = errorCode
        self.statusCode = statusCode
        super().__init__(message)


class LoginFormValidationError(Exception):
    def __init__(self,message,errorCode,statusCode):
        self.message = message
        self.statusCode = statusCode
        self.errorCode = errorCode
        super().__init__(message)

def validate_login_form(requestBody):
    email = requestBody.get("email", "")
    password = requestBody.get("password", "")
    if not password:
        raise LoginFormValidationError('password is empty', 301,401)
    elif not email:
        raise LoginFormValidationError('email is empty', 301,401)

    else:
        return UserLogin(email=email.lower(),password=password)   

def validate_signup_form(requestBody):
    user_name = requestBody.get("user_name", "")
    password = requestBody.get("password", "")
    email = requestBody.get("email", "")

    if not user_name:
        raise SignFormValidationError('user name is empty', 301,401)
    elif not password:
        raise SignFormValidationError('password is empty', 301,401)
    elif not email:
        raise SignFormValidationError('email is empty', 301,401)
    else:
        return User.objects.create( password=password, email=email.lower(), name= user_name, )    
     

@csrf_exempt
def signup(request):
    
    # if invalid request method return error
    if request.method != 'POST':
        return JsonResponse({'error':'Status code not allowed','errorCode':322},status=405)
    try:
        signupForm = json.loads(request.body)
       
        user = validate_signup_form(signupForm)
        user.save()
        return JsonResponse({'success':'user created'},status=201)

    except SignFormValidationError as e:
        return JsonResponse({'error':e.message,'errorCode':e.errorCode},status=e.statusCode)
    except Exception as e:
        return JsonResponse({'error':'internal server error','errorCode':500},status=500)

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken  # Fixed typo here
from django.contrib.auth import authenticate
from django.conf import settings
import jwt
@csrf_exempt
def login(request):
    # if invalid request method return error
    if request.method != 'POST':
        return JsonResponse({'error':'Status code not allowed','errorCode':322},status=405)
    try:
        jsonData = json.loads(request.body)
        userLogin = validate_login_form(jsonData)
        userData = User.objects.get(email=userLogin.email)
        if userData.password != userLogin.password:
            return JsonResponse({'error':'email or password incorrect'},status=401)
         # JWT payload
        payload = {'email': userData.email}
        # Generate JWT token
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        
        # Return token in response
        return JsonResponse({'token': jwt_token})    


    except LoginFormValidationError as e:
        return JsonResponse({'error':e.message,'errorCode':e.errorCode},status=e.statusCode) 
    except Exception as e:
        print(e)
        return JsonResponse({'error':'internal server error','errorCode':500},status=500)

@csrf_exempt
def get_user_data(request):
    userData = User.objects.get(email=request.userEmail)
    print(userData)
    return JsonResponse({'data':userData.email},status=200)
    






         

    


    
   

      




