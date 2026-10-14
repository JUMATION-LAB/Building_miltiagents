import asyncio 
from picoagents import Agent
from picoagents.llm import OpenAIChatCompletionClient
from picoagents.orchestration import RoundRobinOrchestrator
from picoagents.termination import MaxMessageTermination , TextMentionTermination 
from picoagents.webui import serve

import os
 
client = OpenAIChatCompletionClient(
    model="gpt-4.1-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)
 
poet = Agent(
    name="Poet Agent",
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
# asyncio.run(test_poet())
# asyncio.run_stream(test_poet())

critic = Agent(
    name="Critic Agent",
    description="Critic",
    instructions="You are a haiku critic. \
When you see a haiku, provide 2-3 specific, actionable \
suggestions for improvement. . Be constructive and brief. \
If satisfied with the haiku, respond with 'APPROVED'",
    model_client=client
)

# async def critic_funt():
#     response = await critic.run(f"Provide feedback on this poet: ```{poetry}``` poet.")
#     print(f"The critic response is: {response}")

# asyncio.run(critic_funt())

"Creating the terminator."
termination = ( MaxMessageTermination(max_messages=8000) | TextMentionTermination(text="APPROVED") )

"Create the orchestrator"
orchestrator = RoundRobinOrchestrator(
    agents=[poet, critic],
    termination=termination,
    max_iterations = 10
)

# Running the two Agents
async def run_orchestration():
    task= "Write a haiku about an African single mom"
    stream= orchestrator.run_stream(task)
    async for message in stream:
        print(f"{message}")

# asyncio.run(run_orchestration())

# Use the orchestrator we created above
serve(entities=[orchestrator], port=8070, auto_open=True)
