from langchain.core.prompt import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are viral twitter influencer grading a tweet. Generate critique and recommendation for the user.",
        ),
        MessagesPlaceholder("messages"),
    ]
)

generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are viral twitter techie influence asssitant tasked with writing excellent tweets. Write a tweet that will go viral.
            If the user provides critique, respond with revised version of previous tweet.
            """,
        ),
        MessagesPlaceholder("messages"),
    ]
)

llm = ChatOpenAI()
generate_chain = generation_prompt | llm
reflection_chain = reflection_prompt | llm