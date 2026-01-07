import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# Load .env variables
load_dotenv()


def run_demo():
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
        temperature=0.2,
    )

    prompt = PromptTemplate(
        input_variables=["topic"],
        template="Explain {topic} in simple terms for a beginner."
    )

    formatted_prompt = prompt.format(topic="REST APIs")

    response = llm.invoke(formatted_prompt)

    print("Prompt:")
    print(formatted_prompt)
    print("\nResponse:")
    print(response.content)


if __name__ == "__main__":
    run_demo()
