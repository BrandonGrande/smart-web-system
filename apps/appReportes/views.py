from django.shortcuts import render,redirect
from apps.appDiagnostico.models import Diagnostico,Prediccion
from apps.appEnfermedades.models import Enfermedad, ImgMuestra
from django.http import HttpResponse
from django.contrib import messages
import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required(login_url='ingresar')
def cargar_reportes(request):
   
    diagnosticos=Diagnostico.objects.filter(user=request.user).order_by('-fecha')
    enfermedades=Enfermedad.objects.all()
    cantidad=3
    mostrar=False
    if diagnosticos.count() > cantidad:
    	mostrar=True
    paginator= Paginator(diagnosticos,cantidad)
    page =request.GET.get('pagina',1)
    diagnosticos=paginator.get_page(page)

    if diagnosticos.has_next():
    	next_url=f'?pagina={diagnosticos.next_page_number()}'
    else:
    	next_url=''

    if diagnosticos.has_previous():
    	prev_url= f'?pagina={diagnosticos.previous_page_number()}'
    else:
    	prev_url=''

    return render(request,'appReportes/reportes.html',{'diagnosticos':diagnosticos,'enfermedades':enfermedades,'next_page_url':next_url,'prev_page_url':prev_url,'mostrar':mostrar})

@login_required(login_url='ingresar')
def cargar_reporte(request, id_diagnostico):
	try:
		diagnostico=Diagnostico.objects.get(id_diagnostico=id_diagnostico)
		enfermedad=Enfermedad.objects.get(id_enfermedad=diagnostico.enfer.id_enfermedad)
		imagenes_muestra=ImgMuestra.objects.filter(enfermedad=diagnostico.enfer.id_enfermedad)
		return render(request, 'appReportes/reporte.html',{'diagnostico':diagnostico,'enfermedad':enfermedad,'imagenesMuestra':imagenes_muestra})
	except:
		return redirect('cargar_reportes')

@login_required(login_url='ingresar')
def cargar_grafico(request):
	if request.method=='POST':
		id_diagnostico=request.POST.get('id_diagnostico')
		predicciones=Prediccion.objects.filter(diagnostico=id_diagnostico)
		pred_dic=[]
		for prediccion in predicciones:
			clase=prediccion.clase
			pre_enf=Enfermedad.objects.get(id_enfermedad=clase)
			nom_enf=pre_enf.nombreEnfermedad
			valor=prediccion.valor
			pred_dic.append({"name":nom_enf,"y":valor})
		data=json.dumps(pred_dic)
		return HttpResponse(data,'application/json')

	return redirect('cargar_reportes')

@login_required(login_url='ingresar')
def eliminar_reporte_diagnostico(request,id_diagnostico):
	if request.method=='POST':
		diagnostico=Diagnostico.objects.get(id_diagnostico=id_diagnostico)
		try:
			diagnostico.delete()
			messages.success(request,"¡Reporte eliminado con exito!")
		except:
			messages.error(request,"Error al eliminar el reporte")

	return redirect('cargar_reportes')

@login_required(login_url='ingresar')
def modificar_reporte_diagnostico(request,id_diagnostico):
	if request.method=='POST':
		diagnostico=Diagnostico.objects.get(id_diagnostico=id_diagnostico)
		try:
			diagnostico.nombre=request.POST.get('nombreReporte')
			diagnostico.save()
			messages.success(request,"¡Reporte modificado con exito!")
		except:
			messages.error(request,"Error al modificar el reporte")

	return redirect('cargar_reportes')
