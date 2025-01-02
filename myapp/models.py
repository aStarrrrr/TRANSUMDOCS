

from django.db import models

# Create your models here.
class Login(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    user_type=models.CharField(max_length=100)

class User(models.Model):
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    # phone=models.CharField(max_length=100)

class Feedback(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField(auto_now=True)
    feedback=models.CharField(max_length=100)

class Complaint(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField(auto_now=True)
    complaint=models.CharField(max_length=100)
    reply=models.CharField(max_length=100)

class File(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField(auto_now=True)
    file=models.TextField()
    output_summary=models.TextField()
    output_translated=models.TextField()