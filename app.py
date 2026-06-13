import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] ="true"
print(os.getenv("LANGCHAIN_API_KEY"))