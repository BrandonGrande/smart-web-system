from django.contrib import admin
from apps.appReentrenamiento.models import Reentrenamiento,Clase,Error,Calidad

admin.site.register(Reentrenamiento)
admin.site.register(Clase)
admin.site.register(Error)
admin.site.register(Calidad)
