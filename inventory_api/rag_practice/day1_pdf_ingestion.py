import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_pdf():
    pdf_path = os.getenv("RAG_PDF_PATH")

    if not pdf_path:
        raise RuntimeError("RAG_PDF_PATH environment variable is not set")

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    return documents

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=150
    )
    chunks = splitter.split_documents(documents)
    return chunks

def load_and_split_pdf():
    documents = load_pdf()
    chunks = split_documents(documents)
    return chunks

def run_demo():
    documents = load_pdf()
    print(f"Total pages loaded: {len(documents)}")

    chunks = split_documents(documents)
    print(f"Total text chunks created: {len(chunks)}")

    print("\nSample chunk content:\n")
    print(chunks[0].page_content[:500])





if __name__ == "__main__":
    run_demo()