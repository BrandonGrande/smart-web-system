import uuid
from django.db import models
from apps.appUsuario.models import User

class Enfermedad(models.Model):

	id_enfermedad=models.CharField(max_length=36,primary_key=True, unique=True,default=uuid.uuid4)
	nombreEnfermedad=models.CharField(max_length=30)
	tipoPatogeno=models.CharField(max_length=15)
	enfermedad=models.CharField(max_length=1000)
	control=models.CharField(max_length=1000)
	medidas=models.CharField(max_length=1000)
	user= models.CharField(max_length=30)

	class Meta:
		verbose_name='enfermedad'
		verbose_name_plural='enfermedades'

def obtener_ruta_validacion(instance, filename):
    return '{0}/{1}'.format("ImgValidacion/"+str(instance.enfermedad.id_enfermedad), filename)
def obtener_ruta_entrenamiento(instance, filename):
    return '{0}/{1}'.format("ImgEntrenamiento/"+str(instance.enfermedad.id_enfermedad), filename)

class ImgMuestra(models.Model):
	id_imagen=models.CharField(max_length=36,primary_key=True, unique=True,default=uuid.uuid4)
	enfermedad = models.ForeignKey(Enfermedad,on_delete=models.CASCADE)
	numero=models.IntegerField(default=None)
	image = models.FileField(upload_to = 'ImgMuestra/')

class ImgEntrenamiento(models.Model):
	id_imagen=models.CharField(max_length=36,primary_key=True, unique=True,default=uuid.uuid4)
	enfermedad = models.ForeignKey(Enfermedad, on_delete=models.CASCADE)
	image = models.FileField(upload_to =obtener_ruta_entrenamiento)

class ImgValidacion(models.Model):
	id_imagen=models.CharField(max_length=36,primary_key=True, unique=True,default=uuid.uuid4)
	enfermedad = models.ForeignKey(Enfermedad, on_delete=models.CASCADE)
	image = models.FileField(upload_to = obtener_ruta_validacion)







