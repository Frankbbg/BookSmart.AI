
import sys
sys.path.append("..")


from classes.models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import copy

# Let's add some stories to my user
engine = create_engine("sqlite:///../assets/PyProject.db")
Session = sessionmaker(bind=engine)
session = Session()

# Example 1
story1 = Story(
    storyTitle="The Mysterious Pendant",
    messages=[
        Message(text="In a distant land", isAISender=True),
        Message(text="Lived a young adventurer named Alex", isAISender=False),
        Message(text="One day, Alex found a pendant", isAISender=True),
        Message(text="Little did they know, the pendant held ancient powers", isAISender=False),
    ]
)

# Example 2
story2 = Story(
    storyTitle="A Journey Through Time",
    messages=[
        Message(text="In the year 3025", isAISender=True),
        Message(text="Time travel had become a reality", isAISender=False),
        Message(text="Scientists worked tirelessly to perfect the technology", isAISender=True),
        Message(text="But altering the past had consequences beyond imagination", isAISender=False),
    ]
)

# Example 3
story3 = Story(
    storyTitle="The Enchanted Forest",
    messages=[
        Message(text="Deep within the enchanted forest", isAISender=True),
        Message(text="Creatures of myth and magic thrived", isAISender=False),
        Message(text="A young mage named Elara discovered the secrets of the forest", isAISender=True),
        Message(text="But darkness lurked, threatening to consume the magic forever", isAISender=False),
    ]
)

story4 = Story(
    storyTitle="The rise of Cinderalla",
    messages = [
        Message(text="Once upon a time", isAISender=True),
        Message(text="And the king ruled", isAISender=False),
        Message(text="Of course the monarchy was red", isAISender=True),
    ]
)

story5 = Story(
    storyTitle="Sailor of the Cosmic Seas and the Vast Expanse of Aria: The One who is Free",
    messages = [
        Message(text="Endless Horizon!", isAISender=True),
    ]
)


story6 = Story(
    storyTitle="Clash of the Strongest: The Strength and Solitude of being at the Top",
    messages = [
        Message(text="The fight of the century!", isAISender=True),
    ]
)




retrievedStory = session.query(Story).filter_by(storyTitle="Cheffers").first()


currentMessages = []

if retrievedStory:
    currentMessages = retrievedStory.messages

for message in currentMessages:
    print(f"Before: {message.text}")
currentMessages = []



session.commit()

newStory = session.query(Story).filter_by(storyTitle="Cheffers").first()

if newStory:
    for message in newStory.messages:
        print(message.text)


session.close()