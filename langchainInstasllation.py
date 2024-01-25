import os
os.environ['OPENAI_API_KEY'] = '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'



from langchain_openai.chat_models import ChatOpenAI

# chat = ChatOpenAI(openai_api_key="...")

# If you have an envionrment variable set for OPENAI_API_KEY, you can just do:
chat = ChatOpenAI()

response = chat.invoke("Hello, how are you?")

print(response)

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

text = "What would be a good company name for a company that makes colorful socks?"
messages = [HumanMessage(content=text)]
result = chat.invoke(messages)

print(result.content)

print("--------------------")
#Next we will create a system message. This has massive implicaitons for the effectiveness of the model
#If the system has rules, objectives and goals, it will respond far better to the prompts than if it is just a generic 
#model

text = "What would be a good company name for a company that makes colorful socks?"

messages = [SystemMessage(content=text)]
result  = chat.invoke(messages)
print(result.content)

print("--------------------")

#Now we will create a system message with a goal. This will be a goal to create a company name that is memorable

text = "What would be a good company name for a company that makes colorful socks?"

messages = [SystemMessage(content=text, goal="memorable")]
result  = chat.invoke(messages)
print(result.content)

