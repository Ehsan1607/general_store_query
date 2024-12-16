import unittest
import pandas as pd
from modules.embedding import create_or_load_faiss_index, embed_query, find_best_match
from config.config import get_openai_api_key

class TestEmbedding(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment by loading the inventory file,
        preprocessing it to add a 'combined' column, and specifying the FAISS index path.

        The 'combined' column is used for embedding generation, combining department 
        and item information into a single string for better semantic matching.
        """
        # Load the inventory CSV file into a pandas DataFrame
        self.inventory = pd.read_csv("inventory.csv")
        
        # Add a 'combined' column to the inventory by concatenating 'department' and 'item'
        self.inventory["combined"] = (
            self.inventory["department"] + " " + self.inventory["item"]
        )
        
        # Specify the path where the FAISS index is or will be stored
        self.index_path = "faiss_index/index.bin"

    def test_create_or_load_faiss_index(self):
        """
        Test whether the FAISS index and embedding model are created or loaded successfully.

        Ensures that the function correctly initializes or loads a FAISS index 
        and an embedding model.
        """
        # Call the function to create or load the FAISS index
        index, model = create_or_load_faiss_index(self.inventory, self.index_path)
        
        # Assert that the index is not None (i.e., it was created or loaded successfully)
        self.assertIsNotNone(index)
        
        # Assert that the embedding model is not None
        self.assertIsNotNone(model)

    def test_embed_query(self):
        """
        Test if a query is embedded correctly into a vector with the expected shape.

        This ensures the embedding model generates a valid 1D embedding vector for a given query.
        """
        # Create or load the FAISS index and embedding model
        index, model = create_or_load_faiss_index(self.inventory, self.index_path)
        
        # Embed a sample query
        query_embedding = embed_query("Grocery Banana", model)
        
        # Assert that the embedding is a 1D vector
        self.assertEqual(len(query_embedding.shape), 1)

    def test_find_best_match(self):
        """
        Test whether the best match for an embedded query is correctly found in the inventory.

        This ensures that the FAISS index correctly retrieves the closest match 
        for the given query embedding.
        """
        # Create or load the FAISS index and embedding model
        index, model = create_or_load_faiss_index(self.inventory, self.index_path)
        
        # Embed a sample query
        query_embedding = embed_query("Grocery Banana", model)
        
        # Find the best match in the inventory
        match = find_best_match(query_embedding, self.inventory, index)
        
        # Assert that a match is found
        self.assertIsNotNone(match)
        
        # Assert that the matched item's name is 'banana' (case-insensitive check)
        self.assertEqual(match["item"].lower(), "banana")

    def test_find_best_match_no_match(self):
        """
        Test if find_best_match handles cases where no match is found gracefully.

        This ensures that the function returns None when there are no suitable matches.
        """
        # Create or load the FAISS index and embedding model
        index, model = create_or_load_faiss_index(self.inventory, self.index_path)
        
        # Embed a query that doesn't exist in the inventory
        unmatched_embedding = embed_query("Nonexistent Item", model)
        
        # Try to find a match in the inventory
        match = find_best_match(unmatched_embedding, self.inventory, index)
        
        # Assert that no match is found (i.e., match is None)
        self.assertIsNone(match)

    def test_embed_query_invalid_input(self):
        """
        Test if embed_query handles invalid input gracefully.

        This ensures that the function raises an appropriate error 
        when given invalid input, such as None.
        """
        # Create or load the FAISS index and embedding model
        index, model = create_or_load_faiss_index(self.inventory, self.index_path)

        # Check for None input
        with self.assertRaises(ValueError):
            embed_query(None, model)

        # Check for empty string input
        with self.assertRaises(ValueError):
            embed_query("", model)

        # Check for non-string input
        with self.assertRaises(ValueError):
            embed_query(123, model)

if __name__ == "__main__":
    unittest.main()
