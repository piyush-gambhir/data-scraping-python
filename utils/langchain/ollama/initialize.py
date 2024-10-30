from langchain_ollama import OllamaLLM

from fastapi import HTTPException
from utils.logger.setup import setup_logger

logger = setup_logger(__name__)


def initialize_ollama_llm(model_name, base_url="http://localhost:11434"):
    """
    Initializes the Ollama LLM client with a given model name and base URL.

    :param model_name: The name of the model to use.
    :param base_url: The base URL for the LLM.
    :return: Initialized Ollama LLM object.
    """
    try:
        ollama_llm = OllamaLLM(model=model_name, base_url=base_url)
        return ollama_llm
    except Exception as e:
        logger.error(f"Failed to initialize Ollama LLM: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to initialize language model.")
