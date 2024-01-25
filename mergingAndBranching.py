import os

os.environ["OPENAI_API_KEY"] = "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"


from operator import itemgetter
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnablePassthrough

branch = RunnableBranch(
                (lambda x: x == 'hello', lambda x: x),
                (lambda x: isinstance(x, str), lambda x: x.upper()),
                (lambda x: "This is the default case, in case no above lambda functions match."),
            )

print(branch.invoke("hello")) # "hello"
print(branch.invoke(None)) # "This is the default case"

planner = (
    ChatPromptTemplate.from_template("Generate an argument about: {input}")
    | ChatOpenAI()
    | StrOutputParser()
    | {"base_response": RunnablePassthrough()}
)

arguments_for = (
    ChatPromptTemplate.from_template(
        "List the pros or positive aspects of {base_response}"
    )
    | ChatOpenAI()
    | StrOutputParser()
)

arguments_against = (
    ChatPromptTemplate.from_template(
        "List the cons or negative aspects of {base_response}"
    )
    | ChatOpenAI()
    | StrOutputParser()
)

final_responder = (
    ChatPromptTemplate.from_messages(
        [
            ("ai", "{original_response}"),
            ("human", "Pros:\n{results_1}\n\nCons:\n{results_2}"),
            ("system", "Generate a final response given the critique"),
        ]
    )
    | ChatOpenAI()
    | StrOutputParser()
)

chain = (
    planner
    | {
        "results_1": arguments_for,
        "results_2": arguments_against,
        "original_response": itemgetter("base_response"),
    }
    | final_responder
)

print(chain.invoke({"input": "What is the best programming language?"}))