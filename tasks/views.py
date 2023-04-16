#View, es para nosotros ejecutar algo cuando una url sea visitada
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm #importar la clase que me permite crear un formulario ya creado
from django.contrib.auth.models import User #importa el modelo de usuarios para registrarlo
from django.http import HttpResponse

# Create your views here.
def home(request): #Request es un parametro que django ofrece para obtener información
    return render(request,'home.html',);

def signup(request):
    if request.method=='GET':
        return render(request,'signup.html',{
            'form':UserCreationForm
        })
    else:
        if request.POST['password1']==request.POST['password2']:#verifica si las dos contraseñas son iguales
            try:
                #Se ejecuto el  python 'manage.py migrate' y se crearon tablas sqlite por defecto
                user=User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()#guarda el usuario en la base de datos por defecto
                return HttpResponse("Usuario registrado")
            except:
                return HttpResponse("Usuario ya existe")
        return HttpResponse("Contraseña incorrecta")
    

