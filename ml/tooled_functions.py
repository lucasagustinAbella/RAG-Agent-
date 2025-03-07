from tools.search_engine import search_web
from tools.imdb_fetcher import get_movie_info
from tools.youtube_search import search_youtube_trailer


def fetch_movie_details(movie_title: str):
    imdb_data = get_movie_info(movie_title)
    youtube_trailer = search_youtube_trailer(movie_title)

    web_results = []

    try:
        web_results = search_web(movie_title)
    except Exception as e:
        print(
            f"Error with DuckDuckGo search: {e}. Using available data without web search."
        )

    result = {
        "imdb": imdb_data,
        "trailer": youtube_trailer,
        "web_results": web_results,
    }

    return result
