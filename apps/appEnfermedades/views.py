#Librerias y funciones
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test,login_required
from apps.appEnfermedades.models import Enfermedad, ImgMuestra, ImgEntrenamiento, ImgValidacion
from apps.appReentrenamiento.models import Reentrenamiento,Clase
from django.contrib import messages
import json
import os
from django.http import HttpResponse
from django.conf import settings
from django.core.paginator import Paginator
from django.conf import settings

@login_required(login_url='ingresar')
@user_passes_test(lambda u: u.is_superuser)
#Funcion para cargar lista de enfermedades
def cargar_enfermedades(request):
    #Objetos de enfermedades
    enfermedades=Enfermedad.objects.all()
    #Imagenes de muestra enfermedades
    imagenes_muestra=ImgMuestra.objects.all()
    #Retornar la vista de enfermedades

    reentrenamiento=Reentrenamiento.objects.filter(estado=True)
    clases=''
    if reentrenamiento:
        clases=Clase.objects.filter(reentrenamiento=reentrenamiento[0].id_reentrenamiento)

    cantidad=3
    mostrar=False
    if enfermedades.count() > cantidad:
        mostrar=True
    paginator= Paginator(enfermedades,cantidad)
    page =request.GET.get('pagina',1)
    enfermedades=paginator.get_page(page)

    if enfermedades.has_next():
        next_url=f'?pagina={enfermedades.next_page_number()}'
    else:
        next_url=''

    if enfermedades.has_previous():
        prev_url= f'?pagina={enfermedades.previous_page_number()}'
    else:
        prev_url=''


    return render(request,'appEnfermedades/enfermedades.html',{"enfermedades":enfermedades,'imagenesMuestra':imagenes_muestra,'next_page_url':next_url,'prev_page_url':prev_url,'clases':clases,'mostrar':mostrar})

#Validacion de cuenta(Administrador)
@login_required(login_url='ingresar')
@user_passes_test(lambda u: u.is_superuser)
def crear_enfermedad(request):
    #Valida si la peticion es POST
    if request.method == 'POST':
        #Inicializa un objeto Enfermedad para guardar los datos
        enfermedad=Enfermedad()
        enfermedad.user=str(request.user.first_name).capitalize()+" "+str(request.user.last_name).capitalize()
        enfermedad.nombreEnfermedad = request.POST.get('nombreEnfermedad')
        enfermedad.tipoPatogeno = request.POST.get('tipoPatogeno')
        enfermedad.enfermedad = request.POST.get('infoEnfermedad')
        enfermedad.control = request.POST.get('infoControl')
        enfermedad.medidas = request.POST.get('medidasPreventivas')
        #Manejo de errores mediante Try-Except
        try:
            #Se guarda la enfermedad en la base de datos
            enfermedad.save()
            #Se guardan las imagenes de muestra en la base de datos
            for img in range(0, int(request.POST.get('lengthMuestra'))):
                img_muestra=ImgMuestra()
                img_muestra.enfermedad=enfermedad
                img_muestra.numero=img
                img_muestra.image=request.FILES.get(f'muestra{img}')
                img_muestra.save()
            #Se guardan las imagenes de entrenamiento en la base de datos
            for img in range(0, int(request.POST.get('lengthEntrenamiento'))):
                img_entrenamiento=ImgEntrenamiento()
                img_entrenamiento.enfermedad=enfermedad
                img_entrenamiento.image=request.FILES.get(f'entrenamiento{img}')
                img_entrenamiento.save()
            #Se guardan las imagenes de validacion en la base de datos
            for img in range(0, int(request.POST.get('lengthValidacion'))):
                img_validacion=ImgValidacion()
                img_validacion.enfermedad=enfermedad
                img_validacion.image=request.FILES.get(f'validacion{img}')
                img_validacion.save()
            #Se retorna un mensaje de exito en formato json
            data=json.dumps(messages.success(request,"Enfermedad registrada con exito"))
            return HttpResponse(data,'application/json')


        except:
            #Se setorna una mensaje de error en formato json
            data=json.dumps(messages.error(request,"Error registrar la enfermedad"))
            return HttpResponse(data,'application/json')

    return render(request,'appEnfermedades/registrarEnfermedad.html')






@login_required(login_url='ingresar')
def consultar_enfermedad(request, id_enfermedad):
    try:
        enfermedad=Enfermedad.objects.get(id_enfermedad=id_enfermedad)
        imagenes_muestra=ImgMuestra.objects.filter(enfermedad=id_enfermedad)
        cantidad_entrenamiento=ImgEntrenamiento.objects.filter(enfermedad=id_enfermedad).count()
        cantidad_validacion=ImgValidacion.objects.filter(enfermedad=id_enfermedad).count()
        return render(request,'appEnfermedades/enfermedad.html',{"enfermedad":enfermedad,'imagenesMuestra':imagenes_muestra, 'cantidadEntrenamiento':cantidad_entrenamiento, 'cantidadValidacion':cantidad_validacion})
    except:
        return redirect('cargar_principal')

