import os

os.environ["OPENAI_API_KEY"] = "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"

from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.json import SimpleJsonOutputParser

chat = ChatOpenAI(model="gpt-3.5-turbo-1106", model_kwargs={'response_format': {"type": "json_object"}})

chat_prompt = ChatPromptTemplate.from_messages(
    ("system", """I want you to extract the person name, age and a description from the following text.
    Here is the JSON schema:
    "name": string
    "age": int
    "description": string
    {message_to_extract}
    """)
)


chain = (
    chat_prompt
    | chat
    | SimpleJsonOutputParser() # The output parser is optional, but it makes the output easier to parse, rather than using json.loads
)

result = chain.invoke({
    "message_to_extract": "I am 30 years old and my name is John Doe. I am a software engineer."
})

print(result)