from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
import json
from django.http import HttpResponse
from apps.appEnfermedades.models import Enfermedad, ImgEntrenamiento, ImgValidacion
from apps.appReentrenamiento.entrenamiento import entrenamiento_red_neuronal
from apps.appReentrenamiento.models import Reentrenamiento,Clase,Error,Calidad
from datetime import datetime


@login_required(login_url='ingresar')
@user_passes_test(lambda u: u.is_superuser)
def cargar_reentrenamiento(request):
    enfermedades=Enfermedad.objects.all()
    listaEnfermedades=[]
    for enfermedad in enfermedades:
        cantidadValidacion=ImgValidacion.objects.filter(enfermedad=enfermedad.id_enfermedad).count()
        cantidadEntrenamiento=ImgEntrenamiento.objects.filter(enfermedad=enfermedad.id_enfermedad).count()
        id_enfermedad=enfermedad.id_enfermedad
        nombreEnfermedad=enfermedad.nombreEnfermedad
        listaEnfermedades.append({'id_enfermedad':id_enfermedad,'nombreEnfermedad':nombreEnfermedad,'cantidadEntrenamiento':cantidadEntrenamiento, 'cantidadValidacion':cantidadValidacion})
    return render(request, 'appReentrenamiento/reentrenamiento.html',{'listaEnfermedades':listaEnfermedades})

@login_required(login_url='ingresar')
@user_passes_test(lambda u: u.is_superuser)
def reentrenar_red_neuronal(request):

	if request.method == 'POST':
		num_enfermedades=Enfermedad.objects.all().count()
		num_filtro1=request.POST.get('numFiltro1')
		num_filtro2=request.POST.get('numFiltro2')
		num_epocas=request.POST.get('numEpocas')
		

		try:
			datos=entrenamiento_red_neuronal( int(num_filtro1),int(num_filtro2),int(num_epocas),num_enfermedades)	
			Reentrenamiento.objects.all().update(estado=False)
			reentrenamiento=Reentrenamiento()
			id_reentrenamiento=reentrenamiento.id_reentrenamiento
			fecha=datetime.now()
			fecha=fecha.strftime("%d%m%y")
			reentrenamiento.nombre='Reentrenamiento '+str(fecha)
			reentrenamiento.num_filtro1=num_filtro1
			reentrenamiento.num_filtro2=num_filtro2
			reentrenamiento.num_epocas=num_epocas
			reentrenamiento.funcion_activacion="Relu y Softmax"
			reentrenamiento.user=str(request.user.first_name).capitalize()+" "+str(request.user.last_name).capitalize()
			reentrenamiento.save()
			for dato in datos['clases'].items():
				clase_re=Clase()
				clase_re.nombre=dato[0]
				enfermedad_clase=Enfermedad.objects.get(id_enfermedad=dato[0])
				clase_re.nombre_enfermedad=enfermedad_clase.nombreEnfermedad
				clase_re.num_clase=dato[1]
				clase_re.reentrenamiento=reentrenamiento
				clase_re.save()
			epoca=1
			for dato in datos['error']:
				error_re=Error()
				error_re.valor=dato
				error_re.epoca=epoca
				error_re.reentrenamiento=reentrenamiento
				error_re.save()
				epoca=epoca+1
			epoca=1
			for dato in datos['calidad']:
				calidad_re=Calidad()
				calidad_re.valor=dato
				calidad_re.epoca=epoca
				calidad_re.reentrenamiento=reentrenamiento
				calidad_re.save()
				epoca=epoca+1

			data=json.dumps({'id_reentrenamiento':str(id_reentrenamiento),'messages':messages.success(request,"¡Red neuronal reentrenada con exito!")})
		except:
		    data=json.dumps({'id_reentrenamiento':None,'messages':messages.error(request,"Error al reentrenar la red neuronal")})

		return HttpResponse(data,'application/json')

	return redirect('cargar_reentrenamiento')
