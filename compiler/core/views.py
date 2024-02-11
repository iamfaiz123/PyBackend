from django.http import HttpResponse
from ..models import CodeAttempt
from datetime import datetime


def index(request):
    return HttpResponse(" hello this is my first ever python server")


# views.py
import subprocess
import traceback
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def execute_code(request):
    # Check if request method is POST
    if request.method == 'POST':
        # Get the JSON data from request body
        try:
            data = json.loads(request.body)
            code = data.get('code', '')
            language =  data.get('lang', '')
            # Write the Python code to a temporary file

            runFinalCode = True
            stderr = ""
            stdout = ""
            reponse = ""
            if language == 'python':
                with open(request.userEmail+"temp.py", "w") as file:
                  file.write(code)
            elif language == 'rust':
                with open(request.userEmail+"temp.rs", "w") as file:
                  file.write(code)
            else:
                return JsonResponse({'error': 'Language is not yet supported'}, status=405)
            command = ''
            if language == 'python':
                command = ["python3", request.userEmail+"temp.py"]
            # incase of rust, first we need to create , .exe file and then run the code    
            elif language == 'rust':
                command = ["rustc", request.userEmail+"temp.rs"]
                execute_process = subprocess.run(command, capture_output=True)
                if len(execute_process.stderr.decode()) != 0:
                    stderr =  execute_process.stderr.decode()
                    runFinalCode = False
                command =  ["./"+request.userEmail+"temp",""]
            else:
                return JsonResponse({'error': 'Language is not yet supported'}, status=405)
            
            # Execute code
            if runFinalCode:
                execute_process = subprocess.run(command, capture_output=True)
                stdout = execute_process.stdout.decode()
                stderr = execute_process.stderr.decode()
                response = stdout+stderr


            # insert data in user code attempts

            # Create an instance of CodeAttempt
            code_attempt = CodeAttempt(
                user_email=request.userEmail,
                question_slug='your-question-slug',
                attempt_error=stderr,
                attempt_output=stdout,
                code=code,
                languge_user=language,  # Assuming this is the language used
                created_at=datetime.now(),  # Assuming you want to use current time
            )

            code_attempt.save()
            
            # Return the output of the Python script as JSON response
            return JsonResponse({'output': response})
        except Exception as e:
            # Return any error that occurs during code execution
            return JsonResponse({'error': traceback.format_exc()}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



@csrf_exempt
def get_user_last_code(request):
    userData = CodeAttempt.objects.filter(user_email=request.userEmail)
    res = []
    for data in userData:
        res.append({
            'languge': data.languge_user,
            'questionSlug':data.question_slug,
            'stdError':data.attempt_error,
            'stdOut':data.attempt_output,
            'code':data.code,
            'executedAt':data.created_at
        })

    return JsonResponse({'data': res}, status=201)    
  



