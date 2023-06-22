# View, es para nosotros ejecutar algo cuando una url sea visitada
from venv import logger
from django.shortcuts import render, redirect, get_object_or_404
# importar la clase que me permite crear un formulario ya creado
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# importa el modelo de usuarios para registrarlo
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate #login crea el cookie por nosotros
from .forms import TaskForm
from .models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import datetime
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
                userDoc = UserDoc.objects.create(

                    nombre = request.POST['nombre'],
                    apellido = request.POST['apellido'],
                    genero = request.POST['genero'],
                    estudio = request.POST['estudio'],
                    foto=request.POST['foto'],
                    user=user
                )
                user.save()  # guarda el usuario en la base de datos por defecto
                userDoc.save()
                return redirect('decano_menu') #redirecciona a la pagina tasks
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
            if request.POST['username']=="decano":
                login(request, user)
                return redirect('decano_menu')  
            elif request.POST['username']=="coordinador":
                login(request, user)
                return redirect('coordinador_menu')
            login(request, user)
            return redirect('docente_menu') 
        
@login_required
def docente_menu(request):
    #usuario=get_object_or_404(Task,user=request.user)
    
    usuario=UserDoc.objects.filter(user=request.user).first()#devuelve todas las tareas de la base de datos
    if request.method == 'GET':
        return render(request, 'interfazdocente.html',{'user':usuario})
    else:
       return render(request, 'home.html')

@login_required
def decano_menu(request):
    if request.user.username=='decano':
        usuario=UserDoc.objects.filter(user=request.user).first()#devuelve todas las tareas de la base de datos
    
        if request.method == 'GET':
            return render(request, 'interfazDecano.html',{'user':usuario})
        else:
            return render(request, 'home.html')
    return redirect('logout')


@login_required
def coordinador_menu(request):
    if request.user.username=='coordinador':
        usuario=UserDoc.objects.filter(user=request.user).first()#devuelve todas las tareas de la base de datos
        if request.method == 'GET':
            return render(request, 'interfazCoordinador.html',{'user':usuario})
        else:
            return render(request, 'home.html')
    return redirect('logout')

@login_required
def evaluacion_view(request):
    if request.method == 'GET':
        try:
            usuario=UserDoc.objects.filter(user=request.user).first()
            userRol=UserRol.objects.get(user=usuario.user.pk)
            
            eva = Evaluacion.objects.filter(userRol_id=userRol)
            print(type(eva))
            if len(eva)>0:
                return render(request, 'prueba.html',{'user':usuario,"evaluaciones": eva})
            return redirect('docente_menu')
        except Exception as e:
            logger.exception(e)
            return redirect('docente_menu')
    return redirect('docente_menu')


@login_required
def labor_view(request):
    if request.method == 'GET':
        lb = Labor.objects.all()
        tipoLabor=TipoLabor.objects.all()
        return render(request, 'gestionarlabor.html',{'tl':tipoLabor,'labor':lb})
    return redirect('coordinador_menu')

@login_required
def periodo_view(request):
    if request.method == 'GET':
        prd=Periodo.objects.all()
        return render(request, 'gestionarPeriodo.html',{'periodos':prd})
    return redirect('decano_menu')


@login_required
def gestionar_Eva_view(request):
    if request.method == 'GET':
        eva=Evaluacion.objects.all()
        perido=Periodo.objects.all()
        rolUser=UserRol.objects.all()
        lb = Labor.objects.all()
        return render(request, 'gestionarautoevaluacion.html',{"periodos":perido,"labors":lb,"userroles":rolUser,"evaluaciones":eva})
    return redirect('coordinador_menu')

@login_required
def rol_view(request):
    if request.method == 'GET':
        usuario=UserDoc.objects.all()
        rol=Rol.objects.all()
        userRol=UserRol.objects.all()
        return render(request, 'asignarRoles.html',{'usuarios':usuario,'roles':rol,'rolusers':userRol})
    return redirect('coordinador_menu')

