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

class UserDoc(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    genero = models.CharField(max_length=1)
    estudio = models.CharField(max_length=100)
    foto=models.TextField(blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):#cuando utilicen este modelo en string va a retornar el titulo
        return self.nombre 


class Rol(models.Model):    
    rol_descripcion = models.TextField(blank=True)
    
    def __str__(self):#cuando utilicen este modelo en string va a retornar el titulo
        return self.rol_descripcion

class UserRol(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol,on_delete=models.CASCADE)
    def __str__(self):#cuando utilicen este modelo en string va a retornar el titulo
        return self.user.username+"-"+self.rol.rol_descripcion


class TipoLabor(models.Model):
    codigo =models.IntegerField()
    descripcion = models.TextField(blank=True)
    def __str__(self):#cuando utilicen este modelo en string va a retornar el titulo
        return self.descripcion

class Labor(models.Model):
    nombre = models.TextField(max_length=100)
    horas = models.IntegerField()
    tl_id = models.ForeignKey(TipoLabor,on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):#cuando utilicen este modelo en string va a retornar el titulo
        return self.nombre 


class Periodo(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateTimeField(null=True,blank=True)
    fecha_fin = models.DateTimeField(null=True,blank=True)

    def __str__(self):#cuando utilicen este modelo en string va a retornar el titulo
        return self.nombre 

class Evaluacion(models.Model):
    eva_estado = models.CharField(max_length=100)
    eva_puntaje = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    eva_resultado = models.TextField(blank=True)
    userRol_id = models.ForeignKey(UserRol, on_delete=models.CASCADE)
    per_id = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    lab_id = models.ForeignKey(Labor, on_delete=models.CASCADE)
