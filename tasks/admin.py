from django.contrib import admin
from .models import *#traemos el modelo

# Register your models here.
#le damos acceso al administrador al modelo tarea 
admin.site.register(Task)
admin.site.register(Rol)
admin.site.register(UserRol)
admin.site.register(TipoLabor)
admin.site.register(Labor)
admin.site.register(Periodo)
admin.site.register(Evaluacion)