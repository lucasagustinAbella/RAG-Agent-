from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv("YOUTUBE_API_KEY")

# Configure the YouTube API client
youtube = build("youtube", "v3", developerKey=api_key)


def search_youtube_trailer(movie_title: str):
    """Searches for a movie or TV show trailer on YouTube using the YouTube API."""
    query = f"{movie_title} official trailer"

    # Perform the search request
    request = youtube.search().list(part="snippet", q=query, type="video", maxResults=1)
    response = request.execute()

    # Extract results
    if "items" not in response or not response["items"]:
        return None

    video = response["items"][0]
    trailer_info = {
        "title": video["snippet"]["title"],
        "url": f"https://www.youtube.com/watch?v={video['id']['videoId']}",
        "duration": "Not available",  # The API does not provide duration directly in search results
        "view_count": "Not available",  # The search API does not include view count
    }

    return trailer_info
