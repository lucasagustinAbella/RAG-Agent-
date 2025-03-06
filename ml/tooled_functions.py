from tools.search_engine import search_web
from tools.imdb_fetcher import get_movie_info
from tools.youtube_search import search_youtube_trailer


def fetch_movie_details(movie_title: str):
    """Usa las herramientas para obtener detalles de una película o serie."""

    imdb_data = get_movie_info(movie_title)
    youtube_trailer = search_youtube_trailer(movie_title)
    web_results = search_web(movie_title)

    result = {"imdb": imdb_data, "trailer": youtube_trailer, "web_results": web_results}

    return result
