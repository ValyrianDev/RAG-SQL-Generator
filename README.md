
# RAG-SQL-Generator

This project leverages Retrieval Augmented Generation (RAG) to enhance SQL query generation for Oracle Autonomous Data Warehouse (ADW) using the OCI Generative AI service and Marqo AI. By using vector search to narrow down relevant schema data, we provide context to the LLM, enabling it to generate accurate SQL queries.

## Features

- **Oracle ADW Integration**: Utilize Oracle's enterprise-grade data warehouse for scalable and secure data storage.
- **Marqo AI**: Vectorize and search schema data efficiently.
- **OCI Generative AI**: Deploy and use the Llama3 70B model for cost-effective and improved SQL generation.

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- Docker
- Oracle Cloud account
- Git

### Step-by-Step Guide

#### 1. Clone the Repository

```bash
git clone https://github.com/ValyrianDev/RAG-SQL-Generator.git
cd RAG-SQL-Generator
```

#### 2. Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables

Create a `.env` file in the root directory and populate it with your database and OCI credentials:

```env
DB_USERNAME=your_db_username
DB_PASSWORD=your_db_password
DB_WALLET_LOCATION=path_to_your_wallet
DB_CONFIG_DIR=path_to_your_wallet
DB_DSN=your_dsn
DB_SCHEMA=your_schema
OCI_COMPARTMENT_ID=your_compartment_id
OCI_CONFIG_PROFILE=your_config_profile
OCI_CONFIG_FILE=path_to_your_oci_config_file
OCI_ENDPOINT=your_oci_service_endpoint
OCI_MODEL_ID=your_model_id
```

#### 5. Set Up Oracle ADW

Follow these steps to create and set up an Oracle ADW instance:

1. Log into your OCI console.
2. Navigate to `Autonomous Data Warehouse` under `Oracle Database`.
3. Create a new instance with the `Always Free` configuration.
4. Download your instance wallet and keep it secure.

#### 6. Populate ADW with Sample Data

1. Navigate to `Database Actions` in your ADW instance.
2. Run the provided SQL script to create a schema and populate it with sample data.

#### 7. Run Marqo with Docker

```bash
docker pull marqoai/marqo
docker run -d -p 8882:8882 marqoai/marqo
```

#### 8. Initialize the Project

Run the main script to fetch the schema, set up the Marqo index, and start generating SQL queries:

```bash
python main.py
```

## Usage

1. **Initial Setup**: Run the script and choose to refresh the database schema if needed.
2. **Generate SQL Queries**: Enter your query when prompted. The script will search the Marqo index, use the LLM to generate SQL, and execute the query against ADW.
