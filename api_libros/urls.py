from django.urls import path
from api_libros.vistas.data_libros import GetLibroList
from .vistas.views import LibroListView, recommend_books
from api_libros.vistas import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from api_libros.vistas.vistas_recomendaciones import recomendaciones_contenido, recomendaciones_colaborativo
from api_libros.vistas.views import fetch_books_view

#from api_libros.vistas.views import recommend_books
#from api_libros.vistas.views import fetch_books_data


urlpatterns = [
    # Otras rutas
    path('iniciar-sesion/', LoginView.as_view(template_name='iniciar_sesion.html'), name='iniciar_sesion'),
]



urlpatterns = [
    path('', LibroListView.as_view(), name='libro-list'),  # Ruta base: /libros/
    path('all/', GetLibroList.as_view(), name='libros-list'),
    
    path('crear-usuario/', views.crear_usuario, name='crear_usuario'),
    #path('crear-usuario/', views.crear_usuario, name='crear_usuario'),
    
    path('iniciar-sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('perfil/', views.perfil, name='perfil'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('recomendaciones/contenido/<int:libro_id>/', recomendaciones_contenido, name='recomendaciones_contenido'),
    path('recomendaciones/colaborativo/<int:usuario_id>/', recomendaciones_colaborativo, name='recomendaciones_colaborativo'),
    path('fetch-books/', fetch_books_view, name='fetch_books'),
     path('recommend-books/', recommend_books, name='recommend_books'),
   # path('recommend-books/', views.recommend_books, name='recommend_books'),
    #path('recommend-books/', views.recommend_books, name='recommend_books'),

]



