Overview

This project leverages Oracle Cloud Infrastructure (OCI) Generative AI service for large language models (LLM) and Marqo for indexing and searching vectors. It aims to enhance SQL query generation and execution against Oracle Autonomous Data Warehouse (ADW) by utilizing Data Definition Language (DDL) and comments as context to improve query accuracy and relevance based on natural language inputs.

Features

- OCI Gen AI Service: Utilizes OCI's Generative AI capabilities, specifically with Llama3 70B model, to interpret natural language queries and generate SQL commands.
- Marqo Integration: Implements Marqo AI for efficient indexing and vector-based search to handle schema and metadata information.
- Oracle ADW Connection: Connects to Oracle ADW to execute generated SQL queries and retrieve data.
- Context-Aware SQL Generation: Enhances SQL query generation by incorporating DDL and comments from the database schema for more accurate results.
