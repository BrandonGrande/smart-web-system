
from django.shortcuts import render, redirect
from apps.appDiagnostico.models import Diagnostico,Prediccion
from apps.appDiagnostico.prediccion import prediccion
from django.urls import reverse
from apps.appEnfermedades.models import Enfermedad
from django.contrib import messages
from apps.appReentrenamiento.models import Reentrenamiento,Clase
import os
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.conf import settings


@login_required(login_url='ingresar')
def cargar_diagnostico(request):



    if request.method == 'POST':
        dir_mod =os.path.join(settings.BASE_DIR, 'modelo_red_neuronal/modelo.h5')
        dir_pes = os.path.join(settings.BASE_DIR, 'modelo_red_neuronal/pesos.h5')
        reentrenamiento=Reentrenamiento.objects.filter(estado=True)
        if reentrenamiento and ( os.path.exists(dir_mod) and os.path.exists(dir_pes) ):

            diagnostico = Diagnostico()
            imagen = request.FILES.get('imagenDiagnostico')
            diagnostico.imagen = imagen
            resultados = prediccion(imagen)
            clase=Clase.objects.get(num_clase=resultados['clase'][0],reentrenamiento=reentrenamiento[0].id_reentrenamiento)
            enfermedad=Enfermedad.objects.get(id_enfermedad=clase.nombre)
            fecha=datetime.now()
            fecha=fecha.strftime("%d%m%y")
            diagnostico.nombre='Diagnostico '+str(fecha)
            diagnostico.enfer=enfermedad
            diagnostico.user = request.user
            diagnostico.save()
            posicion=0
            for prob in resultados['probabilidades']:
                for val in prob:
                    predicion_enfermedad=Prediccion()
                    clase=Clase.objects.get(num_clase=posicion,reentrenamiento=reentrenamiento[0].id_reentrenamiento)
                    predicion_enfermedad.clase=clase.nombre
                    predicion_enfermedad.valor=val
                    predicion_enfermedad.diagnostico=diagnostico
                    predicion_enfermedad.save()
                    posicion=posicion+1

            id_diagnostico=str(diagnostico.id_diagnostico)

            return redirect(reverse('cargar_reporte', kwargs={"id_diagnostico": id_diagnostico}))
        else:
            messages.error(request,"El diagnóstico aún no esta disponible")
            return redirect('cargar_diagnostico')




    return render(request, 'appDiagnostico/diagnostico.html')







