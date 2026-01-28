import os
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def load_and_split_pdfs(pdf_dir_path: str) -> List[Document]:
    """
    Load all PDF files from a directory and split them into chunks.
    """
    if not os.path.isdir(pdf_dir_path):
        raise ValueError(f"Invalid directory path: {pdf_dir_path}")

    all_documents: List[Document] = []

    for file_name in os.listdir(pdf_dir_path):
        if file_name.lower().endswith(".pdf"):
            full_path = os.path.join(pdf_dir_path, file_name)
            loader = PyPDFLoader(full_path)
            documents = loader.load()
            all_documents.extend(documents)

    if not all_documents:
        raise RuntimeError("No PDF documents found in the given directory")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=150,
    )

    return splitter.split_documents(all_documents)


def run_demo():
    pdf_dir = "/home/bitcot/dataset"
    chunks = load_and_split_pdfs(pdf_dir)
    print(f"Loaded and split {len(chunks)} chunks")


if __name__ == "__main__":
    run_demo()