from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from langchain.chains import RetrievalQA
from langchain.agents import initialize_agent, Tool
from langchain_community.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter

from dotenv import load_dotenv
import os

from vectorstore import save_vectorstore, get_vectorstore
from utils.file_processing import extract_text
from utils.math_tool import calculator_tool
from reasoning.callbacks import ReasoningCallbackHandler
from reasoning.clean import remove_ansi_escape_codes, clean_reasoning
from utils.chat_history import save_chat, get_chat_history

# --- Setup ---
load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # adjust for your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs("vectorstore", exist_ok=True)


# --- Routes ---


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    """Upload document and store its content in a vectorstore."""
    print(f"Received file: {file.filename}")
    docs = extract_text(file)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    save_vectorstore(chunks)
    return {"message": f"Stored {len(chunks)} chunks from {file.filename}"}


@app.post("/chat")
async def chat(query: str = Form(...), session_id: str = Form(...)):
    """Chat endpoint that queries vectorstore context + uses calculator tool."""
    session_id = session_id or "default_session"
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
    agent_input = f"Context: {context_answer}\n\nQuestion: {query}"

    callback_handler = ReasoningCallbackHandler()
    result = agent.run(agent_input, callbacks=[callback_handler])
    save_chat(session_id, "user", query)
    save_chat(session_id, "assistant", result)
    raw_reasoning = remove_ansi_escape_codes(
        "\n".join(callback_handler.reasoning_steps)
    )
    final_reasoning = clean_reasoning(raw_reasoning)

    return JSONResponse(
        content={
            "response": result,
            "reasoning": final_reasoning,
            "history": get_chat_history(session_id),
        }
    )
