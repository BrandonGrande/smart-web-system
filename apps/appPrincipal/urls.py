from django.urls import path
from apps.appPrincipal.views import cargar_principal,cargar_configuracion
from apps.appDiagnostico.views import cargar_diagnostico
from apps.appReportes.views import cargar_reportes, cargar_reporte,cargar_grafico,eliminar_reporte_diagnostico,modificar_reporte_diagnostico
from apps.appComunidad.views import cargar_comunidad,crear_pregunta,eliminar_pregunta,modificar_pregunta,crear_respuesta,cargar_pregunta, modificar_respuesta, eliminar_respuesta
from apps.appUsuario.views import modificar_imgPrincipal,modificar_informacion,modificar_contrasenia,eliminar_productor,cerrar_sesion
from apps.appEnfermedades.views import cargar_enfermedades,crear_enfermedad, consultar_enfermedad, modificar_enfermedad, modificar_imagenes_muestra, modificar_carpeta_entrenamiento,modificar_carpeta_validacion, eliminar_enfermedad
from django.contrib.auth.decorators import login_required,  user_passes_test
from apps.appReentrenamiento.views import cargar_reentrenamiento, reentrenar_red_neuronal
from apps.appBitacora.views import cargar_reporte_reentrenamiento,cargar_bitacora,eliminar_reentrenamiento,modificar_reentrenamiento
from apps.appBiblioteca.views import cargar_biblioteca
from apps.appRespaldo.views import cargar_respaldo,cargar_recuperacion

urlpatterns = [
path('salir',cerrar_sesion,name="cerrar_sesion"),
path('',cargar_principal,name="cargar_principal"),
path('diagnostico',cargar_diagnostico,name="cargar_diagnostico"),
path('reportes',cargar_reportes,name="cargar_reportes"),
path('reporte<id_diagnostico>',cargar_reporte,name="cargar_reporte"),
path('cargar_grafico',cargar_grafico,name="cargar_grafico"),
path('eliminar_reporte_diagnostico<id_diagnostico>',eliminar_reporte_diagnostico,name="eliminar_reporte_diagnostico"),
path('modificar_reporte_diagnostico<id_diagnostico>',modificar_reporte_diagnostico,name="modificar_reporte_diagnostico"),
path('comunidad',cargar_comunidad,name="cargar_comunidad"),
path('crear_pregunta<id_vista>',crear_pregunta,name="crear_pregunta"),
path('eliminar_pregunta<id_pregunta><id_vista>',eliminar_pregunta,name="eliminar_pregunta"),
path('modificar_pregunta<id_pregunta><id_vista>',modificar_pregunta,name="modificar_pregunta"),
path('crear_respuesta<id_pregunta>',crear_respuesta,name="crear_respuesta"),
path('modificar_respuesta<id_respuesta>',modificar_respuesta,name="modificar_respuesta"),
path('eliminar_respuesta<id_respuesta>',eliminar_respuesta,name="eliminar_respuesta"),
path('cargar_pregunta<id_pregunta>',cargar_pregunta,name="cargar_pregunta"),
path('modificar_imgPrincipal',modificar_imgPrincipal, name="modificar_imgPrincipal"),
path('configuracion',cargar_configuracion,name="cargar_configuracion"),
path('modificar_informacion',modificar_informacion,name="modificar_informacion"),
path('modificar_contraseña',modificar_contrasenia,name="modificar_contrasenia"),
path('eliminar_productor',eliminar_productor,name="eliminar_productor"),
path('enfermedades',cargar_enfermedades,name="cargar_enfermedades"),
path('crear_enfermedad',crear_enfermedad,name="crear_enfermedad"),
path('consultar_enfermedad<id_enfermedad>',consultar_enfermedad,name="consultar_enfermedad"),
path('modificar_enfermedad<id_enfermedad>',modificar_enfermedad,name="modificar_enfermedad"),
path('modificar_imagenes_muestra',modificar_imagenes_muestra,name="modificar_imagenes_muestra"),
path('modificar_carpeta_validacion',modificar_carpeta_validacion,name="modificar_carpeta_validacion"),
path('modificar_carpeta_entrenamiento',modificar_carpeta_entrenamiento,name="modificar_carpeta_entrenamiento"),
path('eliminar_enfermedad<id_enfermedad>',eliminar_enfermedad,name="eliminar_enfermedad"),
path('reentrenamiento',cargar_reentrenamiento,name="cargar_reentrenamiento"),
path('reentrenar_red_neuronal',reentrenar_red_neuronal,name="reentrenar_red_neuronal"),
path('cargar_reporte_reentrenamiento<id_reentrenamiento>',cargar_reporte_reentrenamiento,name="cargar_reporte_reentrenamiento"),
path('eliminar_reentrenamiento<id_reentrenamiento>',eliminar_reentrenamiento,name="eliminar_reentrenamiento"),
path('modificar_reentrenamiento<id_reentrenamiento>',modificar_reentrenamiento,name="modificar_reentrenamiento"),
path('bitacora',cargar_bitacora,name="cargar_bitacora"),
path('biblioteca',cargar_biblioteca,name="cargar_biblioteca"),
path('respaldo',cargar_respaldo,name="cargar_respaldo"),
path('recuperacion',cargar_recuperacion,name="cargar_recuperacion"),
]