from django.contrib import admin
from .models import Task#traemos el modelo

# Register your models here.
#le damos acceso al administrador al modelo tarea 
admin.site.register(Task)