# MongoDB Helper Library

This project provides a collection of helper functions and utilities to simplify interactions with MongoDB using Python. It encapsulates CRUD operations, aggregation, indexing, and schema validation, making it easier to work with MongoDB.

## Project Structure

- **aggregation/**
  - `aggregation.py`: Contains helper functions for aggregation pipelines.

- **client/**
  - `close_mongo_client.py`: Closes the MongoDB client connection.
  - `get_mongo_client.py`: Returns a MongoDB client connection.

- **crud/**
  - `bulk.py`: Bulk operations for inserts, updates, and deletes.
  - `delete_document.py`: Helper to delete a document.
  - `find_document.py`: Helper to find a document.
  - `get_document.py`: Helper to retrieve a document by ID.
  - `insert_document.py`: Helper to insert a document.
  - `update_document.py`: Helper to update a document.

- **indexing/**
  - `indexing.py`: Functions for creating, listing, and dropping indexes.

- **validate/**
  - `validate_document.py`: Document schema validation functions.

## Features

### 1. **Client Management**

- `get_mongo_client.py`: Provides a function to initialize and return a MongoDB client connection.
- `close_mongo_client.py`: Provides a function to close an existing MongoDB client connection.

### 2. **CRUD Operations**

The `crud/` directory contains helpers for standard database operations:

- **Insert Documents**: Insert single or multiple documents into a collection.
- **Update Documents**: Update documents using filters.
- **Delete Documents**: Delete documents from a collection.
- **Find Documents**: Find a document with specific criteria.
- **Bulk Operations**: Perform bulk inserts, updates, or deletes.

### 3. **Aggregation**

The `aggregation/aggregation.py` file provides helper functions to perform MongoDB aggregation operations, such as grouping data or filtering with complex pipelines.

### 4. **Indexing**

The `indexing/indexing.py` file contains helper functions for managing indexes:

- Create indexes for fields to improve query performance.
- List all existing indexes on a collection.
- Drop specific indexes or all indexes in a collection.

### 5. **Document Validation**

The `validate/validate_document.py` file provides functions to validate the structure and schema of MongoDB documents before inserting or updating.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/mongo_helpers.git
   ```

2. Install dependencies using **Poetry**:

   If you don't have Poetry installed, you can install it by following the instructions on the [Poetry website](https://python-poetry.org/docs/#installation). Once Poetry is installed, run the following command in the project directory:

   ```bash
   poetry install
   ```

   This will create a virtual environment and install all the dependencies specified in the `pyproject.toml` file.

3. Activate the virtual environment (if needed):

   Poetry automatically creates and manages a virtual environment for your project. You can activate it using:

   ```bash
   poetry shell
   ```

4. Set up MongoDB:

   Ensure you have MongoDB installed and running on your system. You can change the MongoDB URI in your client functions (`client/get_mongo_client.py`) if needed.

## Usage

### Example: Insert and Retrieve a Document

```python
from client.get_mongo_client import get_mongo_client
from crud.insert_document import insert_document
from crud.find_document import find_document

# Get MongoDB client
client = get_mongo_client()
db = client["mydatabase"]
collection = db["mycollection"]

# Insert a document
doc = {"name": "Alice", "age": 30}
insert_document(collection, doc)

# Find a document
query = {"name": "Alice"}
result = find_document(collection, query)
print(result)

# Close the client connection
client.close()
```

### Example: Perform Aggregation

```python
from aggregation.aggregation import group_by_field

# Group documents by 'name' field
results = group_by_field(collection, "name")
for result in results:
    print(result)
```

### Example: Validate a Document

```python
from validate.validate_document import validate_document_schema

# Define a simple schema
schema = {
    "name": str,
    "age": int,
}

# Validate a document
document = {"name": "Alice", "age": 30}
is_valid, message = validate_document_schema(document, schema)
print(is_valid, message)
```

## Running Tests

If you have unit tests for this project, you can run them using Poetry as well. Make sure you have `pytest` or any other testing framework included in the `pyproject.toml` file, and run:

```bash
poetry run pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---