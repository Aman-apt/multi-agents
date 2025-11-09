from typing import Literal, List, TypedDict
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langgraph.types import Command
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START

from .tools import write_document, read_document, edit_document, create_outline, python_repl_tool
from .utils import State, make_supervisor_node


llm = ChatOllama(base_url="http://localhost:11434", model="gpt-oss:120b-cloud")

doc_writer_agent = create_agent(
    llm, 
    tools=[write_document, edit_document, read_document],
    system_prompt=(
        "You can read, write and edit documnets based on the note-taker's outlines ."
        "Don't ask follow-up questions"
    ),
)

def doc_writting_node(state: State) -> Command[Literal["supervisor"]]:
    result = doc_writer_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="doc_writer")
            ]
        },
        # we want our node to always respond back to the "supervisor"
        goto="supervisor"
    )
    

note_taking_agent = create_agent(
    llm,
    tools=[create_outline, read_document],
    system_prompt=(
        "You can read documents and create outlines for the document writer ."
        "Don't ask the follow-up questions."
    ),
)


def note_taking_node(state: State) -> Command[Literal["supervisor"]]:
    result = note_taking_agent.invoke(state)
    return Command(
        update={
            "messages":[
                HumanMessage(content=result["messages"][-1].content, name="note_taker")
            ]
        },
        # Always respond back to the supervisor
        goto="supervisor"
    )
    
chart_generating_agent = create_agent(
    llm, tools=[read_document, python_repl_tool]
)


def chart_generating_node(state: State) -> Command[Literal["supervisor"]]:
    result = chart_generating_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=result["messages"][-1].content, name="chart_generator"
                )
            ]
        },
        # We want our workers to ALWAYS "report back" to the supervisor when done
        goto="supervisor",
    )

doc_writing_supervisor_node = make_supervisor_node(
    llm, ["doc_writer", "note_taker", "chart_generator"]
)


paper_writing_builder = StateGraph(State)
paper_writing_builder.add_node("supervisor", doc_writing_supervisor_node)
paper_writing_builder.add_node("doc_writer", doc_writting_node)
paper_writing_builder.add_node("note_taker", note_taking_node)
paper_writing_builder.add_node("chart_generator", chart_generating_node)

paper_writing_builder.add_edge(START, "supervisor")
paper_writing_graph = paper_writing_builder.compile()

from IPython.display import Image, display
display(Image(paper_writing_graph.get_graph().draw_mermaid_png()))


for s in paper_writing_graph.stream(
    {
        "messages":[
            (
                "user",
                "write an outline for poem about cats and then write poem to disk."
            )
        ]
    },
    {"recursion_limit": 100},
):
    print(s)
    print("-------")