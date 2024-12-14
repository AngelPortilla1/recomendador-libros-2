import requests
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class GetLibroList(APIView):
    """
    Vista para obtener y mostrar una lista de libros desde una API externa.
    """

    def get(self, request, *args, **kwargs):
        # URL de la API de Google Books
        API_URL = "https://www.googleapis.com/books/v1/volumes?q=desarrollo&maxResults=40"

        try:
            # Realizar la solicitud a la API de Google Books
            response = requests.get(API_URL)
            response.raise_for_status()  # Verifica si hubo algún error en la solicitud

            # Procesar los datos obtenidos
            data = response.json()
            libros = []

            for item in data.get("items", []):
                volume_info = item.get("volumeInfo", {})
                libro = {
                    "titulo": volume_info.get("title", "Título no disponible"),
                    "autor": volume_info.get("authors", ["Autor no disponible"]),
                    "genero": volume_info.get("categories", ["Género no disponible"]),
                    "anio_publicacion": volume_info.get("publishedDate", "Fecha no disponible"),
                    "caratula": volume_info.get("imageLinks", {}).get("thumbnail", "Carátula no disponible"),
                    "precio": item.get("saleInfo", {}).get("retailPrice", {}).get("amount", "Precio no disponible"),
                }
                libros.append(libro)

            # Retornar la lista de libros como JSON
            return Response({"libros": libros}, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response({"error": f"Error al obtener datos: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
