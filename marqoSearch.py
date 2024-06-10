import marqo
import json


def search_marqo(user_query, index_name="schema-index", limit=3, marqo_url="http://localhost:8882",
                 output_file='marqo_results.json'):
    # Initialize Marqo client
    mq = marqo.Client(url=marqo_url)

    # Perform the search query with limit
    results = mq.index(index_name).search(q=user_query, limit=limit)

    # Save the search results to a file for use by the next script
    with open(output_file, 'w') as outfile:
        json.dump(results, outfile)

    return results


