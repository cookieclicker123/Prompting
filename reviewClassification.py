from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

import os 

os.environ ["OPENAI_API_KEY"] = "sk-Z5im5OFaiEVNIIpWUb8cT3BlbkFJ1mOwWKdhVbMdxxecqF8rf"

reviews = [
    {'review': 'This is a great movie. I will watch it again.'},
    {'review': 'I love this movie!'},
    {'review': 'I hate this movie.'},
    {'review': 'That was a waste of my time.'},
    {'review': 'I will never get that time back.'},
    {'review': 'This is a waste of money.'},
    {'review': 'I will never watch a movie by that director again.'},
     {'review': 'This is a great movie. I will watch it again.'},
    {'review': 'I love this movie!'},
    {'review': 'I hate this movie.'},
    {'review': 'That was a waste of my time.'},
    {'review': 'I will never get that time back.'},
    {'review': 'This is a waste of money.'},
    {'review': 'I will never watch a movie by that director again.'},
    {'review': 'Absolutely fantastic! A must-watch.'},
    {'review': 'The storyline was captivating from start to finish.'},
    {'review': 'The acting was subpar and the plot was predictable.'},
    {'review': 'I was on the edge of my seat the whole time.'},
    {'review': 'The cinematography was breathtaking.'},
    {'review': 'I wouldn\'t recommend this movie to anyone.'},
    {'review': 'A cinematic masterpiece!'},
    {'review': 'The characters lacked depth and the dialogue was cheesy.'},
    {'review': 'A rollercoaster of emotions. Loved every minute of it.'},
    {'review': 'I fell asleep halfway through.'},
    {'review': 'The hype around this movie was undeserved.'},
    {'review': 'A refreshing take on a classic story.'},
    {'review': 'The pacing was slow and it dragged on.'},
    {'review': 'A visual treat with a compelling narrative.'},
    {'review': 'I regret buying a ticket for this.'},
    {'review': 'The soundtrack was the only good thing about this movie.'},
    {'review': 'A forgettable experience.'},
    {'review': 'This movie left a lasting impression on me.'},
]

chat = ChatOpenAI()
classifications = []

for review in reviews:
    print('Classifiying review: ' + review['review'])
    # Classifiy each review individually:
    response = chat.invoke([SystemMessage(content='''You are responsible for classification of movie reviews. Please classify the following review as positive or negative. You must only use the following words:
                                   negative
                                   positive'''), HumanMessage(content=review['review'])])
    if response.content not in ['negative', 'positive']:
        # Throw an error:
        raise Exception('Invalid classification: ' + response.content)
    classifications.append(response.content)

print(classifications)

