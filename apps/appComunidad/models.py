import uuid
from django.db import models 
from apps.appUsuario.models import User

#Modelo pregunta
class Pregunta(models.Model):
	#Atributos del modelo pregunta
	id_pregunta=models.CharField(max_length=36,primary_key=True, unique=True,default=uuid.uuid4)
	descripcion=models.CharField(max_length=500)
	imagen=models.ImageField(upload_to='preguntas')
	fecha=models.DateTimeField(auto_now_add=True)
	user= models.ForeignKey(User, on_delete=models.CASCADE)
    #renombrado del modelo en base de datos
	class Meta:
		verbose_name='pregunta'
		verbose_name_plural='preguntas'
    #retorno de valor id_pregunta 
	def __str__(self):
		return self.id_pregunta

class Respuesta(models.Model):
	#Atributos del modelo respuesta
	id_respuesta=models.CharField(max_length=36,primary_key=True, unique=True,default=uuid.uuid4)
	descripcion=models.CharField(max_length=500)
	fecha=models.DateTimeField(auto_now_add=True)
	user= models.ForeignKey(User, on_delete=models.CASCADE)
	pregunta= models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    #renombrado del modelo en base de datos
	class Meta:
		verbose_name='respuesta'
		verbose_name_plural='respuestas'
    #retorno de valor id_respuesta  
	def __str__(self):
		return self.id_respuesta

