# Chatbot Application

This project is a **chatbot application** that allows users to upload documents, ask questions, and receive AI-generated responses based on the uploaded content. The chatbot is powered by **FastAPI** on the backend and **React** on the frontend, leveraging **LangChain** and **OpenAI** for document retrieval and reasoning.

---

## Features

1. **File Upload**:

   - Users can upload `.txt` or `.pdf` files.
   - The backend processes the files, extracts text, and stores it in a vectorstore for efficient retrieval.

2. **Chat Functionality**:
   - Users can ask questions related to the uploaded documents.
   - The chatbot retrieves relevant document chunks and generates context-based answers.
   - Includes a calculator tool for evaluating mathematical expressions.
   - It Keeps previous chat history but in json file and retireved by session_id.. this would be enhanced in real life situation and transferred to a database and reterieved by chat_session_id and User_id.

---

## Tech Stack

### Backend:

- **FastAPI**: REST API framework.
- **LangChain**: For document loading, splitting, embeddings, and QA chains.
- **FAISS**: Vector-based document retrieval.
- **OpenAI**: For LLM-based reasoning and answering.

### Frontend:

- **React**: For building the user interface.

---

## Prerequisites

1. **Python**: Ensure Python 3.8+ is installed.
2. **Node.js**: Ensure Node.js and npm are installed.
3. **Virtual Environment**: The `venv` folder is included in the repository.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/AhmedWagdyAli/chatbot.git
```

### 2. create & activate the virtual enviornment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. install requirements

```bash
cd backend
pip install -r requirements.txt
```

### 4. Create a .env file in the backend directory and add your OpenAI API key:

```bash
touch .env
```

```bash
OPENAI_API_KEY=your_openai_api_key
```

### 5.run the backend

```bash
uvicorn main:app --reload --port 8000
```

### 6.start the front end

```bash
cd ../frontend/my-app
npm install
npm start
```

### 7. if the browser don't open, navigate to.

```bash
http://localhost:3000
```
