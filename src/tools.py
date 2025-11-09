import io, contextlib
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Annotated, List, Dict, Optional, TypedDict
from langchain_community.document_loaders import WebBaseLoader
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL


_TEMP_DIRECTORY = TemporaryDirectory()
WORKING_DIRECTORY = Path(_TEMP_DIRECTORY.name)

### RESEARCH AGENTS TEAM TOOLS ###

tavily_tool = TavilySearch(max_results=5)

@tool
def scrape_webpages(urls: List[str]) -> str:
    """User request and bs4 to scrape the provided web pages for detailed information."""
    loader = WebBaseLoader()
    docs = loader.load()
    return "\n\n".join(
        [
            f'<Document name="{doc.metadata.get("title", "")}">\n{doc.page_content}\n</Document>'
            for doc in docs
        ]
    )
    


### DOCUMENT WRITING TEAM TOOLS ###

@tool
def create_outline(
    points: Annotated[List[str], "List of main points or sections"],
    file_name: Annotated[str, "File path to save the outline"],
) -> Annotated[str, "Path of the saved outline file"]:
    """Create and save outline"""
    with (WORKING_DIRECTORY/ file_name).open("w") as file:
        for i, point in enumerate(points):
            file.write(f"{i + 1}. {point}")
    return f"Outline saved to {file_name}"


@tool
def read_documents(
    file_name: Annotated[str, "File path to read the documents froms"],
    start: Annotated[Optional[int], "The start line. Default is 0"] = None,
    end: Annotated[Optional[int], "The end line. Default i None"] = None,
) -> str:
    """Read the given documents"""
    with(WORKING_DIRECTORY/ file_name).open('r') as file:
        lines = file.readlines()
    if start is None:
        start = 0
    return "\n".join(lines[start:end])

@tool
def write_documents(
    file_name: Annotated[str, "File path to write the documents"],
    content: Annotated[str, "Text content to be written into documnets"],
) -> Annotated[str, "Path of saved documents"]:
    """Write the content in to the given file"""
    with (WORKING_DIRECTORY/ file_name).open("w") as file:
        file.write(content)
    return f"Documents saved to {file_name}"


@tool
def edit_document(
    file_name: Annotated[str, "Path of the document to be edited ."],
    inserts: Annotated[
        Dict[int, str],
        "Dictonary where key is the line number (1-indexed) and values is the text to be inserted at that line"
    ],
):
    """Edit the document by inserting text at specific line numbers"""
    
    with (WORKING_DIRECTORY/file_name).open("r") as file:
        lines = file.readlines()
    
    sorted_inserts = sorted(inserts.items())
    
    for line_number, text in sorted_inserts:
        if 1 <= line_number <= len(lines) + 1:
            lines.insert(line_number - 1, text + "\n")
        else:
            return f"Error: Line number{line_number} is out of range."

    with (WORKING_DIRECTORY/file_name).open('w') as file:
        file.writelines(lines)
    return f"Document edited and saved to {file_name}"


repl = PythonREPL()

@tool
def python_repl_tool(code: str) -> str:
    """Execute Python code and return the output."""
    stdout = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout):
            exec(code, {})
        result = stdout.getvalue()
    except Exception as e:
        result = f"Error: {e}"
    return f"Output:\n{result or '(no output)'}"