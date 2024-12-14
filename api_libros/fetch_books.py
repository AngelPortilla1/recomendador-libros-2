import asyncio
import aiohttp
import nest_asyncio

nest_asyncio.apply()  # Evita problemas en entornos con bucles eventuales activos (como Jupyter)

# Limitar la cantidad de tareas concurrentes
MAX_CONCURRENCY = 10  # Cambia según tus necesidades (menos solicitudes concurrentes = menos presión en el servidor)

# Función que obtiene los datos de una URL
async def fetch(session, url, semaphore):
    async with semaphore:
        async with session.get(url) as response:
            return await response.json()

# Función que obtiene todos los libros desde varias URLs
async def fetch_all_books(urls):
    semaphore = asyncio.Semaphore(MAX_CONCURRENCY)  # Controla la concurrencia
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url, semaphore) for url in urls]
        results = await asyncio.gather(*tasks)
        books = []
        for result in results:
            if 'items' in result:
                books.extend(result['items'])
        return books

# Lista de URLs
urls = [
    "https://www.googleapis.com/books/v1/volumes?q=desarrollo&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=science&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=history&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=biography&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=education&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=judicial&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=medicina&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=mecanica&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=finanza&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=deporte&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=gimnasia&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=ambiental&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=cultura&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=baile&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=arte&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=poesía&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=novela&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=infantil&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=filosofía&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=tecnología&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=psicología&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=sociedad&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=educación&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=cocina&maxResults=40",
    "https://www.googleapis.com/books/v1/volumes?q=viajes&maxResults=40",
]

# Función para obtener los libros
def get_books_from_urls():
    books = asyncio.run(fetch_all_books(urls))
    print(f"Total de registros obtenidos: {len(books)}")
    return books

# Llamada a la función
books = get_books_from_urls()
