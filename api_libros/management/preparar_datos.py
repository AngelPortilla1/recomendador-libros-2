from django.core.management.base import BaseCommand
from api_libros.modelos import Libro
import pandas as pd

class Command(BaseCommand):
    help = 'Prepara los datos para el sistema de recomendación'

    def handle(self, *args, **kwargs):
        # Recoge todos los libros
        libros = Libro.objects.all()
        data = []

        # Preparando los datos (título, autor y categorías)
        for libro in libros:
            categorias = ' '.join(libro.categories) if libro.categories else ''  # Unir categorías si existen
            data.append([libro.titulo, libro.autor, categorias])

        # Crear un DataFrame
        df = pd.DataFrame(data, columns=['titulo', 'autor', 'categorias'])

        # Guardar el DataFrame en un archivo CSV o base de datos
        df.to_csv('libros.csv', index=False)
        self.stdout.write(self.style.SUCCESS('Datos preparados correctamente.'))

