from duckduckgo_search import DDGS


def search_web(query: str, max_results=5):

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
        for result in ddgs.text(query, max_results=max_results):

            if any(keyword in result["body"].lower() for keyword in relevant_keywords):
                results.append(
                    {
                        "title": result["title"],
                        "url": result["href"],
                        "snippet": result["body"],
                    }
                )

    return results
