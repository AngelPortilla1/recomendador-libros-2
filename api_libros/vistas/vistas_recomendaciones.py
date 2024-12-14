from django.shortcuts import render
from django.http import JsonResponse
from api_libros.modelos.models import Recomendacion, Libro
from api_libros.utils import recomendar_libros_contenido, recomendar_libros_colaborativo
import pandas as pd

def recomendaciones_contenido(request, libro_id):
    # Cargar libros desde el archivo CSV
    try:
        libros_df = pd.read_csv('libros.csv')
        libros_recomendados = recomendar_libros_contenido(libro_id, libros_df)
        return JsonResponse({'recomendaciones': libros_recomendados})
    except FileNotFoundError:
        return JsonResponse({'error': 'Archivo de libros no encontrado.'}, status=404)

def recomendaciones_colaborativo(request, usuario_id):
    # Obtén los datos desde el modelo
    try:
        queryset = Recomendacion.objects.values('usuario_id', 'libro_id', 'comentario')
        recomendaciones_df = pd.DataFrame.from_records(queryset)

        # Verifica las columnas requeridas
        columnas_requeridas = {'usuario_id', 'libro_id', 'comentario'}
        columnas_presentes = set(recomendaciones_df.columns)

        if not columnas_requeridas.issubset(columnas_presentes):
            faltantes = columnas_requeridas - columnas_presentes
            return JsonResponse({
                'error': f"Faltan las siguientes columnas: {faltantes}",
                'columnas_actuales': list(columnas_presentes),
            }, status=500)

        # Verifica que no esté vacío
        if recomendaciones_df.empty:
            return JsonResponse({
                'error': "No se encontraron datos en la tabla 'Recomendacion'."
            }, status=404)

        # Realiza el pivot y genera las recomendaciones
        libros_recomendados = recomendar_libros_colaborativo(usuario_id, recomendaciones_df)
        return JsonResponse({
            'usuario_id': usuario_id,
            'libros_recomendados': libros_recomendados,
        })

    except Exception as e:
        return JsonResponse({
            'error': f"Ocurrió un error: {str(e)}",
        }, status=500)
