from django.urls import path
from .views import signature_list

urlpatterns = [
    path('', signature_list, name='signatures'),
]