@login_required(login_url='ingresar')
@user_passes_test(lambda u: u.is_superuser)
def modificar_enfermedad(request, id_enfermedad):
    try:
        enfermedad=Enfermedad.objects.get(id_enfermedad=id_enfermedad)
        imagenes_muestra=ImgMuestra.objects.filter(enfermedad=id_enfermedad)
    except:
        return redirect('cargar_enfermedades')

    if request.method == 'POST':

        enfermedad.user=request.user.username
        enfermedad.nombreEnfermedad = request.POST.get('nombreEnfermedad')
        enfermedad.tipoPatogeno = request.POST.get('tipoPatogeno')
        enfermedad.enfermedad = request.POST.get('infoEnfermedad')
        enfermedad.control = request.POST.get('infoControl')
        enfermedad.medidas = request.POST.get('medidasPreventivas')
        try:
            enfermedad.save()
            messages.success(request,"Enfermedad modificada con exito")
        except:
            messages.error(request,"Error al modificar la enfermedad")

    return render(request,'appEnfermedades/modificarEnfermedad.html',{"enfermedad":enfermedad,'imagenesMuestra':imagenes_muestra})


@login_required(login_url='ingresar')
@user_passes_test(lambda u: u.is_superuser)
def modificar_imagenes_muestra(request):

    if request.method == 'POST':
        id_enfermedad= request.POST.get('idEnfermedad')
        imagenes_muestra=ImgMuestra.objects.filter(enfermedad=id_enfermedad)
        enfermedad=Enfermedad.objects.get(id_enfermedad=id_enfermedad)
        try:
            imagenes_muestra.delete()
            for img in range(0, int(request.POST.get('lengthMuestra'))):
                img_muestra=ImgMuestra()
                img_muestra.enfermedad=enfermedad
                img_muestra.numero=img
                img_muestra.image=request.FILES.get(f'muestra{img}')
                img_muestra.save()

            data=json.dumps({'id_enfermedad':id_enfermedad,'messages':messages.success(request,"Imágenes de muestra modificadas con exito")})
        except:
            data=json.dumps({'id_enfermedad':id_enfermedad,'messages':messages.error(request,"Error al modificar las imágenes de muestra")})

    return HttpResponse(data,'application/json')

@login_required(login_url='ingresar')
@user_passes_test(lambda u: u.is_superuser)
def modificar_carpeta_validacion(request):

    if request.method == 'POST':
        id_enfermedad= request.POST.get('idEnfermedad')
        imagenes_validacion=ImgValidacion.objects.filter(enfermedad=id_enfermedad)
        enfermedad=Enfermedad.objects.get(id_enfermedad=id_enfermedad)
        try:
        
            imagenes_validacion.delete()

            for img in range(0, int(request.POST.get('lengthValidacion'))):
                img_validacion=ImgValidacion()
                img_validacion.enfermedad=enfermedad
                img_validacion.image=request.FILES.get(f'validacion{img}')
                img_validacion.save()

            data=json.dumps({'id_enfermedad':id_enfermedad,'messages':messages.success(request,"Carpetas de imágenes de validacion modificadas con exito")})
        except:
            data=json.dumps({'id_enfermedad':id_enfermedad,'messages':messages.error(request,"Error al modificar la carpeta de imágenes de validacion")})

    return HttpResponse(data,'application/json')

@login_required(login_url='ingresar')
@user_passes_test(lambda u: u.is_superuser)
def modificar_carpeta_entrenamiento(request):

    if request.method == 'POST':
        id_enfermedad= request.POST.get('idEnfermedad')
        imagenes_entrenamiento=ImgEntrenamiento.objects.filter(enfermedad=id_enfermedad)
        enfermedad=Enfermedad.objects.get(id_enfermedad=id_enfermedad)
        
        try:
            imagenes_entrenamiento.delete()
    
            for img in range(0, int(request.POST.get('lengthEntrenamiento'))):
                img_entrenamiento=ImgEntrenamiento()
                img_entrenamiento.enfermedad=enfermedad
                img_entrenamiento.image=request.FILES.get(f'entrenamiento{img}')
                img_entrenamiento.save()

            data=json.dumps({'id_enfermedad':id_enfermedad,'messages':messages.success(request,"Carpetas de imágenes de entrenamiento modificadas con exito")})
        except:
            data=json.dumps({'id_enfermedad':id_enfermedad,'messages':messages.error(request,"Error al modificar la carpeta de imágenes de entrenamiento")})

    return HttpResponse(data,'application/json')

@login_required(login_url='ingresar')
@user_passes_test(lambda u: u.is_superuser)
def eliminar_enfermedad(request,id_enfermedad):
    if request.method=='POST':
        enfermedad=Enfermedad.objects.get(id_enfermedad=id_enfermedad)
        id_enfermedad=enfermedad.id_enfermedad
        try:
            enfermedad.delete()
            eliminar_carpetas_vacias()
            reentrenamiento=Reentrenamiento.objects.filter(estado=True)
            if reentrenamiento:
                clase=Clase.objects.filter(nombre=id_enfermedad)
                if clase:
                    Reentrenamiento.objects.all().update(estado=False)
                    dir_mod =os.path.join(settings.BASE_DIR, 'modelo_red_neuronal/modelo.h5')
                    dir_pes = os.path.join(settings.BASE_DIR, 'modelo_red_neuronal/pesos.h5')
                    if os.path.exists(dir_mod):
                        os.remove(dir_mod)
                    if os.path.exists(dir_pes):
                        os.remove(dir_pes)

            messages.success(request,"Enfermedad eliminada con exito")
        except:
            messages.error(request,"Error al eliminar la enfermedad")

    return redirect('cargar_enfermedades')


def eliminar_carpetas_vacias():
    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
        for d in dirs:
            dir = os.path.join(root, d)
            if not os.listdir(dir):
                os.rmdir(dir)

