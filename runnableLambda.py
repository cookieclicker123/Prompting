import os
os.environ["OPENAI_API_KEY"] = "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"

from langchain_core.runnables import RunnableLambda

print(type(RunnableLambda(lambda x: x + 1))) # <class 'langchain.schema.runnable.RunnableLambda'>

chain = RunnableLambda(lambda x: x + 1)

print(chain.invoke(1))

print(chain.invoke(5))

# A RunnableSequence constructed using the `|` operator
sequence = RunnableLambda(lambda x: x + 1) | (lambda x: x * 2)

print(type(sequence)) # <class 'langchain.schema.runnable.RunnableSequence'>
print('\n\n---')
print(sequence.invoke(1)) # 4
print(sequence.batch([1, 2, 3])) # [4, 6, 8]
print("---------------------------")
# A sequence that contains a RunnableParallel constructed using a dict literal
sequence = RunnableLambda(lambda x: x + 1) | {
    "mul_2": RunnableLambda(lambda x: x * 2),
    "mul_5": RunnableLambda(lambda x: x * 5),
}
print(sequence.invoke(1))  # {'mul_2': 4, 'mul_5': 10}
print("---------------------------")
sequence = RunnableLambda(lambda x: x + 1) | {
    'mul_2': RunnableLambda(lambda x: x * 2),
    'mul_5': RunnableLambda(lambda x: x * 5)
} | RunnableLambda(lambda x: x['mul_2'] + x['mul_5'])
print(sequence.invoke(1)) # {'mul_2': 4, 'mul_5': 10}
print("---------------------------")

from langchain_core.runnables import RunnableParallel

parallel = RunnableParallel({
    'mul_2': RunnableLambda(lambda x: x * 2),
    'mul_5': RunnableLambda(lambda x: x * 5)
})

# This is a dictionary, however it will be composed with other runnables when used in a sequence:
parallel_two = {
    'mul_2': RunnableLambda(lambda x: x['input_one'] * 2),
    'mul_5': RunnableLambda(lambda x: x['input_two'] * 5)
}

print(type(parallel)) # <class 'langchain.schema.runnable.RunnableParallel'>
print(type(parallel_two)) # <class 'dict'

chain = parallel | RunnableLambda(lambda x: x['mul_2'] + x['mul_5'])

#help me so this line mutliplies mul 2 by five and mul 5 by 2
print(chain.invoke(5))
print("---------------------------")
second_chain = parallel_two | RunnableLambda(lambda x: x['mul_2'] + x['mul_5'])
print(second_chain.invoke({'input_one': 5, 'input_two': 10}))

print("---------------------------")

parallel = RunnableParallel({
    'mul_2': RunnableLambda(lambda x: x * 2),
    'mul_5': RunnableLambda(lambda x: x * 5)
})


# This is good practice:
test = RunnableLambda(lambda x: x + 1) | parallel
print(test)
print(test.invoke(5))