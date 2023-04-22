# View, es para nosotros ejecutar algo cuando una url sea visitada
from django.shortcuts import render, redirect
# importar la clase que me permite crear un formulario ya creado
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# importa el modelo de usuarios para registrarlo
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

# Create your views here.


def home(request):  # Request es un parametro que django ofrece para obtener información
    return render(request, 'home.html',)


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        # verifica si las dos contraseñas son iguales
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Se ejecuto el  python 'manage.py migrate' y se crearon tablas sqlite por defecto
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()  # guarda el usuario en la base de datos por defecto
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'Contraseña incorrecta'
        })


def tasks(request):
    return render(request, 'tasks.html')


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        
        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'Usuario o contraseña incorrectos'
            })
        else:
          login(request, user)
          return redirect('tasks')  



        
