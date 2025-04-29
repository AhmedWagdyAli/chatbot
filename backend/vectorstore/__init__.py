import os
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])


def save_vectorstore(docs):
    """
    Save documents to a FAISS vectorstore.

    This function creates a FAISS vectorstore from the provided documents
    using OpenAI embeddings and saves it locally.

    Args:
        docs (List[Document]): A list of documents to be stored in the vectorstore.

    Returns:
        None
    """
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("vectorstore")


def get_vectorstore():
    """
    Load the FAISS vectorstore from the local storage.

    This function loads a previously saved FAISS vectorstore using OpenAI embeddings.

    Returns:
        FAISS: The loaded FAISS vectorstore instance.
    """
    return FAISS.load_local(
        "vectorstore", embeddings, allow_dangerous_deserialization=True
    )
