import os
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from .tooled_functions import fetch_movie_details
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access the environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class RAGAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-4", openai_api_key=OPENAI_API_KEY)

    def process_query(self, query: str):
        """Processes the user's query and decides which tool to use."""

        # Fetch movie details
        results = fetch_movie_details(query)

        # Generate response using LLM
        response = self.llm(
            [
                HumanMessage(
                    content=f"Information found about '{query}': {results['imdb']}. Trailer: {results['trailer']}"
                )
            ]
        )

        return {
            "query": query,
            "movie_info": results["imdb"],
            "trailer_url": results["trailer"],
            "web_results": results["web_results"],
            "ai_response": response.content,
        }


if __name__ == "__main__":
    agent = RAGAgent()
    user_query = input("Search for a movie or TV series: ")
    result = agent.process_query(user_query)
    print(result)
