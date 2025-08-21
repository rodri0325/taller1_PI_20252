from django.shortcuts import render
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib
import base64

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    
    return render(request, 'home.html', {
        'searchTerm': searchTerm,
        'movies': movies,
        'name': 'David Rodriguez'
    })

def about(request):
    return render(request, 'about.html')

def signup(request):
    email= request.GET.get('email')
    return render(request, 'signup.html', {'email':email})

def statistics_view(request):
    # Configurar el backend de matplotlib
    matplotlib.use('Agg')
    
    # ===== GRÁFICA DE PELÍCULAS POR AÑO =====
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {}
    
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        
        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    # Crear gráfica de años
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)  # 1 fila, 2 columnas, primer gráfico
    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center', color='skyblue')
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=45)
    plt.tight_layout()

    # ===== GRÁFICA DE PELÍCULAS POR GÉNERO =====
    # Obtener todos los géneros (solo el primer género de cada película)
    movies = Movie.objects.all()
    genre_counts = {}
    
    for movie in movies:
        if movie.genre:
            # Tomar solo el primer género (separado por coma si hay múltiples)
            first_genre = movie.genre.split(',')[0].strip()
            if first_genre in genre_counts:
                genre_counts[first_genre] += 1
            else:
                genre_counts[first_genre] = 1
        else:
            if "No Genre" in genre_counts:
                genre_counts["No Genre"] += 1
            else:
                genre_counts["No Genre"] = 1

    # Ordenar géneros por cantidad (opcional)
    sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
    genres = [item[0] for item in sorted_genres]
    counts = [item[1] for item in sorted_genres]

    # Crear gráfica de géneros
    plt.subplot(1, 2, 2)  # 1 fila, 2 columnas, segundo gráfico
    colors = plt.cm.Set3(range(len(genres)))  # Paleta de colores
    plt.barh(genres, counts, color=colors)  # Gráfica horizontal
    plt.title('Movies per Genre (First Genre)')
    plt.xlabel('Number of movies')
    plt.ylabel('Genre')
    plt.tight_layout()

    # Guardar la gráfica combinada en un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    plt.close()

    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # Renderizar la plantilla con la gráfica
    return render(request, 'statistics.html', {'graphic': graphic})