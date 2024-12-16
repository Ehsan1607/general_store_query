import faiss
from sentence_transformers import SentenceTransformer
import os
import openai
from config.config import get_openai_api_key
from llm.call_llm import call_llm
import pickle

openai.api_key = get_openai_api_key()

# Initialize an in-memory cache for query embeddings
embedding_cache = {}

def create_or_load_faiss_index(inventory, index_path):
    """
    Create or load a FAISS index from the specified path.

    Args:
        inventory (pd.DataFrame): The inventory DataFrame containing the 
                                  'combined' column with text to embed.
        index_path (str): The file path where the FAISS index is stored or will be saved.

    Returns:
        tuple: A tuple containing:
               - index (faiss.Index): The FAISS index for fast similarity search.
               - embedding_model (SentenceTransformer): The embedding model used to generate embeddings.
    """
    # Load the SentenceTransformer model for generating embeddings.
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Generate embeddings for the 'combined' column of the inventory.
    embeddings = embedding_model.encode(inventory['combined'].tolist())
    
    if os.path.exists(index_path):
        # Check if the FAISS index already exists at the given path.
        # If it exists, load the index from the file.
        #print("Loading FAISS index...")
        index = faiss.read_index(index_path)
    else:
        # If the index does not exist, create a new FAISS index.
        print("Creating new FAISS index...")
        
        # Initialize a FAISS index for L2 (Euclidean) distance with the correct embedding dimensions.
        index = faiss.IndexFlatL2(embeddings.shape[1])
        
        # Add the generated embeddings to the index.
        index.add(embeddings)
        
        # Ensure the directory for the index file exists.
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        
        # Save the created index to the specified path for future use.
        faiss.write_index(index, index_path)
        #print(f"FAISS index saved at {index_path}")
    
    # Return the FAISS index and the embedding model.
    return index, embedding_model


def embed_query(query, embedding_model):
    """
    Generate an embedding for a given query using the specified model.
    Use caching to avoid redundant computations for repeated queries.

    Args:
        query (str): The query string to embed.
        embedding_model (SentenceTransformer): The embedding model to use.

    Returns:
        numpy.ndarray: The embedding vector for the query.

    Raises:
        ValueError: If the query is None or empty.
    """
    if not query or not isinstance(query, str):
        raise ValueError("Invalid query: The query must be a non-empty string.")

    # Check if the query is already in the cache
    if query in embedding_cache:
        return embedding_cache[query]

    # Generate the embedding using the model
    embedding = embedding_model.encode([query])[0]
    
    # Store the result in the cache
    embedding_cache[query] = embedding

    # Save the cache to disk for persistence
    with open("embedding_cache.pkl", "wb") as f:
        pickle.dump(embedding_cache, f)

    return embedding
 

def find_best_match(query_embedding, inventory, index):
    """
    Find the best match for a query embedding in the inventory.

    Args:
        query_embedding (np.ndarray): The embedding vector of the query.
        inventory (pd.DataFrame): The inventory DataFrame containing the items to search.
        index (faiss.Index): The FAISS index to perform the similarity search.

    Returns:
        pd.Series or None: The row in the inventory DataFrame that best matches the query embedding.
                           Returns None if no match is found within the specified threshold.
    """
    # Perform a search in the FAISS index for the closest match to the query embedding.
    # `query_embedding.reshape(1, -1)` ensures the query is in the correct 2D shape for FAISS input.
    # `k=5` specifies that we want 5 closest matches.
    distances, indices = index.search(query_embedding.reshape(1, -1), k=5)

    # Check if the closest match has a distance below the threshold of 1.
    # If so, return the corresponding row from the inventory DataFrame.
    # Otherwise, return None (indicating no suitable match was found).
    return inventory.iloc[indices[0][0]] if distances[0][0] < 1 else None

    

def generate_user_response(query_embedding, inventory, index, user_query):
    """
    Generate a user-facing response based on the query embedding, inventory data, 
    and top matches from a FAISS index using an LLM.

    Args:
        query_embedding (np.ndarray): The embedding of the user's query.
        inventory (pd.DataFrame): The inventory DataFrame containing items, departments, prices, and availability.
        index (faiss.Index): The FAISS index for retrieving top matches based on the query embedding.
        user_query (str): The original query provided by the user.

    Returns:
        str: A generated response for the user, or an error message if no matches are found or an exception occurs.
    """

    # Find top 5 matches from the FAISS index
    distances, indices = index.search(query_embedding.reshape(1, -1), k=5)

    # Filter matches with a similarity distance below the threshold (1)
    top_matches = [
        inventory.iloc[idx] for idx, dist in zip(indices[0], distances[0]) if dist < 1
    ]
    
    # If no suitable matches are found, return an appropriate message
    if not top_matches:
        return "Sorry, no matching items found. Please refine your query."

    # Prepare context by formatting the top matches into a readable string
    context = "\n".join(
        [
            f"- Item: {match['item']}, Department: {match['department']}, "
            f"Price: ${match['price']}, Availability: {match['availability']}" 
            for match in top_matches
        ]
    )
    
    # Construct a prompt for the LLM to generate a response
    prompt = f"""
    You are a helpful assistant. A customer asked the following query: "{user_query}".
    Based on the inventory information below, provide a concise and professional response 
    without adding any extra prefixes like 'Response:'.

    Inventory information:
    {context}
    """

    try:
        # Call the LLM with the constructed prompt and handle exceptions gracefully
        response = call_llm(prompt, max_tokens=300)
        return response
    except Exception as e:
        # Return an error message if something goes wrong with the LLM call
        return f"An error occurred while processing your request: {str(e)}"
