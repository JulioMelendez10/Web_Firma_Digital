from django.urls import path
from . import views

app_name = 'documentos'

urlpatterns = [
    path('', views.lista_documentos, name='lista'),
    path('crear/', views.crear_documento, name='crear'),
    path('<int:pk>/', views.detalle_documento, name='detalle'),
    path('<int:pk>/firmar/', views.firmar_documento, name='firmar'),
    path('<int:pk>/verificar-firma/', views.verificar_firma, name='verificar_firma'),
    path('<int:pk>/editar/', views.editar_documento, name='editar'),
    path('<int:pk>/eliminar/', views.eliminar_documento, name='eliminar'),
    path('<int:pk>/descargar/', views.descargar_documento, name='descargar'),
    path('<int:pk>/verificar/', views.verificar_hash, name='verificar_hash'),
]