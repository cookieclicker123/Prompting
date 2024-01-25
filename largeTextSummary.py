import os



from langchain_openai.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain_community.document_loaders import WebBaseLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate

os.environ['OPENAI_API_KEY'] = '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'
chat = ChatOpenAI()

loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
docs = loader.load()

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
chain = load_summarize_chain(llm, chain_type="stuff")

chain.invoke(docs)
chain.get_summary()
chain.get_summary().content



