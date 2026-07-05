from django.shortcuts import render


def signature_list(request):
    return render(request, 'home.html', {'title': 'Firma digital'})
