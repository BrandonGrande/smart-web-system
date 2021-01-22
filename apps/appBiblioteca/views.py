from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from apps.appEnfermedades.models import Enfermedad,ImgMuestra,ImgEntrenamiento,ImgValidacion
import json
from django.contrib.auth.decorators import login_required

@login_required(login_url='ingresar')
def cargar_biblioteca(request):

	if request.method=='POST':

		nombre=request.POST.get('nombreEnfermedad')
		tipo=request.POST.get('tipoPatogeno')
		if tipo:

			enfermedades=Enfermedad.objects.filter(nombreEnfermedad__icontains=nombre,tipoPatogeno=tipo)
		else:
			enfermedades=Enfermedad.objects.filter(nombreEnfermedad__icontains=nombre)

		imagenes_muestra=ImgMuestra.objects.all()

		lista_enf=[]
		for enfermedad in enfermedades:
			informacion=enfermedad.enfermedad
			nombre=enfermedad.nombreEnfermedad
			tipo=enfermedad.tipoPatogeno
			imagenes=ImgMuestra.objects.filter(enfermedad=enfermedad.id_enfermedad)
			imagen=imagenes[0].image.url
			id_enfermedad=enfermedad.id_enfermedad
			lista_enf.append({'id_enfermedad':id_enfermedad, 'nombre':nombre,'tipoPatogeno':tipo,'informacion':informacion[0:100],'imagen':imagen})

		resultados=len(lista_enf)
		data=json.dumps({'enfermedades':lista_enf,'resultados':resultados})

		return HttpResponse(data,'application/json')





	return render(request,'appBiblioteca/biblioteca.html')
