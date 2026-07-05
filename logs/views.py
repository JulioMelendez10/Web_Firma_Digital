from django.shortcuts import render


def history_list(request):
    return render(request, 'home.html', {'title': 'Historial'})
