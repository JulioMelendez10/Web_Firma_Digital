from django.contrib.auth import logout
from django.shortcuts import redirect, render


def profile_view(request):
    return render(request, 'home.html', {'title': 'Perfil'})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    return redirect('/')
