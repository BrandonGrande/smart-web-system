from django.shortcuts import render
from apps.appDiagnostico.models import Diagnostico
from apps.appComunidad.models import Pregunta
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required(login_url='ingresar')
def cargar_principal(request):
    
    diagnosticos=Diagnostico.objects.filter(user=request.user)[:3]
    preguntas=Pregunta.objects.filter(user=request.user).order_by('-fecha')
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

    return render(request, 'appPrincipal/principalProductor.html',{'diagnosticos':diagnosticos, 'preguntas':preguntas,'next_page_url':next_url,'prev_page_url':prev_url,'mostrar':mostrar})


@login_required(login_url='ingresar')
def cargar_configuracion(request):

    return render(request, 'appPrincipal/configuracionProductor.html')

