from django.shortcuts import render


def certificate_list(request):
    return render(request, 'home.html', {'title': 'Certificados'})
