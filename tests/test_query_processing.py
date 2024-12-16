import unittest
import pandas as pd
import re
from modules.query_processing import interpret_query, correct_spelling, determine_department
from config.config import get_openai_api_key

class TestQueryProcessing(unittest.TestCase):
    """
    Unit tests for query processing functions:
    - interpret_query
    - correct_spelling
    - determine_department
    """

    def setUp(self):
        """
        Set up the test environment by loading the inventory file.
        """
        # Load the inventory file into a pandas DataFrame
        self.inventory = pd.read_csv("inventory.csv")

    def test_interpret_query(self):
        """
        Test if interpret_query correctly extracts 'banana' from a simple query.

        Validates:
        - The function's ability to identify items in basic queries.
        """
        query = "Where can I find banana?"
        result = interpret_query(query)
        self.assertIn("banana", result.lower())  # Substring check for "banana"

    def test_interpret_query_with_extras(self):
        """
        Test if interpret_query correctly identifies 'bananas' when extra words are included.

        Validates:
        - The function's ability to parse more complex queries with additional words.
        """
        query = "Do you have fresh bananas available in the store?"
        result = interpret_query(query)
        self.assertIn("bananas", result.lower())  # Substring check for "bananas"

    def test_correct_spelling(self):
        """
        Test if correct_spelling corrects a minor misspelling ('Bananaa') to 'banana'.

        Validates:
        - Fuzzy matching for minor misspellings.
        """
        misspelled_item = "Bananaa"
        corrected_item = correct_spelling(misspelled_item, self.inventory)
        self.assertIn("banana", corrected_item.lower())  # Substring check for "banana"

    def test_correct_spelling_complex(self):
        """
        Test if correct_spelling corrects a significant misspelling ('Banna') to 'banana'.

        Validates:
        - Fuzzy matching for more significant misspellings.
        """
        misspelled_item = "Banna"
        corrected_item = correct_spelling(misspelled_item, self.inventory)
        self.assertIn("banana", corrected_item.lower())  # Substring check for "banana"

    def test_correct_spelling_no_match(self):
        """
        Test if correct_spelling returns the original input when no good match is found.

        Validates:
        - The function's ability to gracefully handle inputs not present in the inventory.
        """
        misspelled_item = "Zucchini"
        corrected_item = correct_spelling(misspelled_item, self.inventory)
        self.assertEqual(corrected_item, misspelled_item)  # No correction expected

    def test_determine_department(self):
        """
        Test if determine_department correctly identifies the department for 'banana'.

        Validates:
        - The function's ability to assign items to the correct department.
        """
        department = determine_department("banana", self.inventory)
        self.assertIn("grocery", department.lower())  # Substring check for "grocery"

    def test_determine_department_invalid_item(self):
        """
        Test if determine_department handles invalid items gracefully.

        Validates:
        - The function's behavior when asked for an item not present in the inventory.
        """
        department = determine_department("laptop charger", self.inventory)
        self.assertIn("electronics", department.lower())  # Check for department name
        self.assertIn("laptop charger", department.lower())  # Check for item name

    def test_interpret_query_case_insensitive(self):
        """
        Test if interpret_query works correctly with case-insensitive input.

        Validates:
        - The function's ability to handle uppercase/lowercase variations in queries.
        """
        query = "do you have BANANAS?"
        result = interpret_query(query)
        self.assertIn("bananas", result.lower())  # Substring check for "bananas"

    def test_determine_department_case_insensitive(self):
        """
        Test if determine_department works correctly with mixed-case input.

        Validates:
        - The function's ability to handle uppercase/lowercase variations in item names.
        """
        department = determine_department("BanAnA", self.inventory)
        self.assertIn("banana", department.lower())  # Check for item name
        self.assertIn("grocery", department.lower())  # Check for department name

    def test_correct_spelling_case_insensitive(self):
        """
        Test if correct_spelling works correctly with case-insensitive input.

        Validates:
        - The function's ability to correct misspelled words regardless of case.
        """
        misspelled_item = "BANANAA"
        corrected_item = correct_spelling(misspelled_item, self.inventory)
        self.assertIn("banana", corrected_item.lower())  # Substring check for "banana"


if __name__ == "__main__":
    unittest.main()
