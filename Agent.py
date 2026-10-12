import asyncio 
from picoagents import Agent
from picoagents.llm import OpenAIChatCompletionClient
import os
 
client = OpenAIChatCompletionClient(
    model="gpt-4.1-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)
 
poet = Agent(
    name="Agent",
    description="Haiku poet",
    instructions="You are Haiku Poet.",
    model_client=client
)

poetry=""
async def test_poet():
    global poetry
    response = await poet.run("Write a haiku about cherry blossoms in spring") #Call the agent implementation
    print(f"Poet says: {response}")
    poetry= response
asyncio.run(test_poet())
# asyncio.run_stream(test_poet())

critic = Agent(
    name="Agent",
    description="Critic ",
    instructions="Youre a critic analyzer who analyzes Haiku Poets to tell whether theyre nice or not",
    model_client=client
)

async def critic_funt():
    response = await critic.run(f"Provide feedback on this poet: ```{poetry}``` poet.")
    print(f"The critic response is: {response}")

asyncio.run(critic_funt())

