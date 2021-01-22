from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.management import call_command
from django.core import management
from django.core.management.commands import loaddata
import os
from django.conf import settings
from django.http import HttpResponse, Http404

import os,shutil
import zipfile
from io import StringIO,BytesIO

from django.http import HttpResponse
from datetime import datetime
from django.core.files.base import ContentFile
import shutil
from django.contrib.auth.decorators import user_passes_test,login_required
from apps.appReentrenamiento.models import Reentrenamiento


@login_required(login_url='ingresar')
@user_passes_test(lambda u: u.is_superuser)
def cargar_respaldo(request):

    if request.method=='POST':
        try:
            folder =os.path.join(settings.BASE_DIR, 'backup/')
            limpiar_carpeta(folder,0)
            management.call_command('dbbackup',interactive=False)
            management.call_command('mediabackup',interactive=False)
            filenames=obtener_archivos(folder)
            fecha=datetime.now()
            fecha=fecha.strftime("%d%m%y_%H%M%S")
            zip_subdir = "respaldo_"+str(fecha)
            zip_filename = "%s.zip" % zip_subdir
            s = BytesIO()
            zf = zipfile.ZipFile(s, "w")
            for fpath in filenames:
                fdir, fname = os.path.split(fpath)
                zip_path = os.path.join(zip_subdir, fname)
                zf.write(fpath, zip_path)
            zf.close()

            resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
            resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
            return resp
        except:
            messages.error(request,"Error al generar respaldo de base de datos")
            return redirect('cargar_respaldo')


    return render(request,'appRespaldo/respaldo.html')


@login_required(login_url='ingresar')
@user_passes_test(lambda u: u.is_superuser)
def cargar_recuperacion(request):

    if request.method=='POST':
        try:
            limpiar_carpeta(os.path.join(settings.BASE_DIR, 'backup/') ,0)
            limpiar_carpeta(os.path.join(settings.BASE_DIR, 'backup/recovery') ,1)
            file= request.FILES.get('archivoRespaldo')
            ruta_recuperacion=os.path.join(settings.BASE_DIR,"backup/recovery/"+ str(request.FILES['archivoRespaldo'].name))
            with open(ruta_recuperacion, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            shutil.unpack_archive(ruta_recuperacion,os.path.join(settings.BASE_DIR,"backup/recovery"))
            ruta_recuperacion_libre=os.path.splitext(ruta_recuperacion)[0]
            mover_archivos(ruta_recuperacion_libre)
            management.call_command('dbrestore',interactive=False)
            Reentrenamiento.objects.all().update(estado=False)
            limpiar_carpeta(os.path.join(settings.BASE_DIR, 'media/') ,1)
            management.call_command('mediarestore',interactive=False)
            messages.success(request,"¡Sistema inteligente recuperado con exito!")
        except:
            messages.error(request,"Error al recuperar el sistema inteligente")

    return redirect('cargar_respaldo')


def limpiar_carpeta(folder,orden):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        if orden==1:
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)

def obtener_archivos(folder):
    lista=[]
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        if os.path.isfile(file_path):
            lista.append(file_path)
    return lista

def mover_archivos(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        if os.path.isfile(file_path):
            shutil.move(file_path,os.path.join(settings.BASE_DIR,'backup'))
