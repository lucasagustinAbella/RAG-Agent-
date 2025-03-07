from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("YOUTUBE_API_KEY")

youtube = build("youtube", "v3", developerKey=api_key)


def search_youtube_trailer(movie_title: str):
    query = f"{movie_title} official trailer"

    request = youtube.search().list(part="snippet", q=query, type="video", maxResults=1)
    response = request.execute()

    if "items" not in response or not response["items"]:
        return None

    video = response["items"][0]
    trailer_info = {
        "title": video["snippet"]["title"],
        "url": f"https://www.youtube.com/watch?v={video['id']['videoId']}",
    }

    return trailer_info
