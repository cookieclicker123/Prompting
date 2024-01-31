import os

os.environ["OPENAI_API_KEY"] = "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"

import pandas as pd
import numpy as np
from tqdm import tqdm

llm_results = [
    "Coding is fun.",
    "I am learning about coding and I wanted to know how to write a for loop, so I decided to learn JavaScript",
    "Using strong types in code is the way forward #dev",
    "learning about data engineering is fun and I had a great time at the conference! #devOps",
    "Have you ever considered that learning DevOps might be useful for your career? See this thread #DevOps #Software",
    "I love making software #dev",
    "I love my dog. #dogs",
    "Cats are awesome. #cats",
    "It's always good to be with your family and friends."
    "Software is awesome #software"
    "Data science is really fun and I can't wait to share what I've learned with you at DataScienceCon! #data"
]

# Social media post text length:
social_post_df = pd.DataFrame(
    {"generated_social_media_post": llm_results}  # Adding a toy dataset for LLM results
)

def eval_has_hashtag(text: str) -> bool:
    if "#" in text:
        return True
    else:
        return False

def eval_length_of_social_post(text: str) -> bool:
    if len(text) >= 30 and len(text) <= 150:
        return True
    else:
        return False

# This is used for one-hot encoding the boolean results into an integer
# so that it can be counted when calculating accuracy.
def convert_boolean_to_one_hot_encoding(bool_result: bool) -> int:
    if bool_result: return 1
    return 0

eval_functions = {
    "eval_has_hashtag": eval_has_hashtag,
    "eval_length_of_social_post": eval_length_of_social_post,
}

# For each row, loop through:
for index, row in social_post_df.iterrows():
    # For each eval, run the eval and store the output in a new column for that row:
    for key, value in eval_functions.items():
        # Find the right eval function:
        eval_function_to_call = eval_functions[key]

        # Call the eval function and save to a column in the original df:
        eval_result = eval_function_to_call(row["generated_social_media_post"])

        # Save to column at index position,
        # this also converts the boolean to 1 for success and 0 for failure on the evaluation:
        social_post_df.loc[index, key] = convert_boolean_to_one_hot_encoding(
            eval_result
        )

print("--------------------")
print(social_post_df.head(5))
print("--------------------")
eval_columns = [col for col in social_post_df.columns if "eval" in col]
print(eval_columns)
print("--------------------")

eval_accuracy_results = {}

for col in eval_columns:
    # Get that eval column:
    single_eval_results = social_post_df[col]

    # Compare to the length and calculate the accuracy:
    single_eval_accuracy = single_eval_results.sum() / len(single_eval_results)

    # Save to the eval_accuracy_results dictionary:
    eval_accuracy_results[col] = single_eval_accuracy

print("--------------------")
print(eval_accuracy_results)
print("--------------------")

mean_evals_accuracy = np.mean(list(eval_accuracy_results.values()))
print(mean_evals_accuracy) # 61% accuracy
print("--------------------")

# Define weights for each evaluation metric
weights = {
    "eval_has_hashtag": 0.7,  # 70% weight
    "eval_length_of_social_post": 0.3,  # 30% weight
}

# Initialize a variable to store the weighted average
weighted_avg_accuracy = 0

# Calculate the weighted average accuracy
for eval_metric, accuracy in eval_accuracy_results.items():
    weighted_avg_accuracy += accuracy * weights[eval_metric]
print(f"The weighted average accuracy: {weighted_avg_accuracy:.2f}")
print("--------------------")
# Adding the true labels to the dataframe (based on whether the topic is coding or not):
true_labels = [1, 1, 1, 1, 1, 1, 0, 0, 0]
social_post_df["is_coding_true_labels"] = true_labels

from langchain_openai.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# 1. Define the model:
model = ChatOpenAI(
    model="gpt-3.5-turbo-1106",
    model_kwargs={"response_format": {"type": "json_object"}},
)

# 2. Define the prompt:
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Act as a content editor, you are responsible for classifying
            social media posts using the following format instructions.
            Format Instructions: {format_instructions}
              """,
        ),
        (
            "user",
            """Social media post text: {generated_social_media_post}
            The topic to be classified against is: {topic}
            """,
        ),
    ]
)


# 3. Define the pydantic model:
class SocialMediaPostClassifier(BaseModel):
    is_topic: int = Field(
        default=0,
        description="""This field is a classification result for
                           whether a result is identified against a known topic. 1 for yes and 0 for no.""",
    )


# 4. Define the output parser:
output_parser = PydanticOutputParser(pydantic_object=SocialMediaPostClassifier)

# 5. Create an LCEL chain:
chain = prompt | model | output_parser

# 6. Invoke the chain for the whole dataset:
results = []
TOPIC = "coding, software or data science"

# For each row, loop through:
for index, row in social_post_df.iterrows():
    result = chain.invoke(
        {
            "generated_social_media_post": row["generated_social_media_post"],
            "format_instructions": output_parser.get_format_instructions(),
            "topic": TOPIC
        }
    )
    # Extract the is_topic property from the Pydantic model:
    results.append(result.is_topic)

# Save the results to a new column:
social_post_df['eval_is_coding_topic'] = results

print(social_post_df.head(5))

# Loop through each row and calculate the accuracy against the true labels:
true_labels = social_post_df["is_coding_true_labels"]
eval_results = social_post_df["eval_is_coding_topic"]

# Loop through and check for equality in terms of 0 or 1 for each row, when it is equal, add 1 to the count:
count = 0
for index, row in social_post_df.iterrows():
    if row["is_coding_true_labels"] == row["eval_is_coding_topic"]:
        count += 1

single_eval_accuracy = count / len(true_labels)
print(f"GPT-3.5 Turbo achieved {round(single_eval_accuracy, 2) * 100} % accuracy against the true labels.")

# Define weights for each evaluation metric






