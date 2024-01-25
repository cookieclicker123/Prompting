import os

os.environ["OPENAI_API_KEY"] = "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"

import json
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

chat = ChatOpenAI(model="gpt-3.5-turbo-1106", model_kwargs={'response_format': {"type": "json_object"}})

system_message = SystemMessage(
    content='''I want you to extract the person name, age and a description from the following text.
    Here is the JSON object, output:
    {
        "name": string,
        "age": int,
        "description": string
    }
    ''')

user_message = HumanMessage(content='''John is 20 years old. He is a student at the University of California,
                            Berkeley. He is a very smart student.''')

json_object = chat([
    system_message,
    user_message
])

print(json_object)

try:
    json_object = json.loads(json_object.content)
    print(json_object)
except json.decoder.JSONDecodeError:
    print(json_object.content)

print("--------------------")

print(json_object)

print("--------------------")

print(json_object["name"], json_object["age"], json_object["description"])

