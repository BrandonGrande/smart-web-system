import uuid
from django.db import models 
from apps.appUsuario.models import User

#Modelo pregunta
class Reentrenamiento(models.Model):
	id_reentrenamiento=models.CharField(max_length=36,primary_key=True, unique=True,default=uuid.uuid4)
	nombre=models.CharField(max_length=30)
	fecha=models.DateTimeField(auto_now_add=True)
	num_filtro1=models.IntegerField()
	num_filtro2=models.IntegerField()
	num_epocas=models.IntegerField()
	funcion_activacion=models.CharField(max_length=20)
	estado = models.BooleanField(default=True)
	user= models.CharField(max_length=30)


class Clase(models.Model):
	id_clase=models.CharField(max_length=36,primary_key=True, unique=True,default=uuid.uuid4)
	nombre=models.CharField(max_length=36)
	nombre_enfermedad=models.CharField(max_length=40)
	num_clase=models.IntegerField()
	reentrenamiento= models.ForeignKey(Reentrenamiento, on_delete=models.CASCADE)


class Error(models.Model):
	id_error=models.CharField(max_length=36,primary_key=True, unique=True,default=uuid.uuid4)
	valor=models.FloatField()
	epoca=models.IntegerField()
	reentrenamiento= models.ForeignKey(Reentrenamiento, on_delete=models.CASCADE)

class Calidad(models.Model):
	id_calidad=models.CharField(max_length=36,primary_key=True, unique=True,default=uuid.uuid4)
	valor=models.FloatField()
	epoca=models.IntegerField()
	reentrenamiento= models.ForeignKey(Reentrenamiento, on_delete=models.CASCADE)
