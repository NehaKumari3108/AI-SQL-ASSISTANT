from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

schema_docs = [

"""
Table orders

Columns:
order_id
order_date
order_time

Primary Key:
order_id
""",

"""
Table order_details

Columns:
order_details_id
order_id
pizza_id
quantity

Foreign Keys:
order_id -> orders.order_id
pizza_id -> pizzas.pizza_id
""",

"""
Table pizzas

Columns:
pizza_id
pizza_type_id
size
price

Foreign Keys:
pizza_type_id -> pizza_types.pizza_type_id
""",

"""
Table pizza_types

Columns:
pizza_type_id
name
category
ingredients
"""
]

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma.from_texts(
    texts=schema_docs,
    embedding=embeddings,
    persist_directory="./schema_embeddings"
)

print("Embeddings created successfully!")