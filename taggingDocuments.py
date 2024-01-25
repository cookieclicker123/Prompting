import os
os.environ['OPENAI_API_KEY'] = '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'

from langchain.document_loaders.sitemap import SitemapLoader
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains import create_tagging_chain, create_tagging_chain_pydantic
import pandas as pd

sitemap_loader = SitemapLoader(web_path="https://understandingdata.com/sitemap.xml")
sitemap_loader.requests_per_second = 5
docs = sitemap_loader.load()

# Schema
schema = {
    "properties": {
        "sentiment": {"type": "string" },
        "aggressiveness": {"type": "integer"},
        "primary_topic": {"type": "string", "description": "The main topic of the document."},
    },
     "required": ["primary_topic", "sentiment", "aggressiveness"],
}

# LLM
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
chain = create_tagging_chain(schema, llm, output_key='output')

results = []

# Remove the 0:10 to run on all documents:
for doc in docs[0:10]:
    chain_result = chain({'input': doc.page_content})
    results.append(chain_result['output'])


df = pd.DataFrame(results)

docs[0].metadata
print("--------------------")
# Combine the URLs with the results
df['url'] = [doc.metadata['source'] for doc in docs[0:10]]

print(df)