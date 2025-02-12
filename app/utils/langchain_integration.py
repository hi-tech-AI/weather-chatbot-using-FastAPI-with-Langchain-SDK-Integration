from langchain_openai import ChatOpenAI


class QueryProcessor:
    def __init__(self):
        self.llm = self._initialize_llm()

    @staticmethod
    def _initialize_llm():
        """Initialize the language model."""
        try:
            return ChatOpenAI()
        except Exception as e:
            raise RuntimeError("Failed to initialize ChatOpenAI.") from e

    def process_query(self, user_query: str) -> str:
        """
        Process the user's query using the language model.

        Args:
            user_query (str): The query input by the user.

        Returns:
            str: The response from the language model.
        """
        try:
            response = self.llm.invoke(user_query)
            return response.content
        except Exception as e:
            raise RuntimeError("Failed to process the query.") from e
