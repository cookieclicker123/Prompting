import os
os.environ['OPENAI_API_KEY'] = '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'

from bs4 import BeautifulSoup
from langchain_community.document_loaders import TextLoader
import requests

# Get this file and save it locally:
url = "https://github.com/hammer-mt/thumb/blob/master/README.md"

# Save it locally:
r = requests.get(url)

# Extract the text from the HTML:
soup = BeautifulSoup(r.text, 'html.parser')
text = soup.get_text()

with open("README.md", "w") as f:
    f.write(text)

loader = TextLoader('README.md')
docs = loader.load()


from langchain_core.documents import Document
[ Document(page_content='test', metadata={'test': 'test'}) ] 

# Split the text into sentences:
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 300,
    chunk_overlap  = 50,
    length_function = len,
    is_separator_regex = False,
)

final_docs = text_splitter.split_documents(loader.load())

len(final_docs)

from langchain_openai.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain

chat = ChatOpenAI()

chain = load_summarize_chain(llm=chat, chain_type="map_reduce")
chain.invoke({
    "input_documents": final_docs,
})