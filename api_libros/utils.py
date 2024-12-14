import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recomendar_libros_contenido(libro_id, libros_df):
    # Usamos el título, autor y categorías como base para recomendaciones
    libros_df['contenido'] = libros_df['titulo'] + ' ' + libros_df['autor'] + ' ' + libros_df['categorias']
    
    # Crear la matriz de características TF-IDF
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(libros_df['contenido'])
    
    # Calcular la similitud del coseno
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    # Obtener el índice del libro
    idx = libros_df[libros_df['titulo'] == libro_id].index[0]  # Buscar el índice por el título
    
    # Obtener los libros similares
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Ordenar por similitud
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Tomar los 5 libros más similares
    sim_scores = sim_scores[1:6]
    
    # Obtener los títulos de los libros recomendados
    libros_recomendados = [libros_df['titulo'].iloc[i[0]] for i in sim_scores]
    
    return libros_recomendados


def recomendar_libros_colaborativo(usuario_id, recomendaciones_df):
    # Asegúrate de que las columnas estén limpias
    recomendaciones_df.columns = recomendaciones_df.columns.str.strip()

    # Crea la matriz
    try:
        matrix = recomendaciones_df.pivot(index='usuario_id', columns='libro_id', values='comentario').fillna(0)
    except KeyError as e:
        raise ValueError(f"Error al generar la matriz: {e}. Verifica que todas las columnas necesarias estén presentes.")

    # Generar recomendaciones (esto es un ejemplo, ajusta según tu lógica)
    if usuario_id not in matrix.index:
        raise ValueError(f"El usuario con ID {usuario_id} no tiene datos suficientes para generar recomendaciones.")

    # Supongamos que usas similitud de coseno
    from sklearn.metrics.pairwise import cosine_similarity
    similitudes = cosine_similarity(matrix)
    similitudes_df = pd.DataFrame(similitudes, index=matrix.index, columns=matrix.index)

    # Busca los libros recomendados (lógica de ejemplo)
    usuarios_similares = similitudes_df[usuario_id].sort_values(ascending=False).index[1:]  # Ignora al propio usuario
    recomendaciones = matrix.loc[usuarios_similares].mean().sort_values(ascending=False).head(10)
    
    return recomendaciones.index.tolist()
