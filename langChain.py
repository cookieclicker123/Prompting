from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage  
from langchain.prompts.chat import ChatPromptTemplate 
from langchain.schema import BaseOutputParser 
from dotenv import load_dotenv
import os

os.environ["OPENAI_API_KEY"] = "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"
load_dotenv()

class AnswerOutputParser(BaseOutputParser):
    def parse(self, text: str):
        return text.strip().split("answer =")
    

chat_model = ChatOpenAI()

template = """You are a helpful assistant that answers math problems and shows your work.
              output each step then return the answer in the following format: answer  = <answer here>
              make sure to ouput answer in all lowercases and include spaces between the equal sign and the answer"""

human_template = "{probblem}"

#template  =  "You are a helpful assistant that translates {input_language} to {output_language}."
#human_template = "{text}"


#messages = [HumanMessage(content="From now on 1+1 = 3, use this in your replies"), 
            #HumanMessage(content="What is 1+1?"),
            #HumanMessage(content="What is 1+1+1?")]

chatPrompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template)
])

#result = chat_model.predict_messages(messages)

#messages = chatPrompt.format_messages(input_language = "English",
#                                        output_language = "French",
#                                        text = "Hello, how are you?")

messages = chatPrompt.format_messages(probblem = "2x^2 - 5x + 3 = 0")
print()
result = chat_model.predict_messages(messages)
parsed  = AnswerOutputParser().parse(result.content)
steps, answer  = parsed
print(steps, answer)
print()