# README.md

## Quick Start
The General Store Query System is a command-line application that uses a Large Language Model (LLM) to interpret and process user queries about a general store inventory. It retrieves product details such as availability, price, and department using Retrieval-Augmented Generation (RAG).

---

## Prerequisites

1. **Python**: Ensure Python 3.10 is installed.
2. **Dependencies**: Install required Python libraries using the provided `requirements.txt` file.
3. **FAISS Index**: Either create a new FAISS index or use the provided one.
4. **Environment Variable**: Set the `OPENAI_API_KEY` in your environment.

---

## Structure
The project structure is as follows:

```
├── main.py                 # Entry point for the application
├── requirements.txt        # Dependencies
├── inventory.csv           # Inventory data
├── DESIGN.md               # Design documentation
├── README.md               # Read me file
├── config/                 # Configuration folder
│   └── config.py           # Configuration for API keys
├── faiss_index/            # Folder for the FAISS index
│   └── index.bin           # Prebuilt FAISS index
├── modules/                # Core modules
│   ├── embedding.py        # Embedding generation and FAISS retrieval
│   ├── inventory.py        # Inventory loading and preprocessing
│   ├── query_processing.py # Query interpretation and department routing
│   └── __init__.py         # Package initialization file
├── llm/                    # LLM-related modules
│   ├── call_llm.py         # Wrapper for LLM calls
│   └── __init__.py         # Package initialization file
├── tests/                  # Unit tests
│   ├── test_embeddings.py  # Tests for embedding functionality
│   ├── test_inventory.py   # Tests for inventory module
│   ├── test_query_processing.py # Tests for query processing module
│   └── __init__.py         # Package initialization file
└── embedding_cache.pkl     # Cache file for query embeddings
```

---

## Set Up the Environment

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd general_store_query
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set the API Key**:
   - Set your OpenAI API key as an environment variable: For Windows (Command Prompt)
     ```bash
     set OPENAI_API_KEY=<your_openai_api_key>
     ```

4. **Verify the Setup**:
   - Ensure all dependencies are installed and the `inventory.csv` file is present.

---

## Run the Application
To start the CLI application, run:

```bash
python main.py
```

You can then enter natural language queries, such as:
- *"Do you have bananas in stock?"
- *"What is the price of milk?"*

Type `exit` to quit the application.

---

## Test the Application

### Run All Tests

To run all test files at once:
```bash
python -m unittest discover
```

### Run Individual Test Files

To run a specific test file:
```bash
python -m unittest tests.test_inventory
python -m unittest tests.test_embeddings
python -m unittest tests.test_query_processing
```

---

## Description of Test Files

1. **`test_inventory.py`**:
   - Validates inventory loading and preprocessing.
   - Ensures the presence of required columns and data integrity.

2. **`test_embeddings.py`**:
   - Tests embedding generation, FAISS index creation, and query matching.
   - Includes tests for invalid inputs and edge cases.

3. **`test_query_processing.py`**:
   - Tests LLM-based query interpretation and department routing.
   - Validates spelling correction functionality.

---

## Sample Conversation

**User Query**:
```bash
Please enter your query below: (or type 'exit' to quit): Do you have apples?
```
**Response**:
```bash
The item "apple" belongs to the grocery department.
Yes, we have apples available in the grocery department priced at $0.89. They are currently in stock.
```

**User Query**:
```bash
Please enter your query below: (or type 'exit' to quit): What electronics are available?
```
**Response**:
```bash
Could you please specify the item you're looking for? For example, "Do you have smartphones?" or "Is a laptop available?" This will help me assist you better.
```

**User Query**:
```bash
Please enter your query below: (or type 'exit' to quit): Do you have bananas and oranges?
```
**Response**:
```bash
The item "banana" belongs to the grocery department.
Yes, we have bananas available in the grocery department priced at $0.99. They are currently in stock.
```

**User Query**:
```bash
Please enter your query below: (or type 'exit' to quit): What is the price of milk?
```
**Response**:
```bash
The item "milk" belongs to the grocery department.
Milk is available in the grocery department priced at $2.49. It is currently in stock.
```

**User Query**:
```bash
Please enter your query below: (or type 'exit' to quit): What fruits are available?
```
**Response**:
```bash
Could you please specify the fruit you're looking for? For example, "Do you have apples?" or "Are oranges available?"
```

**Exit**:
```bash
Please enter your query below: (or type 'exit' to quit): exit
Goodbye!
```
