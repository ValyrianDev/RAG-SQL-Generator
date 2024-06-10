import json
import oci
import re
from dotenv import load_dotenv
import os

load_dotenv()


def generate_sql_query(user_query):
    # Load the search results from the file
    with open('marqo_results.json', 'r') as infile:
        marqo_results = json.load(infile)

    # Prepare the input for OCI Generative AI Service
    marqo_results_str = json.dumps(marqo_results)

    # OCI Generative AI Service setup
    compartment_id = os.getenv("OCI_COMPARTMENT_ID")
    config_profile = os.getenv("OCI_CONFIG_PROFILE")
    config_file = os.getenv("OCI_CONFIG_FILE")
    endpoint = os.getenv("OCI_ENDPOINT")
    model_id = os.getenv("OCI_MODEL_ID")

    config = oci.config.from_file(config_file, config_profile)

    generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(
        config=config,
        service_endpoint=endpoint,
        retry_strategy=oci.retry.NoneRetryStrategy(),
        timeout=(10, 240)
    )

    content = oci.generative_ai_inference.models.TextContent()
    content.text = (f"User query: {user_query}\nMarqo results: {marqo_results_str}\nGenerate a SQL query to answer the "
                    f"user's question in the following format: ```sql\nYOUR QUERY HERE\n```.")
    message = oci.generative_ai_inference.models.Message()
    message.role = "USER"
    message.content = [content]

    chat_request = oci.generative_ai_inference.models.GenericChatRequest()
    chat_request.api_format = oci.generative_ai_inference.models.BaseChatRequest.API_FORMAT_GENERIC
    chat_request.messages = [message]
    chat_request.max_tokens = 1071
    chat_request.temperature = 1
    chat_request.frequency_penalty = 0
    chat_request.top_p = 0.75
    chat_request.top_k = -1

    chat_detail = oci.generative_ai_inference.models.ChatDetails()
    chat_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(model_id=model_id)
    chat_detail.chat_request = chat_request
    chat_detail.compartment_id = compartment_id

    # Get response from OCI Generative AI Service
    chat_response = generative_ai_inference_client.chat(chat_detail)

    # Extract the message content
    message_content = chat_response.data.chat_response.choices[0].message.content[0].text

    # Clean the SQL query
    sql_match = re.search(r'```sql\n(.*?)\n```', message_content, re.DOTALL)
    if sql_match:
        sql_query = sql_match.group(1).strip()
    else:
        raise ValueError("SQL query not found in the response.")

    # Save the SQL query to a file
    with open('generated_query.sql', 'w') as file:
        file.write(sql_query)
    print(f"SQL query saved to generated_query.sql")

    return sql_query
