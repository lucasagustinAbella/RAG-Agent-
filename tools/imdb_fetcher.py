import imdb


def get_movie_info(title: str):
    ia = imdb.Cinemagoer()

    search_results = ia.search_movie(title)
    if not search_results:
        return None

    movie = search_results[0]
    movie_id = movie.movieID
    movie_details = ia.get_movie(movie_id)

    info = {
        "title": movie_details.get("title"),
        "year": movie_details.get("year"),
        "rating": movie_details.get("rating"),
        "genres": movie_details.get("genres"),
        "plot": movie_details.get("plot outline"),
        "url": f"https://www.imdb.com/title/tt{movie_id}/",
    }

    return info
