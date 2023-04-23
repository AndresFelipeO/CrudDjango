from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model): #crear una tabla task sql
    title=models.CharField(max_length=100)  #nos permite definir el tipo del atributo
    description=models.TextField(blank=True)
    created=models.DateTimeField(auto_now_add=True)
    datecompleted=models.DateTimeField(null=True,blank=True)
    important=models.BooleanField(default=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)


    def __str__(self):#cuando utilicen este modelo en string va a retornar el titulo
        return self.title+'- by '+self.user.username