from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate 
from langchain.schema import BaseOutputParser 
from dotenv import load_dotenv
import os

os.environ["OPENAI_API_KEY"] = "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"
load_dotenv()

chat_model   = ChatOpenAI()

class commaSeparatedListOutputParser(BaseOutputParser):
    def parse(self, text: str):
        return text.strip().split(", ")
    

template  = """You are a helpful assistant who generates comma separated lists.
                A user will pass in a catagory ad you should generate 5 objects in that catagory in a comma separated list. 
                ONLY return a comma separated list and nothing more"""

human_template = "{text}"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template)
])

chain =  chat_prompt | chat_model | commaSeparatedListOutputParser()
result  = chain.invoke({"text":"colours"})
print(result)


