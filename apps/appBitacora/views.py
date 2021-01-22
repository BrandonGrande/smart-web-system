from django.shortcuts import render,redirect
from apps.appReentrenamiento.models import Reentrenamiento,Error,Calidad,Clase
from django.db.models import Avg
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
import os
from django.core.paginator import Paginator
from django.conf import settings

@login_required(login_url='ingresar')
@user_passes_test(lambda u: u.is_superuser)
def cargar_reporte_reentrenamiento(request,id_reentrenamiento):
    try:
        reentrenamiento=Reentrenamiento.objects.get(id_reentrenamiento=id_reentrenamiento)
        clases=Clase.objects.filter(reentrenamiento=id_reentrenamiento)
        errores=Error.objects.filter(reentrenamiento=id_reentrenamiento).order_by('epoca')
        calidades=Calidad.objects.filter(reentrenamiento=id_reentrenamiento).order_by('epoca')
        promedio_error=Error.objects.filter(reentrenamiento=id_reentrenamiento).aggregate(Avg('valor'))
        promedio_calidad=Calidad.objects.filter(reentrenamiento=id_reentrenamiento).aggregate(Avg('valor'))
        lista_errores=[]
        for error in errores:
            lista_errores.append(error.valor)
        lista_calidad=[]
        for calidad in calidades:
            lista_calidad.append(calidad.valor)
        return render(request,'appBitacora/reporte.html',{'reentrenamiento':reentrenamiento,'clases':clases,'errores':lista_errores,'calidad':lista_calidad,'promedio_error':promedio_error['valor__avg'],'promedio_calidad':promedio_calidad['valor__avg']})
    except:
        return redirect('cargar_bitacora')

@login_required(login_url='ingresar')
@user_passes_test(lambda u: u.is_superuser)
def cargar_bitacora(request):
    reentrenamientos=Reentrenamiento.objects.all().order_by('-fecha')
    cantidad=3
    mostrar=False
    if reentrenamientos.count() > cantidad:
        mostrar=True
    paginator= Paginator(reentrenamientos,cantidad)
    page =request.GET.get('pagina',1)
    reentrenamientos=paginator.get_page(page)

    if reentrenamientos.has_next():
        next_url=f'?pagina={reentrenamientos.next_page_number()}'
    else:
        next_url=''

    if reentrenamientos.has_previous():
        prev_url= f'?pagina={reentrenamientos.previous_page_number()}'
    else:
        prev_url=''
    return render(request,'appBitacora/reportes.html',{'reentrenamientos':reentrenamientos,'next_page_url':next_url,'prev_page_url':prev_url,'mostrar':mostrar})


@login_required(login_url='ingresar')
@user_passes_test(lambda u: u.is_superuser)
def eliminar_reentrenamiento(request,id_reentrenamiento):
    if request.method=="POST":
        reentrenamiento=Reentrenamiento.objects.get(id_reentrenamiento=id_reentrenamiento)
        try:
            if reentrenamiento.estado:
                dir_mod =os.path.join(settings.BASE_DIR, 'modelo_red_neuronal/modelo.h5')
                dir_pes = os.path.join(settings.BASE_DIR, 'modelo_red_neuronal/pesos.h5')

                if os.path.exists(dir_mod):
                    os.remove(dir_mod)
                if os.path.exists(dir_pes):
                    os.remove(dir_pes)

            reentrenamiento.delete()
            messages.success(request,"¡Reentrenamiento eliminado con exito!")
        except:
            messages.error(request,"Error al eliminar el reentrenamiento")

    return redirect('cargar_bitacora')


@login_required(login_url='ingresar')
@user_passes_test(lambda u: u.is_superuser)
def modificar_reentrenamiento(request,id_reentrenamiento):

    if request.method=="POST":
        reentrenamiento=Reentrenamiento.objects.get(id_reentrenamiento=id_reentrenamiento)
        try:
            reentrenamiento.nombre=request.POST.get('nombreReentrenamiento')
            reentrenamiento.save()

            messages.success(request,"¡Reentrenamiento modificado con exito!")
        except:
            messages.error(request,"Error al modificar el reentrenamiento")

    return redirect('cargar_bitacora')


