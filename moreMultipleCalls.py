
from langchain_openai.chat_models import ChatOpenAI

import os

os.environ["OPENAI_API_KEY"] = "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"

from pydantic import BaseModel

from typing import List
from langchain.chains.openai_tools import create_extraction_chain_pydantic

# Make sure to use a recent model that supports tools
model = ChatOpenAI(model="gpt-3.5-turbo-1106")

class Person(BaseModel):
    """A person object that we want to extract from the text"""
    name: str
    age: int

# Previous we had to write this:
class Persons(BaseModel):
    persons: List[Person]

chain = create_extraction_chain_pydantic(Person, model)

print(chain.invoke({"input": "James is 30 and Sarah is 26 years old."}))
