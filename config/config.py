import os

def get_openai_api_key():
    """
    Retrieve OpenAI API key from environment variables.

    This function attempts to fetch the OpenAI API key from the system's 
    environment variables. If the environment variable "OPENAI_API_KEY" 
    is not set, it falls back to using a default API key provided as a 
    string.

    Returns:
        str: The OpenAI API key, either from the environment variable or 
             the fallback default value.
    """
    # Retrieve the API key from the "OPENAI_API_KEY" environment variable.
    # If not found, use the fallback default API key provided.
    return os.getenv(
        "OPENAI_API_KEY",  # Environment variable to search for
        "YOUR_API_KEY"  # Default fallback key
    )