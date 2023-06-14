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

class Usuario(models.Model):
    apellido = apellido
    genero = genero
    estudio = estudio
    correo = correo
    contrasenia = contrasenia


    class Labor:
        def __init__(self, id_labor, nombre, horas, tipo, descripcion):
            self.id_labor = id_labor
            self.nombre = nombre
            self.horas = horas
            self.tipo = tipo
            self.descripcion = descripcion


    class Periodo:
        def __init__(self, id_periodo, nombre, fecha_inicio, fecha_fin):
            self.id_periodo = id_periodo
            self.nombre = nombre
            self.fecha_inicio = fecha_inicio
            self.fecha_fin = fecha_fin


    class Docente(Usuario):
        def __init__(self, id_usuario, apellido, genero, estudio, correo, contrasenia, estado, horas, materias, tipo_ocupacion):
            super().__init__(id_usuario, apellido, genero, estudio, correo, contrasenia)
            self.estado = estado
            self.horas = horas
            self.materias = materias
            self.tipo_ocupacion = tipo_ocupacion
    

    class Coordinador(Docente):
        def __init__(self, id_usuario, apellido, genero, estudio, correo, contrasenia, estado, horas, materias, tipo_ocupacion):
            super().__init__(id_usuario, apellido, genero, estudio, correo, contrasenia, estado, horas, materias, tipo_ocupacion)
    

class Decano(Docente):
    def __init__(self, id_usuario, apellido, genero, estudio, correo, contrasenia, estado, horas, materias, tipo_ocupacion):
        super().__init__(id_usuario, apellido, genero, estudio, correo, contrasenia, estado, horas, materias, tipo_ocupacion)


class Evaluacion:
    def __init__(self, id_evaluacion, estado, puntaje, resultado):
        self.id_evaluacion = id_evaluacion
        self.estado = estado
        self.puntaje = puntaje
        self.resultado = resultado
            