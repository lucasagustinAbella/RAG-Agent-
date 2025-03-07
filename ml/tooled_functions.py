from tools.search_engine import search_web
from tools.imdb_fetcher import get_movie_info
from tools.youtube_search import search_youtube_trailer


class Tool:
    def __init__(self, name, func, description):
        self.name = name
        self.func = func
        self.description = description

    def execute(self, *args, **kwargs):
        return self.func(*args, **kwargs)


tools = [
    Tool(
        name="IMDb",
        func=get_movie_info,
        description="Retrieves detailed information about a movie or TV show, such as title, year, rating, genres, plot, and the IMDb link.",
    ),
    Tool(
        name="YouTube",
        func=search_youtube_trailer,
        description="Searches for the official trailer of a movie or TV show. The query should be about the movie/TV show title and 'official trailer'.",
    ),
    Tool(
        name="Web Search",
        func=search_web,
        description="Searches the web for general information about a movie or TV show, looking for reviews, summaries, ratings, etc.",
    ),
]
