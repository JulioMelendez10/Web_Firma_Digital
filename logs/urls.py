from django.urls import path
from .views import history_list

urlpatterns = [
    path('', history_list, name='logs'),
]
