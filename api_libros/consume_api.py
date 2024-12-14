import requests

# URL de la API
API_URL = "https://www.googleapis.com/books/v1/volumes?q=desarrollo&maxResults=40"  # Ajusta si tu endpoint es diferente.

try:
    # Realizar la solicitud GET a la API
    response = requests.get(API_URL)
    response.raise_for_status()  # Verifica si hubo algún error en la solicitud

    # Procesar los datos obtenidos
    data = response.json()

    # Extraer y mostrar información de los libros
    libros = data.get("items", [])

    # Mostrar la información en formato legible
    if libros:
        for libro in libros:
            volume_info = libro.get("volumeInfo", {})
            title = volume_info.get("title", "Título no disponible")
            authors = volume_info.get("authors", ["Autor no disponible"])
            print(f"Autor(es): {', '.join(authors)}")
    else:
        print("No hay libros disponibles en la API.")

except requests.exceptions.RequestException as e:
    print(f"Error al consumir la API: {e}")
