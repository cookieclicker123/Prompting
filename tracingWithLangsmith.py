import os
os.environ["OPENAI_API_KEY"] = "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"

from langchain import hub

prompt = hub.pull("homanp/question-answer-pair")
prompt_two = hub.pull("gitmaxd/synthetic-training-data")
prompt_three = hub.pull("rlm/text-to-sql")
rag_prompt = hub.pull("rlm/rag-prompt")

print(prompt)
print("--------------------")
print(prompt_two)

print("--------------------")

print(rag_prompt)
print("--------------------")

print(rag_prompt.messages)
print("--------------------")

# Load docs
from langchain.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
data = loader.load()

# Split
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 0)
all_splits = text_splitter.split_documents(data)

# Store splits
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
vectorstore = FAISS.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())

# RAG prompt
from langchain import hub
prompt = hub.pull("rlm/rag-prompt")

# LLM
from langchain.chains import RetrievalQA
from langchain_openai.chat_models import ChatOpenAI
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# RetrievalQA
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectorstore.as_retriever(),
    chain_type_kwargs={"prompt": prompt}
)
question = "What are the approaches to Task Decomposition?"
result = qa_chain({"query": question})
result["result"]
