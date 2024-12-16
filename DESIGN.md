# DESIGN.md

## 1. Introduction
The General Store Query System is a command-line interface (CLI) application that leverages a Large Language Model (LLM) and a vector-based retrieval system to interpret and process customer queries for a general store. It efficiently retrieves product information such as department, availability, and price based on natural language queries. By combining Retrieval-Augmented Generation (RAG) with prompt engineering, the system ensures accurate and user-friendly responses while optimizing performance.

---

## 2. System Architecture

### Components
1. **LLM (GPT-3.5)**: Interprets queries, determines departments, and generates responses.
2. **Embedding Generator**: Uses `all-MiniLM-L6-v2` to convert text into dense vector embeddings.
3. **FAISS Vector Database**: Stores inventory embeddings for efficient searches to match queries with inventory items.
4. **Inventory Module**: Loads and preprocesses product data.
5. **Query Processing Module**: Handles query interpretation, department routing, and spelling correction.
6. **Cache Mechanism**: Caches embeddings to optimize repeated queries.
7. **CLI**: Allows users to input natural language queries and view results.

---

## 3. System Workflow

1. **Initialization**:
   - Load inventory data and FAISS index.
   - Preload cached query embeddings.
2. **User Query Handling**:
   - Validate and process user input.
3. **Query Processing**:
   - Use LLM to interpret the query and identify the requested item.
   - Apply spelling correction if necessary.
4. **Department Routing**:
   - Determine the relevant department using the LLM.
5. **Embedding and Retrieval**:
   - Embed the query and retrieve the top 5 matching items from FAISS.
6. **Response Generation**:
   - Use LLM to generate user-facing responses based on retrieved results.
7. **Result Display**:
   - Present responses to the user via CLI.

---

## 4. Design Choices

### Key Decisions
- **Embedding Model (`all-MiniLM-L6-v2`)**: Lightweight and efficient for small-scale RAG systems.
- **Vector Database (FAISS)**: Optimized for fast, scalable similarity searches.
- **LLM (GPT-3.5 Turbo)**: Provides robust natural language understanding and generation.
- **Caching**: Reduces redundant computations for repeated queries, improving performance.

---

## 5. Scalability and Optimization

### Scalability
- **Distributed FAISS**: Enable handling larger datasets by deploying distributed FAISS.
- **Cloud Deployment**: Use AWS, Azure, or GCP to support concurrent users.
- **Enhanced Caching**: Implement Redis for distributed caching across multiple servers.

### Optimization
- **Precomputed Embeddings**: Cache embeddings for frequently queried items.
- **Prompt Efficiency**: Minimize token usage to reduce LLM API costs.
- **Robust Error Handling**: Ensure resilience against API failures and invalid inputs.

---

## 6. Performance Metrics

1. **Response Time**:
   - Time taken to process user queries, including LLM interaction, embedding generation, and FAISS retrieval.

2. **Query Resolution Rate**:
   - Percentage of queries successfully resolved without errors or clarifications.

3. **Precision and Recall**:
   - Precision: Proportion of relevant items in retrieved results.
   - Recall: Proportion of relevant items retrieved from the inventory.

4. **API Latency and Cost**:
   - Time and token usage for LLM API calls, focusing on prompt optimization to minimize cost.

5. **Memory Usage**:
   - Memory consumption during FAISS operations and caching.

6. **Fallback Rate**:
   - Frequency of fallback mechanisms like spelling corrections or query clarifications.

---

## 7. Future Enhancements

1. **Handling Complex Queries**:
   - Enable processing of multiple items or compound queries in a single request to provide more comprehensive results.

2. **Streamlined Clarifications**:
   - Minimize repetitive clarification questions by improving LLM prompts and adding query disambiguation.

3. **Conversation History**:
   - Implement user session tracking to maintain conversational context and handle multi-turn queries effectively.

4. **Enhanced Conversational Ability**:
   - Extend the LLM’s general conversational capabilities beyond information retrieval for better user interaction.

5. **Model Fine-Tuning**:
   - Fine-tune the LLM with specific training data to reduce errors and improve accuracy.

6. **Optimized API Usage**:
   - Introduce batch inference and request batching to minimize LLM API usage and reduce operational costs.



