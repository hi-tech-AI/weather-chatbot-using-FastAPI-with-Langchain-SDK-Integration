from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def process_query(user_query: str) -> str:
    """
    Process the user's query based on given information.

    Args:
        user_query (str): The query input by the user.

    Returns:
        str: The response from the LLM or given query information.
    """

    llm = ChatOpenAI()
    response = llm.invoke(user_query)
    return response.content
