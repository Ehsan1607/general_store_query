import os
import pandas as pd
import pickle

def load_inventory(file_path):
    """
    Load the inventory data from a CSV file and preprocess it.

    Args:
        file_path (str): Path to the inventory CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the inventory data, with an additional 
                      'combined' column for embedding purposes.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The inventory file '{file_path}' does not exist. Please provide a valid file.")
    
    inventory = pd.read_csv(file_path)
    
    if inventory.empty:
        raise ValueError("The inventory file is empty. Please ensure it contains valid data.")
    
    inventory['combined'] = inventory['department'] + ' ' + inventory['item']
    return inventory
