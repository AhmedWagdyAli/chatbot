import os
import shutil
from fastapi import UploadFile
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader

UPLOAD_DIR = "./uploads"


def extract_text(file: UploadFile):
    """
    Extract text content from an uploaded file.

    This function saves the uploaded file to the server, determines its type
    (e.g., `.txt` or `.pdf`), and extracts its text content using the appropriate
    loader. Only `.txt` and `.pdf` files are supported.

    Args:
        file (UploadFile): The uploaded file object from FastAPI.

    Returns:
        List[Document]: A list of `Document` objects containing the extracted text.

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