@login_required
def labor_registrar(request):
    if request.method == 'POST':
        try:
            if 'Guardar' in request.POST:
                tipo_labor_id = request.POST['tipo']
                try:
                    tipo_labor = TipoLabor.objects.get(id=tipo_labor_id)
                    lb = Labor.objects.create(
                        nombre=request.POST['nombre'],
                        horas=request.POST['horas'],
                        tl_id=tipo_labor,
                        descripcion=request.POST['descripcion']
                    )
                    lb.save()
                    return redirect('labor')
                except TipoLabor.DoesNotExist:
                    pass
            elif 'Eliminar' in request.POST:
                labor_id = request.POST['Blabor']
                try:
                    labor = Labor.objects.get(id=labor_id)
                    labor.delete()
                except Labor.DoesNotExist:
                    pass
                return redirect('labor')
            elif 'Editar' in request.POST:
                labor_id = request.POST['Blabor']
                tipo_labor_id = request.POST['tipo']
                try:
                    tipo_labor = TipoLabor.objects.get(id=tipo_labor_id)
                    lb = Labor.objects.get(id=labor_id)
                    lb.nombre=request.POST['nombre']
                    lb.horas=request.POST['horas']
                    lb.tl_id=tipo_labor
                    lb.descripcion=request.POST['descripcion']
                    lb.save()
                except Labor.DoesNotExist:
                    pass
                return redirect('labor')
            elif 'Buscar' in request.POST:
                labor_id = request.POST['Blabor']
                lb = Labor.objects.all()
                tipoLabor=TipoLabor.objects.all()
                lbselect = Labor.objects.get(id=labor_id)
                tipo_labor_id = lbselect.tl_id.pk
                tlselect = TipoLabor.objects.get(id=tipo_labor_id)
                return render(request, 'gestionarlabor.html',{'tl':tipoLabor,'labor':lb,'lbS':lbselect,'tlS':tlselect})    
        except :    
            return redirect('labor') 
    return redirect('labor')

@login_required
def gestionar_eva(request):
    if request.method == 'POST':
        try:
            if 'Guardar' in request.POST:
                perido_id=request.POST['periodo']
                docente_id=request.POST['rol']
                labor_id=request.POST['labor']
                    
                perido = Periodo.objects.get(id=perido_id)
                docente =  UserRol.objects.get(id=docente_id)
                labor = Labor.objects.get(id=labor_id)
                eva = Evaluacion.objects.create(
                    eva_estado = request.POST['estado'],
                    eva_puntaje = 0,
                    eva_resultado = 0,
                    userRol_id = docente,
                    per_id = perido,
                    lab_id = labor
                )
                eva.save()
                return redirect('gestionar_evaluacion')
            elif 'Eliminar' in request.POST:
                evaId = request.POST['evaluacion']
                try:
                    ev = Evaluacion.objects.get(id=evaId)
                    ev.delete()
                except Evaluacion.DoesNotExist:
                    pass
                return redirect('gestionar_evaluacion')
            elif 'Editar' in request.POST:
                perido_id=request.POST['periodo']
                docente_id=request.POST['rol']
                labor_id=request.POST['labor']
                evaId = request.POST['evaluacion']
                
                perido = Periodo.objects.get(id=perido_id)
                docente =  UserRol.objects.get(id=docente_id)
                labor = Labor.objects.get(id=labor_id)
                
                try:
                    ev = Evaluacion.objects.get(id=evaId)

                    ev.eva_estado=request.POST['estado']
                    ev.eva_puntaje=request.POST['puntaje']
                    ev.eva_resultado=request.POST['resultado']
                    ev.userRol_id = docente
                    ev.per_id=perido
                    ev.lab_id=labor
                    ev.save()
                    return redirect('gestionar_evaluacion')
                except Labor.DoesNotExist:
                    pass
                
            elif 'Buscar' in request.POST:
                eva_id = request.POST['evaluacion']
                evaSelect = Evaluacion.objects.get(id=eva_id)
                labor_id = evaSelect.lab_id.pk
                labSelect = Labor.objects.get(id=labor_id)
                per_id = evaSelect.per_id.pk
                perSelect = Periodo.objects.get(id=per_id)
                rol_id = per_id = evaSelect.userRol_id.pk
                rolSelect = UserRol.objects.get(id=rol_id)
                eva=Evaluacion.objects.all()
                perido=Periodo.objects.all()
                rolUser=UserRol.objects.all()
                lb = Labor.objects.all()
                
                return render(request, 'gestionarautoevaluacion.html',{"periodos":perido,"labors":lb,"userroles":rolUser,"evaluaciones":eva,"evaS":evaSelect,"labS":labSelect,"perS":perSelect,"rolS":rolSelect})   
        except :    
            return redirect('gestionar_evaluacion') 
    return redirect('gestionar_evaluacion')

    
