from django.shortcuts import render
from django.views import View
from rest_framework.generics import ListAPIView
from ..modelos.models import Libro
from ..serializers import LibroSerializer

class LibroListView(ListAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    
""" 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..user_serializers import UsuarioSerializer

class CrearUsuarioAPIView(View):
    def post(self, request, *args, **kwargs):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            return Response(
                {
                    "message": "Usuario creado exitosamente",
                    "user_id": usuario.id,
                    "email": usuario.email,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""

"""
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

Usuario = get_user_model()

def crear_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f"Usuario '{usuario.username}' creado exitosamente.")
            return redirect('iniciar_sesion')  # Redirige a la página de inicio
        else:
            messages.error(request, "Hubo un error al crear el usuario. Revisa los datos.")
    else:
        form = UserCreationForm()

    return render(request, 'crear_usuario.html', {'form': form})

"""


"""
from django.shortcuts import render, redirect
from ..forms import RegistroUsuarioForm
from django.contrib import messages

def registrar_usuario(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            try:
                form.save()  # Guarda el usuario
                messages.success(request, "Usuario registrado exitosamente.")
                return redirect('iniciar_sesion')  # Redirige al login
            except Exception as e:
                messages.error(request, f"Error al registrar el usuario: {str(e)}")
        else:
            # Captura los errores del formulario
            for field, error in form.errors.items():
                messages.error(request, f"{field}: {error}")
    else:
        form = RegistroUsuarioForm()

    return render(request, 'crear_usuario.html', {'form': form})
"""








#AQUIII -----------------------------------------------------------



""" 
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

Usuario = get_user_model()

def crear_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f"Usuario '{usuario.username}' creado exitosamente.")
            return redirect('iniciar_sesion')  # Redirige a la página de inicio
        else:
            messages.error(request, "Hubo un error al crear el usuario. Revisa los datos.")
    else:
        form = UserCreationForm()

    return render(request, 'crear_usuario.html', {'form': form})
