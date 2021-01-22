from django.contrib import admin
from apps.appUsuario.models import User
admin.site.register(User)
# Register your models here.
admin.site.site_header="Administración del sistema inteligente"
admin.site.site_title="Administración del sistema inteligente"
admin.site.index_title="Bienvenido administrador"