@login_required
def gestionar_periodo(request):
    if request.method == 'POST':
        try:
                        
            if 'Guardar' in request.POST:
                fecha_inicio_str = request.POST['fecha_inicio']
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').replace(hour=0, minute=0, second=0)
                
                fecha_fin_str = request.POST['fecha_fin']
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
                print("xd")
                per = Periodo.objects.create(
                    nombre=request.POST['nombre'],
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin
                )
                per.save()
                
                return redirect('periodo')  
            elif 'Eliminar' in request.POST:
                perID = request.POST['buscar_periodo']
                try:
                    periodo = Periodo.objects.get(id=perID)
                    periodo.delete()
                except periodo.DoesNotExist:
                    pass
                return redirect('periodo')
            elif 'Editar' in request.POST:
                perID = request.POST['buscar_periodo']
                try:
                    
                    fecha_inicio_str = request.POST['fecha_inicio']
                    fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').replace(hour=0, minute=0, second=0)
                    
                    fecha_fin_str = request.POST['fecha_fin']
                    fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
                    
                    periodo = Periodo.objects.get(id=perID)
                    
                    periodo.nombre=request.POST['nombre']
                    periodo.fecha_inicio=fecha_inicio
                    periodo.fecha_fin=fecha_fin
                    periodo.save()
                    return redirect('periodo')
                except Labor.DoesNotExist:
                    pass
            elif 'Buscar' in request.POST:
                perID = request.POST['buscar_periodo']
                periodoSelect = Periodo.objects.get(id=perID)
                fIstr = periodoSelect.fecha_inicio.strftime('%Y-%m-%d')
                fFstr = periodoSelect.fecha_fin.strftime('%Y-%m-%d')
                prd=Periodo.objects.all()
                return render(request, 'gestionarPeriodo.html',{'periodos':prd,"perS":periodoSelect,"fI":fIstr,"fF":fFstr})   
        except :    
            return redirect('periodo') 
    return redirect('periodo')

@login_required
def gestionar_eva_doc(request):
    if request.method == 'POST':
        try:
            if 'Guardar' in request.POST:
                cambios = []
                for key in request.POST:
                    if key.startswith('cambios['):
                        indice = key.split('[', 1)[1].split(']')[0]
                        #if indice 
                        cambio = {
                            'id': request.POST[f'cambios[{indice}][id]'],
                            'estado': request.POST[f'cambios[{indice}][estado]'],
                            'resultado': request.POST[f'cambios[{indice}][resultado]'],
                            'puntaje': request.POST[f'cambios[{indice}][puntaje]']
                        }
                        cambios.append(cambio)
                
                print(cambios)
                for cambio in cambios:
                    evaluacion_id = cambio['id']
                    resultado = cambio['resultado']
                    puntaje = cambio['puntaje']
                    if cambio['estado'] == 'En ejecución':
                        
                        evaluacion = Evaluacion.objects.get(id=evaluacion_id)
                        evaluacion.eva_resultado = resultado
                     
                        evaluacion.eva_puntaje = puntaje
                        evaluacion.save()            
                return redirect('evaluacion')   
        except :    
            return redirect('evaluacion') 
    return redirect('evaluacion')

@login_required
def gestionar_user_rol(request):
    if request.method == 'POST':
        try:
                        
            if 'Guardar' in request.POST:
                userID = request.POST['usuario']
                userObj = User.objects.get(id=userID)
                rolID = request.POST['rol']
                rolObj = Rol.objects.get(id=rolID)
                uRol = UserRol.objects.create(
                    user = userObj,
                    rol = rolObj
                )
                uRol.save()
                
                return redirect('rol_view')  
            elif 'Eliminar' in request.POST:
                userRolID = request.POST['RolUsusario']
                try:
                    userRolSelect = UserRol.objects.get(id=userRolID)
                    userRolSelect.delete()
                except userRolSelect.DoesNotExist:
                    pass
                return redirect('rol_view')
            elif 'Editar' in request.POST:
                try:
                    userRolID = request.POST['RolUsusario']
                    userRolSelect = UserRol.objects.get(id=userRolID)
                    userID = request.POST['usuario']
                    userObj = User.objects.get(id=userID)
                    rolID = request.POST['rol']
                    rolObj = Rol.objects.get(id=rolID)

                    userRolSelect.user=userObj
                    userRolSelect.rol=rolObj
                    userRolSelect.save()
                    
                    return redirect('rol_view')
                except Labor.DoesNotExist:
                    pass
            elif 'Buscar' in request.POST:
                userRolID = request.POST['RolUsusario']
                userRolSelect = UserRol.objects.get(id=userRolID)
                usuario=UserDoc.objects.all()
                rol=Rol.objects.all()
                userRol=UserRol.objects.all()
                return render(request, 'asignarRoles.html',{'usuarios':usuario,'roles':rol,'rolusers':userRol,'urS':userRolSelect})   
        except :    
            return redirect('rol_view') 
    return redirect('rol_view')
