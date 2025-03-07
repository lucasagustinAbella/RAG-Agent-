import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

system_prompt = """
You are a helpful assistant trained to answer user queries by selecting the appropriate tools.
Here are the available tools and their descriptions:
- 'YouTube': Searches for the official trailer of a movie or TV show. The query should be about the movie/TV show title and 'official trailer'.
- 'IMDb': Retrieves detailed information about a movie or TV show, such as title, year, rating, genres, plot, and the IMDb link.
- 'Web Search': Searches the web for general information about a movie or TV show, looking for reviews, summaries, ratings, etc.

When you select a tool, please ensure that:
- If YouTube is selected, you must **search for and provide the real URL** of the official trailer in the response, formatted as: "Here is the official trailer: [actual URL]".
- If IMDb is selected, you must provide detailed information such as title, year, rating, genres, and plot in the format: "Title: [title], Year: [year], Rating: [rating], Genres: [genres], Plot: [plot], IMDb Link: [link]".
- If Web Search is selected, return relevant information with a brief summary or description of the movie or TV show in the format: "Here is a summary of [movie/TV show]: [summary]".

Make sure that the result is a **valid, real URL** (in case of YouTube) and that it is formatted correctly.
Your response should be in this format:
- "TOOLS: [List of Tools Used]"
- "RESULT: [Combined result of the tools]"

Please avoid any other text or explanations, just provide the selected tools' results in the specified format.
"""

chained_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)


class RAGAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-4", openai_api_key=OPENAI_API_KEY)

    def process_query(self, query: str):
        prompt = chained_prompt.format(input=query)
        response = self.llm.invoke([HumanMessage(content=prompt)])

        raw_response = response.content.strip()

        tools_used = []
        ai_response = ""

        if "TOOLS: " in raw_response and "RESULT: " in raw_response:
            try:
                tools_section = raw_response.split("TOOLS: ")[1].split("\n")[0].strip()
                result_section = raw_response.split("RESULT: ")[1].strip()

                tools_used = tools_section.split(", ")
                ai_response = f"{result_section}"

            except IndexError:
                pass

        if not ai_response:
            ai_response = "No valid result."

        return {
            "ai_response": ai_response,
            "tools_used": ", ".join(tools_used) if tools_used else "Unknown Tools",
        }


if __name__ == "__main__":
    agent = RAGAgent()
    user_query = input("Search for a movie or TV series: ")
    result = agent.process_query(user_query)
    for r in result:
        print(f"Tool Used: {r['tool_used']}")
        print(f"Result: {r['result']}")
