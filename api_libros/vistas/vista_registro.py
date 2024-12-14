from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

Usuario = get_user_model()
"""
def crear_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f"Usuario '{usuario.username}' creado exitosamente.")
            return redirect('inicio')  # Redirige a la página de inicio
        else:
            messages.error(request, "Hubo un error al crear el usuario. Revisa los datos.")
    else:
        form = UserCreationForm()

    return render(request, 'crear_usuario.html', {'form': form})
"""