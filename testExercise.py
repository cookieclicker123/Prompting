import os

os.environ["OPENAI_API_KEY"] = "API_KEY_HERE"

import json
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 0. Update the model name and model kwargs:
chat = ChatOpenAI(model="<<model name>>", model_kwargs={})

# 1. Create a system message prompt:
system_message =

# 2. Create a user message prompt:
user_message =

# 3. Call the chat model:
chat()

# 4. Update this try, except block to handle the response:
try:
    pass
except json.decoder.JSONDecodeError:
    pass