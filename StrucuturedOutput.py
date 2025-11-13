from dotenv import load_dotenv

load_dotenv()

from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
import json

from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS
from schemas import AgentResponse


tools = [TavilySearch()]
llm = ChatOpenAI(model="gpt-4")
react_prompt = hub.pull("hwchase17/react")


# This creates the overall agent, combining the tools, the instructions on how it should format and all.
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=react_prompt,
)

# Wraps the agent so it can loop: reason → call tool → reason again → produce final answer.
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Extracts just the "output" field from the agent's response dict.
extract_output = RunnableLambda(lambda x: x["output"])

# This method directly structure the output without using the output parser for the pydantic object and also saves token as this is a tool calling method
llm_parser = llm.with_structured_output(AgentResponse)

# Chaining the agent with the output extracter and then formatting it through parse_output
chain = agent_executor | extract_output | llm_parser



def main():
    result = chain.invoke(
        input={
            "input": "Tell me about the job openings in Linkedin for the roles of Junior Data Enginner.",
        }
    )
    print(result)

if __name__ == "__main__":
    main()
