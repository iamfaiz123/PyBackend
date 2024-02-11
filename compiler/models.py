from django.db import models

# Create your models here.

from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100,)
    password = models.CharField(max_length=100)
    email = models.EmailField(primary_key=True)

    def __str__(self):
        return self.name

class CodeAttempt(models.Model):
    user_email = models.EmailField()
    question_slug = models.SlugField()
    attempt_error = models.TextField()
    attempt_output = models.TextField()
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_email} - {self.question_slug} - {self.created_at}"

