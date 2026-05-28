from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.0-flash",
    temperature = 0.3
)

response = llm.invoke("Hello")

print(response.content)