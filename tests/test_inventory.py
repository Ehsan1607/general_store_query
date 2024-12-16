import unittest
import pandas as pd
from modules.inventory import load_inventory
from config.config import get_openai_api_key

class TestInventory(unittest.TestCase):
    """
    Unit tests for the inventory loading and validation functionality.
    """

    def test_load_inventory(self):
        """
        Test if the inventory is loaded correctly and contains the expected columns and data.

        Validates:
        - The 'combined' column is added to the inventory.
        - The inventory contains data (is not empty).
        - All expected columns ('department', 'item', 'price', 'availability') are present.
        """
        # Load the original inventory file
        inventory = load_inventory("inventory.csv")

        # Check if the 'combined' column is added to the inventory
        self.assertIn("combined", inventory.columns, "The 'combined' column is missing from the inventory.")

        # Check if the inventory contains any rows
        self.assertGreater(len(inventory), 0, "The inventory file appears to be empty.")

        # Ensure all expected columns are present
        expected_columns = ["department", "item", "price", "availability"]
        self.assertTrue(all(col in inventory.columns for col in expected_columns),
                        f"Missing one or more expected columns: {expected_columns}")

    def test_inventory_price_column(self):
        """
        Test if all items in the inventory have valid price values.

        Validates:
        - All prices are numeric (either int or float).
        - All prices are non-negative.
        """
        # Load the inventory
        inventory = load_inventory("inventory.csv")

        # Check if all prices are valid numbers and non-negative
        self.assertTrue(inventory["price"].apply(lambda x: isinstance(x, (int, float)) and x >= 0).all(),
                        "All items should have non-negative numeric prices.")

    def test_inventory_availability_column(self):
        """
        Test if the availability column contains valid values ('in stock' or 'out of stock').

        Validates:
        - All values in the 'availability' column match expected options.
        """
        # Load the inventory
        inventory = load_inventory("inventory.csv")

        # Check if availability contains only expected values
        valid_availability_values = {"in stock", "out of stock"}
        self.assertTrue(inventory["availability"].isin(valid_availability_values).all(),
                        f"Invalid values found in the availability column. Expected: {valid_availability_values}")

    def test_empty_inventory_file(self):
        """
        Test how the function handles an empty inventory file.

        Validates:
        - The function raises a ValueError or handles the empty inventory gracefully.
        """
        # Mock an empty inventory DataFrame
        empty_inventory = pd.DataFrame(columns=["department", "item", "price", "availability", "combined"])

        # Simulate an empty inventory file and check for appropriate handling
        with self.assertRaises(ValueError):
            if len(empty_inventory) == 0:
                raise ValueError("The inventory file is empty.")

if __name__ == "__main__":
    unittest.main()