"""

from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
import json

Usuario = get_user_model()

@csrf_exempt
def crear_usuario(request):
    if request.method == 'POST':
        try:
            # Parsear los datos del JSON enviado
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email', '')  # Email opcional

            # Validar que se enviaron los datos necesarios
            if not username or not password:
                return JsonResponse({'error': 'El nombre de usuario y la contraseña son obligatorios.'}, status=400)

            # Verificar si el usuario ya existe
            if Usuario.objects.filter(username=username).exists():
                return JsonResponse({'error': f"El usuario '{username}' ya existe."}, status=400)

            # Crear el usuario
            usuario = Usuario.objects.create(
                username=username,
                email=email,
                password=make_password(password)  # Encripta la contraseña
            )

            return JsonResponse({'message': f"Usuario '{usuario.username}' creado exitosamente."}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido.'}, status=400)

    return JsonResponse({'error': 'Método no permitido. Usa POST.'}, status=405)


import json
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User as Usuario
from django.contrib.sessions.models import Session  # Para gestionar sesiones
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def iniciar_sesion(request):
    if request.method == 'POST':
        try:
            # Parsear los datos del JSON enviado
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # Validar que se enviaron los datos necesarios
            if not username or not password:
                return JsonResponse({'error': 'El nombre de usuario y la contraseña son obligatorios.'}, status=400)

            # Verificar si el usuario existe
            try:
                usuario = Usuario.objects.get(username=username)
            except Usuario.DoesNotExist:
                return JsonResponse({'error': 'Usuario o contraseña incorrectos.'}, status=401)

            # Validar la contraseña
            if not check_password(password, usuario.password):
                return JsonResponse({'error': 'Usuario o contraseña incorrectos.'}, status=401)

            # Crear una sesión (si no se utiliza JWT u otro mecanismo)
            request.session['usuario_id'] = usuario.id
            return JsonResponse({'message': f"Inicio de sesión exitoso. Bienvenido, {usuario.username}."}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido.'}, status=400)

    return JsonResponse({'error': 'Método no permitido. Usa POST.'}, status=405)


def perfil(request):
    return render(request, 'perfil.html', {'usuario': request.user})





from django.http import JsonResponse
from api_libros.fetch_books import get_books_from_urls

def fetch_books_view(request):
    """
    Vista que consulta los libros desde las URLs de Google Books API.
    """
    try:
        # Obtener libros usando la función de utilidades
        books = get_books_from_urls()
        return JsonResponse({"books": books, "count": len(books)}, status=200)
    except Exception as e:
        # Manejar errores y devolver un mensaje de error
        return JsonResponse({"error": str(e)}, status=500)

"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Cargar el modelo preentrenado para embeddings
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Obtener los datos de los libros desde la URL proporcionada
response = requests.get("https://2b7tvpcm-8000.use2.devtunnels.ms/libros/fetch-books/")
books_data = response.json()

# Access the list of books using the 'books' key
books = books_data['books']

# Extraer títulos y descripciones de los libros
book_titles = [book['volumeInfo']['title'] for book in books]
book_descriptions = [book['volumeInfo'].get('description', 'No description available') for book in books]

# Combinar títulos y descripciones para generar embeddings
book_texts = [f"{title} {description}" for title, description in zip(book_titles, book_descriptions)]

# Generar embeddings para los libros
book_embeddings = model.encode(book_texts)

def find_similar_books(user_suggestion, top_n=5):
    # Generar embedding para la sugerencia del usuario
    user_embedding = model.encode([user_suggestion])

    # Calcular la similitud del coseno entre la sugerencia del usuario y los embeddings de los libros
    similarities = cosine_similarity(user_embedding, book_embeddings)

    # Obtener los índices de los libros más similares
    similar_indices = similarities.argsort()[0][-top_n:][::-1]

    # Devolver los títulos de los libros más similares
    similar_books = [book_titles[i] for i in similar_indices]
    return similar_books

@csrf_exempt
def recommend_books(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_suggestion = data.get('suggestion', '')
        similar_books = find_similar_books(user_suggestion)
        return JsonResponse({'similar_books': similar_books})
    return JsonResponse({'error': 'Invalid request method'}, status=400)
"""





###################### PRUEBA VISTA ##################################
########################################################################
# ******************************************************************

from django.http import JsonResponse
from api_libros.services import fetch_books_data, generate_book_embeddings, find_similar_books

def recommend_books(request):
    user_suggestion = request.GET.get('suggestion', '')
    if not user_suggestion:
        return JsonResponse({'error': 'No suggestion provided'}, status=400)

    # Obtener los datos y generar embeddings
    books = fetch_books_data()
    if not books:
        return JsonResponse({'error': 'No books found'}, status=500)
    
    books_data, book_embeddings = generate_book_embeddings(books)
    similar_books = find_similar_books(user_suggestion, books_data, book_embeddings)
    
    # Formatear la respuesta
    response_data = [
        {
            'title': book['volumeInfo'].get('title', 'No title available'),
            'subtitle': book['volumeInfo'].get('subtitle', ''),
            'authors': book['volumeInfo'].get('authors', ['Unknown Author']),
            'description': book['volumeInfo'].get('description', 'No description available'),
            'published_date': book['volumeInfo'].get('publishedDate', 'Unknown'),
            'publisher': book['volumeInfo'].get('publisher', 'Unknown'),
            'categories': book['volumeInfo'].get('categories', []),
            'page_count': book['volumeInfo'].get('pageCount', 'Unknown'),
            'language': book['volumeInfo'].get('language', 'Unknown'),
            'thumbnail': book['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
            'preview_link': book['volumeInfo'].get('previewLink', ''),
            'info_link': book['volumeInfo'].get('infoLink', ''),
            'similarity': float(similarity)
        }
        for book, similarity in similar_books
    ]

    return JsonResponse({'similar_books': response_data})

