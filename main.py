import os
import json
import re
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, inspect
from langchain_community.utilities import SQLDatabase
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langsmith import traceable





# -------------------------
# Load Environment Variables
# -------------------------
load_dotenv()

api_key = os.getenv("LANGCHAIN_API_KEY")

if not api_key:
    raise ValueError("LANGCHAIN_API_KEY not found in .env file")

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = api_key
os.environ["LANGCHAIN_PROJECT"] = "SQL Assistant"

# -------------------------
# Database Connection
# -------------------------
db_url = "sqlite:///pizzahut.db"



db = SQLDatabase.from_uri(db_url)

# -------------------------
# Extract Schema
# -------------------------
@traceable #(name="Extract Schema")
def extract_schema(db_url):

    inspector = inspect(create_engine(db_url))

    schema_text = ""

    for table_name in inspector.get_table_names():

        schema_text += f"\nTable:{table_name}\n"

        columns = inspector.get_columns(table_name)
        
        for col in columns:
            schema_text += (
                f"  - {col['name']} "
                f"({col['type']})\n"
            )
        pk = inspector.get_pk_constraint(table_name)

        if pk["constrained_columns"]:
            schema_text += (
                f"Primary Key: "
                f"{pk['constrained_columns']}\n"
            )
        fks = inspector.get_foreign_keys(table_name)

        for fk in fks:
            schema_text += (
                f"Foreign Key: "
                f"{fk['constrained_columns']} ->"
                f"{fk['referred_table']}"
                f"({fk['referred_columns']})\n"
            )

    return schema_text


# -------------------------
# Text To SQL
# -------------------------
@traceable #(name="Text To SQL")
def text_to_sql(schema, prompt):
    SYSTEM_PROMPT = """
    You are an expert SQLite SQL assistant for a Pizza Hut database.
    Your job is to convert natural language questions into accurate SQL queries.

Database Schema:
orders
order_id (PRIMARY KEY)
order_date
order_time
order_details
order_details_id (PRIMARY KEY)
order_id (FOREIGN KEY → orders.order_id)
pizza_id (FOREIGN KEY → pizzas.pizza_id)
quantity
pizzas
pizza_id (PRIMARY KEY)
pizza_type_id (FOREIGN KEY → pizza_types.pizza_type_id)
size
price
pizza_types
pizza_type_id (PRIMARY KEY)
name
category
ingredients
Rules:
Always generate only SQL queries (no explanation unless asked).
Use correct JOINs when multiple tables are needed.
Always use correct table aliases consistently.
Use only the aliases defined in the FROM/JOIN clause.
Do not invent new aliases like p, x, or y.
Ensure GROUP BY columns match SELECT columns exactly.
Prefer explicit column names (no SELECT *).
Use table aliases for readability.
Optimize queries for readability and correctness.
Assume SQLite/MySQL compatibility.
Output Format:
Return only the result.
"""

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            (
                "user",
                "Schema:\n{schema}\n\nQuestion:\n{prompt}\n\nSQL Query:"
            )
        ]
    )

    model = OllamaLLM(
        model="qwen2.5:7b"
    )

    chain = prompt_template | model

    sql_query = chain.invoke(
        {
            "schema": schema,
            "prompt": prompt
        }
    )

    sql_query = re.sub(r"```sql|```", "", sql_query).strip()
    return sql_query


# -------------------------
# Execute SQL
# -------------------------
@traceable #(name="SQL Execution")
def get_sql_query_from_user_input(user_input):

    schema = extract_schema(db_url)

    sql_query = text_to_sql(
        schema,
        user_input
    )

    engine = create_engine("sqlite:///pizzahut.db")


    df = pd.read_sql_query(sql_query,engine)

    return df