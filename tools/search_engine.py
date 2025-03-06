from duckduckgo_search import DDGS


def search_web(query: str, max_results=5):
    """Performs a DuckDuckGo search and returns the top relevant results."""

    relevant_keywords = [
        "review",
        "analysis",
        "details",
        "summary",
        "ratings",
        "critique",
    ]
    results = []

    with DDGS() as ddgs:
        # Perform the search
        for result in ddgs.text(query, max_results=max_results):
            # Check if the snippet contains relevant keywords
            if any(keyword in result["body"].lower() for keyword in relevant_keywords):
                results.append(
                    {
                        "title": result["title"],
                        "url": result["href"],
                        "snippet": result["body"],
                    }
                )

    return results
