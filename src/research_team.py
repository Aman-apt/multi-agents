from typing import Literal
from langgraph.graph import StateGraph, START
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langgraph.types import Command

from .tools import scrape_webpages, tavily_tool
from .utils import State, make_supervisor_node


llm = ChatOllama(base_url="http://localhost:11434", model="gpt-oss:120b-cloud")

search_agent = create_agent(llm, tools=[tavily_tool])


def search_node(state: State) -> Command[Literal["supervisor"]]:
    result = search_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="search")
            ]
        },
        #we want our workers to alsways "report back" to the supervisor when done
        goto="supervisor"
    )
    
web_scraper_agent = create_agent(llm, tools=[scrape_webpages])

def web_scraper_node(state: State) -> Command[Literal["supervisor"]]:
    result = web_scraper_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="web_scraper")
            ]
        },
        # we want our workets to always reprot back to the supervisor when done
        goto="supervisor",
    )
    
research_supervisor_node = make_supervisor_node(llm, ["search", "web_scraper"])


# Let's build the graph and connect the Nodes 

research_builder = StateGraph(State)
research_builder.add_node("supervisor", research_supervisor_node)
research_builder.add_node("search", search_node)
research_builder.add_node("web_scraper", web_scraper_node)

research_builder.add_edge(START, "supervisor")
research_graph = research_builder.compile()


from IPython.display import Image, display

display(Image(research_graph.get_graph().draw_mermaid_png()))