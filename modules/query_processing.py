from fuzzywuzzy import process
import openai
from config.config import get_openai_api_key
from llm.call_llm import call_llm

# Set the OpenAI API key using the configuration function
openai.api_key = get_openai_api_key()


def interpret_query(query):
    """
    Use GPT-3.5 Turbo to interpret the user's query and extract the item.

    Args:
        query (str): The user's query in natural language.

    Returns:
        str: The interpreted item name or a clarification request if the item cannot be determined.
    """
    # Prompt for the LLM to interpret the query and extract the item name
    prompt = (
        f"You are a helpful assistant. Analyze the query and determine the item the user is asking for. "
        f"Only return the item name. If the item cannot be determined, respond with: "
        f"'Could you please clarify what item you’re looking for? This will help me assist you better.'. Query: {query}"
    )
    # Call the LLM to process the prompt and return the result
    return call_llm(prompt)


def correct_spelling(item, inventory):
    """
    Use fuzzy matching to correct spelling mistakes in the item name.

    Args:
        item (str): The item name provided by the user, potentially misspelled.
        inventory (pd.DataFrame): The inventory DataFrame containing valid item names.

    Returns:
        str: The corrected item name if a good match is found; otherwise, returns the original input.
    """
    # Get a list of all valid item names from the inventory
    all_items = inventory['item'].tolist()
    
    # Use fuzzy matching to find the best match for the given item
    best_match, score = process.extractOne(item, all_items)
    
    # Return the best match if the match score is above 80, else return the original input
    return best_match if score > 80 else item


def determine_department(item, inventory):
    """
    Use GPT-3.5 Turbo to determine the department for a given item.

    Args:
        item (str): The item name whose department needs to be determined.
        inventory (pd.DataFrame): The inventory DataFrame containing department information.

    Returns:
        str: The department name that the item belongs to, as determined by the LLM.
    """
    # Create a comma-separated list of unique departments in the inventory
    departments = ', '.join(inventory['department'].unique())
    
    # Prompt for the LLM to determine the department for the given item
    prompt = (
        f"You are a helpful assistant. Determine which department the following item belongs to. "
        f"Item: {item}. Available departments: {departments}."
    )
    # Call the LLM to process the prompt and return the department name
    return call_llm(prompt)
