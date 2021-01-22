from django.contrib import admin
from apps.appEnfermedades.models import Enfermedad,ImgMuestra, ImgEntrenamiento,ImgValidacion

admin.site.register(Enfermedad)
admin.site.register(ImgValidacion)
admin.site.register(ImgEntrenamiento)
admin.site.register(ImgMuestra)
