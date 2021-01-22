from django.contrib import admin
from apps.appDiagnostico.models import Diagnostico, Prediccion

admin.site.register(Diagnostico)
admin.site.register(Prediccion)