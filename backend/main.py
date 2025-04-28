from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import os
import shutil

from langchain.document_loaders import TextLoader, PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.tools import tool
from dotenv import load_dotenv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # front end url
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs("vectorstore", exist_ok=True)
load_dotenv()
embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])

# --- Helper Functions ---


def save_vectorstore(docs):
    """Save a list of document chunks into a local FAISS vectorstore."""
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("vectorstore")


def get_vectorstore():
    """Load the FAISS vectorstore from the local directory."""
    return FAISS.load_local(
        "vectorstore", embeddings, allow_dangerous_deserialization=True
    )


def extract_text(file: UploadFile):
    """Save the uploaded file locally and extract its textual content.

    Supports `.txt` and `.pdf` file formats.

    Args:
        file (UploadFile): The uploaded file.

    Returns:
        List of Document objects containing the extracted text.

    Raises:
        ValueError: If the file type is unsupported.
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    if file.filename.endswith(".txt"):
        loader = TextLoader(file_path)
    elif file.filename.endswith(".pdf"):
        loader = PyMuPDFLoader(file_path)
    else:
        raise ValueError("Unsupported file type")

    return loader.load()


# --- Routes ---


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    """API endpoint to upload a document, split it into chunks, and save it into a vectorstore.

    Args:
        file (UploadFile): The file uploaded by the user.

    Returns:
        JSON message indicating the number of chunks stored.
    """
    print(f"Received file: {file.filename}")
    docs = extract_text(file)
    print(docs)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    save_vectorstore(chunks)
    return {"message": f"Stored {len(chunks)} chunks from {file.filename}"}


from math import sqrt
import math


@tool
def calculator_tool(expression: str) -> str:
    """Evaluate a simple mathematical expression using the math library.

    Args:
        expression (str): The mathematical expression to evaluate.

    Returns:
        str: The result of the evaluation, rounded to two decimal places.
            Returns an error message if evaluation fails.
    """
    try:
        # Allow all functions inside math
        result = eval(expression, {"__builtins__": {}}, vars(math))
        return str(round(result, 2))
    except Exception as e:
        return f"Error: {e}"


@app.post("/chat")
async def chat(query: str = Form(...)):
    """API endpoint to handle a chat query.

    It retrieves relevant context from the vectorstore, evaluates mathematical expressions
    if needed, and generates a final answer using an OpenAI agent.

    Args:
        query (str): The user's query submitted via a form field.

    Returns:
        JSON response containing the generated answer.
    """
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever()

    qa = RetrievalQA.from_chain_type(llm=OpenAI(temperature=0), retriever=retriever)

    tools = [
        Tool.from_function(
            func=calculator_tool,
            name="calculator_tool",
            description="Evaluates a simple mathematical expression and returns the result.",
        )
    ]
    agent = initialize_agent(
        tools=tools,
        llm=OpenAI(temperature=0),
        agent_type="zero-shot-react-description",
        verbose=True,
    )

    context_answer = qa.run(query)
    # prompt
    agent_input = f"Context: {context_answer}\n\nQuestion: {query}"
    result = agent.run(agent_input)

    return JSONResponse(content={"response": result})
