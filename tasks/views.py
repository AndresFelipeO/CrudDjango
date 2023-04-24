# View, es para nosotros ejecutar algo cuando una url sea visitada
from django.shortcuts import render, redirect, get_object_or_404
# importar la clase que me permite crear un formulario ya creado
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# importa el modelo de usuarios para registrarlo
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate #login crea el cookie por nosotros
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):  # Request es un parametro que django ofrece para obtener información
    return render(request, 'home.html',)

#registra un usuario al sistema
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
                return redirect('tasks') #redirecciona a la pagina tasks
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'Contraseña incorrecta'
        })

#redireciona a la pagina de tareas no completadas}
@login_required
def tasks(request):
    tasks=Task.objects.filter(user=request.user,datecompleted__isnull=True)#devuelve todas las tareas de la base de datos
    return render(request, 'tasks.html',{
        'tasks':tasks,
    })
#muestra las tareas completadas
@login_required
def tasks_completed(request):
    tasks=Task.objects.filter(user=request.user,datecompleted__isnull=False)#devuelve todas las tareas de la base de datos
    return render(request, 'tasks.html',{
        'tasks':tasks,
    })

#crea una tarea nueva
@login_required
def create_task(request):
    if request.method=='GET':
        return render(request,'create_task.html',{
            'form':TaskForm,
        })
    else:
        try:
            form=TaskForm(request.POST)
            newTask=form.save(commit=False)
            newTask.user=request.user
            newTask.save()
            return render(request,'tasks.html',{
                'form':TaskForm,
            })
        except ValueError:
            return render(request,'create_task.html',{
            'form':TaskForm,
            'error':'Plase provide data'
        })

#muestra los detalles de una tarea en especifico y permite modificar
@login_required
def task_detail(request,task_id):
    if request.method=='GET': #muestra las tareas
        task=get_object_or_404(Task,pk=task_id,user=request.user)
        form=TaskForm(instance=task)#llena el formulario con la tarea 
        return render(request, 'task_detail.html',
                {'task':task,
                   'form':form
                })
    else:#actualiza la tarea
       try:
            task=get_object_or_404(Task,pk=task_id,user=request.user)
            form=TaskForm(request.POST,instance=task)#crea una formulario con los datos nuevos
            form.save()#los guarda en la base de datos
            return redirect('tasks')
       except ValueError:
           return render(request, 'task_detail.html',
                {'task':task,
                   'form':form,
                   'error':"Error updating task"
                })

#Completa las tareas completadas
@login_required
def complete_task(request,task_id):
    task=get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method=='POST':
        task.datecompleted=timezone.now()
        task.save()
        return redirect('tasks')

#Elimina la tarea 
@login_required
def delete_task(request,task_id):
    task=get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method=='POST':
        task.delete()
        return redirect('tasks')

#Cierra la sesion del usuario
@login_required
def signout(request):
    logout(request)
    return redirect('home')

#permite atenticar al usuario con una cuenta ya creada
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



        
