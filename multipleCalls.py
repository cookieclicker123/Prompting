import os

os.environ["OPENAI_API_KEY"] = "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"

from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.json import SimpleJsonOutputParser

chat = ChatOpenAI(model="gpt-3.5-turbo-1106",
                  model_kwargs={'response_format': {"type": "json_object"}})

chat_prompt = ChatPromptTemplate.from_messages(
    ("system", """I want you to extract the person name, age and a description from the following text.
    Here is the JSON schema:
    "name": string
    "age": int
    "description": string
    {message_to_extract}
    ---
    If there are multiple people, then put them in a 'persons' key, which is a list of the above schema.
    """)
)
chain = (
    chat_prompt
    | chat
    | SimpleJsonOutputParser()
)

multiple_results = chain.invoke({
    "message_to_extract": '''James is 30 years old and he is a software engineer, he likes to play tennis and he lives in London.
    John is 35 years old and he is a data engineer and he lives in New York, He likes to play football.
    Mark is 40 years old is a Java Developer and he lives in London. He doesn't have many hobbies.
    '''
})

print(multiple_results)

print("--------------------")

from pydantic import BaseModel
from typing import List
from langchain.chains.openai_tools import create_extraction_chain_pydantic

# Make sure to use a recent model that supports tools
model = ChatOpenAI(model="gpt-3.5-turbo-1106")


class Person(BaseModel):
    """A person object that we want to extract from the text"""
    name: str
    age: int
    description: str

# Previous we had to write this:
class Persons(BaseModel):
    persons: List[Person]

chain = create_extraction_chain_pydantic(Persons, model)

print(chain.invoke({"input":"James is 30 and Sarah is 26 years old."}))

