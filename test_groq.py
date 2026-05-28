from dotenv import load_dotenv

from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()


# Initialize Groq model
llm = ChatGroq(

    model="llama-3.1-8b-instant",

    temperature=0.5
)


# Send prompt
response = llm.invoke("Hello")

print(response.content)