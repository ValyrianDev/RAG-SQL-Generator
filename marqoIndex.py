import marqo
import json


def setup_marqo_index(schema_file='schema_info.json', index_name="schema-index", marqo_url="http://localhost:8882",
                      model="hf/e5-base-v2"):
    # Initialize Marqo client
    mq = marqo.Client(url=marqo_url)

    # Delete existing index if it exists
    try:
        mq.index(index_name).delete()
    except:
        pass  # Ignore error if index does not exist

    # Create a new index
    mq.create_index(index_name, model=model)

    # Read the JSON file
    with open(schema_file, 'r') as json_file:
        parsed_tables = json.load(json_file)

    # Create a list of documents for Marqo
    documents = []
    for table in parsed_tables:
        doc = {
            # Account for null values
            "Table": table["Table"] if table["Table"] is not None else "",
            "Columns": table["Columns"] if table["Columns"] is not None else "",
            "Constraints": table["Constraints"] if table["Constraints"] is not None else "",
            "Column_Comments": ' '.join([f"{col}: {comment}" for col, comment in table["Column Comments"].items()]) if
            table["Column Comments"] is not None else "",
            "Table_Comment": table["Table Comment"] if table["Table Comment"] is not None else ""
        }
        documents.append(doc)

    # Add documents to the index and check for errors
    response = mq.index(index_name).add_documents(documents, tensor_fields=["Columns", "Constraints", "Column_Comments",
                                                                            "Table_Comment"])

    # Print success message
    print("Marqo Index has been created")

    return response
