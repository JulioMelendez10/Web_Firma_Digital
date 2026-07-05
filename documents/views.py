from django.shortcuts import render


def document_list(request):
    return render(request, 'home.html', {'title': 'Gestión de documentos'})
