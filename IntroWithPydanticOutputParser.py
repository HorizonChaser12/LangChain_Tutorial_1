from dotenv import load_dotenv

load_dotenv()

from langchain import hub
from langchain.agents import AgentExecutor
from langchain_core.output_parsers.pydantic import PydanticOutputParser
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
# Creates a parser that will validate/format the LLM's final output into your AgentResponse Pydantic model (with answer and sources fields).
output_parser = PydanticOutputParser(pydantic_object=AgentResponse)

# They extract everything between those curly brackets and they implicitly add them as input variables.
# So this is why the missing tools input variable, which is missing here, is still going to be populated
react_prompt_with_format_instructions = PromptTemplate(template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
input_variables=["input","agent_scratchpad", "tools_name"]
).partial(format_instructions = output_parser.get_format_instructions())

# This creates the overall agent, combining the tools, the instructions on how it should format and all.
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=react_prompt_with_format_instructions,
)

# Wraps the agent so it can loop: reason → call tool → reason again → produce final answer.
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Extracts just the "output" field from the agent's response dict.
extract_output = RunnableLambda(lambda x: x["output"])

# Takes the extracted string and parses it into your AgentResponse Pydantic model.
parse_output = RunnableLambda(lambda x: output_parser.parse(str(x)))

# Chaining the agent with the output extracter and then formatting it through parse_output
chain = agent_executor | extract_output | parse_output

# Flow when you call chain.invoke(...):
# Agent searches → LLM formats answer per schema → extract text → validate & convert to Pydantic model → return.


def main():
    result = chain.invoke(
        input={
            "input": "Can you find me what a beginner has to do to learn more about Data Engineering?",
        }
    )
    print(result)
    # print(output_parser.get_format_instructions())
    # Output:
    # As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]} the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.
    # Here is the output schema:
    # ```
    # {"$defs": {"Source": {"description": "Schema for a source used by the agent", "properties": {"url": {"description": "The URL of the source", "title": "Url", "type": "string"}}, "required": ["url"], "title": "Source", "type": "object"}}, "description": "Schema for agent response with answer and sources", "properties": {"answer": {"description": "The agent's answer to the query", "title": "Answer", "type": "string"}, "sources": {"description": "List of sources used to generate the answer", "items": {"$ref": "#/$defs/Source"}, "title": "Sources", "type": "array"}}, "required": ["answer"]}
    # ```

if __name__ == "__main__":
    main()
