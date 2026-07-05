from django.urls import path
from .views import certificate_list

urlpatterns = [
    path('', certificate_list, name='certificates'),
]
