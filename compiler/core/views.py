from django.http import HttpResponse
import loggin

def index(request):
    return HttpResponse(" hello this is my first ever python server")


# views.py
import subprocess
import traceback
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import jwt

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

            if language == 'python':
                with open("temp.py", "w") as file:
                  file.write(code)
            elif language == 'rust':
                with open("temp.rs", "w") as file:
                  file.write(code)
            else:
                return JsonResponse({'error': 'Language is not yet supported'}, status=405)


            command = ''
            command2 = ''
            if language == 'python':
                command = ["python3", "temp.py"]
            elif language == 'rust':
                command = ["rustc", "temp.rs"]
                execute_process = subprocess.run(command, capture_output=True)
                if len(execute_process.stderr.decode()) != 0:
                    return JsonResponse({'output': execute_process.stderr.decode()})

                command =  ["./temp",""]
                
            else:
                return JsonResponse({'error': 'Language is not yet supported'}, status=405)



            
            
            # Execute the Python script
            execute_process = subprocess.run(command, capture_output=True)
            stdout = execute_process.stdout.decode()
            stderr = execute_process.stderr.decode()
            a = stdout+stderr
            
            # Return the output of the Python script as JSON response
            return JsonResponse({'output': a})
        except Exception as e:
            # Return any error that occurs during code execution
            return JsonResponse({'error': traceback.format_exc()}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)