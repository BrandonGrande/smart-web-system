from apps.appUsuario.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.urls import reverse_lazy
from apps.appUsuario.forms import registro_form
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required


def iniciar_sesion(request):
    if request.method =="POST":
        form =AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            email = request.POST['username']
            contrasenia = request.POST['password']
            user=authenticate(username=email,password=contrasenia)
            if user is not None:
                login(request,user)
                return redirect("cargar_principal")
            else:
                messages.error(request,"Email o contraseña incorrectos")
                return redirect("ingresar")
        else:
            messages.error(request,"Email o contraseña incorrectos")
            return redirect("ingresar")

    return render(request,'appUsuario/ingresar.html')

@login_required(login_url='ingresar')
def cerrar_sesion(request):
    logout(request)
    return redirect('ingresar')


def registro_usuario(request):

    if request.method =="POST":
        form= registro_form(request.POST)
        if form.is_valid():
            usuario=form.save()
            messages.success(request,"¡Bienvenido "+usuario.first_name+"!")
            login(request,usuario)
            return redirect("cargar_principal")
        else:
            for msg in form.errors:
                messages.error(request,form.errors[msg])
            return redirect("registrar_usuario")

    return render(request, 'appUsuario/registrarUsuario.html')


@login_required(login_url='ingresar')
def modificar_imgPrincipal(request):
    usuario=request.user
    if request.method == 'POST':

        if request.FILES.get('imgPrincipalEditar'):

            usuario.image = request.FILES.get('imgPrincipalEditar')
        try:

            usuario.save()
            messages.success(request,"¡Imagen modificada con exito!")
        except:
            messages.error(request,"Error al modificar la imagen")


    return redirect ('cargar_principal')

@login_required(login_url='ingresar')
def modificar_informacion(request):

    usuario=request.user

    if request.method=='POST':
        if request.FILES.get('image'):
            usuario.image = request.FILES.get('image')
        usuario.first_name=request.POST.get('first_name')
        usuario.last_name=request.POST.get('last_name')
        usuario.username=request.POST.get('username')
        usuario.email=request.POST.get('email')
        try:
            usuario.save()
            messages.success(request,"¡Informacion modificada con exito!")
        except:
            messages.error(request,"Error al modificar los datos")
            if(User.objects.filter(email=request.user.email).exists()):
                messages.error(request,"El correo electronico ya se encuentra registrado en otra cuenta")


    return redirect ('cargar_configuracion')

@login_required(login_url='ingresar')
def modificar_contrasenia(request):

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            try:
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request,"¡Contraseña modificada con exito!")
            except:
                messages.error(request,"Error al modificar la contraseña")
        else:
            for msg in form.errors:
                messages.error(request,form.errors[msg])

    return redirect ('cargar_configuracion')


@login_required(login_url='ingresar')
def eliminar_productor(request):

    if request.method == 'POST':
        usuario=request.user
        if (check_password(request.POST.get('old_password'), usuario.password)):
            try:
                usuario.delete()
                return redirect ('ingresar')
            except:
                messages.error(request,"Error al eliminar la cuenta")
                return redirect ('cargar_configuracion')
        else:
             messages.error(request,"La contraseña ingresada es incorrecta")


    return redirect ('cargar_configuracion')





