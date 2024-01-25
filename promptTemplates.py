import os
os.environ['OPENAI_API_KEY'] = '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'

from langchain_openai.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,

)

chat = ChatOpenAI()

template = "What would be a good company name for a {company_description}. List 3 company names that you like. Make sure that the list is a numbered list."

system_message_prompt = SystemMessagePromptTemplate.from_template(template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt])


# Get a chat completion from the formatted messages
result = chat.invoke(
    chat_prompt.format_prompt(company_description="Data engineering").to_messages()
)

print(result.content)
