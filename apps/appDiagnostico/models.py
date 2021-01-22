import uuid
from django.db import models 
from apps.appUsuario.models import User
from apps.appEnfermedades.models import Enfermedad

#Modelo diagnostico
class Diagnostico(models.Model):
	#Atributos del modelo diagnostico
	id_diagnostico=models.CharField(max_length=36,primary_key=True, unique=True,default=uuid.uuid4)
	imagen=models.ImageField(upload_to='diagnosticos')
	nombre=models.CharField(max_length=30)
	fecha=models.DateTimeField(auto_now_add=True)
	enfer= models.ForeignKey(Enfermedad, on_delete=models.CASCADE)
	user= models.ForeignKey(User, on_delete=models.CASCADE)
    #renombrado del modelo en base de datos
	class Meta:
		verbose_name='diagnostico'
		verbose_name_plural='diagnosticos'
    #retorno de valor id_diagnostico  
	def __str__(self):
		return self.id_diagnostico
    
class Prediccion(models.Model):
	id_prediccion=models.CharField(max_length=36,primary_key=True, unique=True,default=uuid.uuid4)
	clase=models.CharField(max_length=36)
	valor=models.FloatField()
	diagnostico=models.ForeignKey(Diagnostico,on_delete=models.CASCADE)