import requests
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Cargar el modelo preentrenado para embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Obtener los datos de los libros desde la URL proporcionada
def fetch_books_data():
    response = requests.get("https://2b7tvpcm-8000.use2.devtunnels.ms/libros/fetch-books/")
    if response.status_code == 200:
        books_data = response.json()
        return books_data.get('books', [])
    return []

# Generar embeddings de los libros
def generate_book_embeddings(books):
    book_titles = [book['volumeInfo']['title'] for book in books]
    book_descriptions = [book['volumeInfo'].get('description', 'No description available') for book in books]
    book_authors = [', '.join(book['volumeInfo'].get('authors', ['Unknown Author'])) for book in books]
    book_subtitles = [book['volumeInfo'].get('subtitle', '') for book in books]

    book_texts = [f"{title} {subtitle} {author} {description}" for title, subtitle, author, description in zip(book_titles, book_subtitles, book_authors, book_descriptions)]
    book_embeddings = model.encode(book_texts, convert_to_tensor=True)
    return books, book_embeddings

# Encontrar libros similares
def find_similar_books(user_suggestion, books, book_embeddings, top_n=5):
    user_embedding = model.encode([user_suggestion], convert_to_tensor=True)
    similarities = cosine_similarity(user_embedding, book_embeddings)
    similar_indices = similarities.argsort()[0][-top_n:][::-1]
    similar_books = [(books[i], similarities[0][i]) for i in similar_indices]
    return similar_books
