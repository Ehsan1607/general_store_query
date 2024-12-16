import openai
from config.config import get_openai_api_key

import openai

def call_llm(prompt, model="gpt-3.5-turbo", max_tokens=200):
    """
    Centralized method to call GPT-3.5 Turbo with a given prompt.

    Args:
        prompt (str): The prompt to send to the LLM.
        model (str): The LLM model to use. Default is "gpt-3.5-turbo".
        max_tokens (int): The maximum tokens for the LLM response. Default is 200.

    Returns:
        str: The response content from the LLM or an error message.
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        return f"An error occurred while processing your request: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

