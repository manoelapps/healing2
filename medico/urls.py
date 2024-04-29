from django.urls import path
from . import views

urlpatterns = [
    path('cadastro_medico/', views.cadastro_medico, name="cadastro_medico"),
    path('abrir_horario/', views.abrir_horario, name="abrir_horario"),
    path('consultas_medico/', views.consultas_medico, name="consultas_medico"),
    path('consulta_area_medico/<int:id_consulta>/', views.consulta_area_medico, name="consulta_area_medico"),
    path('finalizar_consulta/<int:id_consulta>/', views.finalizar_consulta, name="finalizar_consulta"),
    path('cancelar_consulta_med2/<int:id_consulta>/', views.cancelar_consulta_med2, name="cancelar_consulta_med2"),
    path('historico_consulta_med/', views.historico_consulta_med, name="historico_consulta_med"),
]
