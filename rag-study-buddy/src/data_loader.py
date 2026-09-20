"""
Step 2: Data Loader + Chunking

This file has two jobs:
1. load_all_documents()  -> reads every PDF in data/docs/ and turns each
   page into a LangChain Document object (text + info about where it came from).
2. chunk_documents()     -> splits those documents into smaller overlapping
   pieces ("chunks") so they are a good size to search over later.
"""

from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_all_documents(data_dir: str = "data/docs") -> list:
    documents = []
    data_path = Path(data_dir)
    pdf_files = list(data_path.glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF file(s) in {data_dir}")
    for pdf_file in pdf_files:
        print(f"  Loading: {pdf_file.name}")
        loader = PyMuPDFLoader(str(pdf_file))
        docs = loader.load()
        for doc in docs:
            doc.metadata["source_file"] = pdf_file.name
        documents.extend(docs)
    print(f"Loaded {len(documents)} total page(s) across all PDFs")
    return documents


def chunk_documents(documents: list, chunk_size: int = 1000, chunk_overlap: int = 200) -> list:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} document(s) into {len(chunks)} chunk(s)")
    return chunks


if __name__ == "__main__":
    docs = load_all_documents()
    chunks = chunk_documents(docs)
    print("\n--- Preview of chunk #1 ---")
    if chunks:
        print(chunks[0].page_content[:300])
        print("\nMetadata:", chunks[0].metadata)
    else:
        print("No chunks found - check that your PDF is in data/docs/")
