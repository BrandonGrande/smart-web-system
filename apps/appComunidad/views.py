#Librerias y modelos 
from django.shortcuts import render
from apps.appComunidad.models import Pregunta,Respuesta
from django.shortcuts import redirect
from django.http import HttpResponse
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required(login_url='ingresar')
def cargar_comunidad(request):
    
    preguntas=Pregunta.objects.order_by('-fecha')
    cantidad=4
    mostrar=False
    if preguntas.count() > cantidad:
        mostrar=True
    paginator= Paginator(preguntas,cantidad)
    page =request.GET.get('pagina',1)
    preguntas=paginator.get_page(page)

    if preguntas.has_next():
        next_url=f'?pagina={preguntas.next_page_number()}'
    else:
        next_url=''

    if preguntas.has_previous():
        prev_url= f'?pagina={preguntas.previous_page_number()}'
    else:
        prev_url=''

    return render(request,'appComunidad/comunidad.html',{'preguntas':preguntas,'next_page_url':next_url,'prev_page_url':prev_url,'mostrar':mostrar})

@login_required(login_url='ingresar')
def crear_pregunta(request,id_vista):
    
    if request.method == 'POST':
        pregunta = Pregunta()
        pregunta.user = request.user
        pregunta.imagen = request.FILES.get('imagenPregunta')
        pregunta.descripcion=request.POST.get('descripcionPregunta')    
        try:
            pregunta.save()
        except:
            messages.error(request,"Error al crear la pregunta")
            
    if(id_vista=='1'):
         return redirect ('cargar_principal')
    return redirect ('cargar_comunidad')

@login_required(login_url='ingresar')
def eliminar_pregunta(request,id_pregunta,id_vista):
    
    if request.method=='POST':
        pregunta=Pregunta.objects.get(id_pregunta=id_pregunta)
        try:
            pregunta.delete()
        except:
            messages.error(request,"Error al eliminar la pregunta")

    if(id_vista=='1'):
        return redirect ('cargar_principal')
    elif(id_vista=='3'):
        return redirect('cargar_pregunta',id_pregunta)
    return redirect ('cargar_comunidad')

@login_required(login_url='ingresar')
def modificar_pregunta(request,id_pregunta,id_vista):

    if request.method == 'POST': 
        pregunta=Pregunta.objects.get(id_pregunta=id_pregunta)
        if request.FILES.get('imagenPregunta'):
            pregunta.imagen = request.FILES.get('imagenPregunta')
        pregunta.descripcion=request.POST.get('descripcionPregunta')    
        try:
            pregunta.save()
        except:
            messages.error(request,"Error al modificar la pregunta")
           
    
    if(id_vista=='1'):
        return redirect ('cargar_principal')
    elif(id_vista=='3'):
        return redirect('cargar_pregunta',id_pregunta)
    return redirect ('cargar_comunidad')


@login_required(login_url='ingresar')
def cargar_pregunta(request,id_pregunta):
    try:
        pregunta=Pregunta.objects.get(id_pregunta=id_pregunta)
        respuestas=Respuesta.objects.filter(pregunta=pregunta).order_by('fecha')
        return render(request,'appComunidad/pregunta.html',{'pregunta':pregunta,'respuestas':respuestas})
    except:
        return redirect('cargar_comunidad')


@login_required(login_url='ingresar')
def crear_respuesta(request,id_pregunta):
   
    if request.method == 'POST':
        respuesta = Respuesta()
        respuesta.descripcion=request.POST.get('descripcionRespuesta') 
        respuesta.user = request.user
        pregunta=Pregunta.objects.get(id_pregunta=id_pregunta)
        respuesta.pregunta= pregunta   
        try:
            respuesta.save()
        except:
            messages.error(request,"Error al crear respuesta")

    return redirect ('cargar_pregunta',id_pregunta)

@login_required(login_url='ingresar')
def modificar_respuesta(request,id_respuesta):
    if request.method == 'POST':
        id_pregunta=request.POST.get('id_pregunta')
        respuesta=Respuesta.objects.get(id_respuesta=id_respuesta)
        respuesta.descripcion=request.POST.get('descripcionRespuesta')
        try:
            respuesta.save()
        except:
            messages.error(request,"Error al modificar respuesta")
        return redirect('cargar_pregunta',id_pregunta)
    return redirect('cargar_comunidad')

@login_required(login_url='ingresar')
def eliminar_respuesta(request,id_respuesta):
    if request.method=='POST':
        id_pregunta=request.POST.get('id_pregunta')
        respuesta=Respuesta.objects.get(id_respuesta=id_respuesta)
        try:
            respuesta.delete()
        except:
            messages.error(request,"Error al eliminar respuesta")

        return redirect('cargar_pregunta',id_pregunta)
    return redirect('cargar_comunidad')



    


