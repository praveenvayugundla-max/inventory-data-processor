import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate


def get_llm():
    """
    Creates and returns ChatOpenAI instance.
    """
    return ChatOpenAI(
        model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
        temperature=0.2,
        api_key=os.getenv("OPENAI_API_KEY"),
    )


def build_prompt():
    """
    Prompt template used for all queries.
    """
    return PromptTemplate(
        input_variables=["query","title"],
        template=(
            "You are a helpful backend assistant.\n"
            "Answer the following question clearly and concisely:\n\n"
            "Question: {query},\n"
            "Title: {title}\n\n"
            "Answer:"
        ),
    )


def run_llm(query: str, title: str) -> dict:
    """
    Runs the LLM with formatted prompt and returns response + usage.
    """
    llm = get_llm()
    prompt = build_prompt()

    formatted_prompt = prompt.format(query=query,title=title)
    response = llm.invoke(formatted_prompt)

    return {
        "text": response.content,
        "usage": response.response_metadata.get("token_usage", {})
    }
