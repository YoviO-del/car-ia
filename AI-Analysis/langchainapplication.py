import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_core.prompts import PromptTemplate

load_dotenv(r"C:\Users\yovin\Desktop\Car-IA\.venv-1\.env")
api_key = os.getenv('OPENAI_API_KEY')


loader = CSVLoader("C:/Users/yovin/Desktop/Car-IA/listings.csv")
data = loader.load()

question_test = """
    Review the following Linkedin profile:

    - List the profile
    - What college they went to 
    - Where they are from

"""

prompt_template = PromptTemplate.from_template(template=question_test)

llm = ChatOpenAI(model="gpt-5.6",api_key=api_key)

llm_chain = prompt_template | llm

llm_chain.invoke({"question": "Tell me about Yapeth"}) 