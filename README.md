# Document Processing and Query API with Pinecone and Google Gemini

This project is a Flask-based web application that allows users to upload PDF documents, process and index the text using Pinecone, and then query the indexed content using Google Gemini's language model. The project also integrates Firebase for metadata storage and document management.

### Demo
[Demo Link](https://github.com/user-attachments/assets/5d1b1b45-f8fc-4f2d-b826-22bca2044b0d)

## Features
- **Upload PDF**: Extract text from PDF files, chunk the text, and create vector embeddings using Sentence Transformers.
- **Indexing with Pinecone**: Store document chunks and their embeddings in Pinecone for efficient retrieval.
- **Query Documents**: Query the indexed content using Pinecone and generate responses using Google Gemini's generative AI model.
- **Firebase Integration**: Store and retrieve document metadata for managing multiple document uploads.

## Technologies Used
- **Flask**: Python web framework for creating the API.
- **PyPDF2**: Library for extracting text from PDF documents.
- **Pinecone**: Vector database for storing and querying embeddings.
- **Google Gemini**: Generative AI model used for answering questions based on document content.
- **Firebase**: Used for storing document metadata.
- **Sentence Transformers**: For embedding text chunks into vectors.
- **LangChain**: Framework for chaining models and building generative AI pipelines.

## Getting Started

### Prerequisites
- Python 3.8+
- [Pinecone API Key](https://www.pinecone.io/)
- [Google Gemini API Key](https://developers.generativeai.google/)
- Firebase account for metadata storage

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/document-query-api.git
    cd document-query-api
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment variables:
    - Create a `.env` file or export environment variables in your terminal.
    ```bash
    export GEMINI_API_KEY=your_gemini_api_key
    export PINECONE_API_KEY=your_pinecone_api_key
    ```

### Running the Application

1. Start the Flask app:
    ```bash
    python app.py
    ```

2. The API will be available at `http://127.0.0.1:5000/`.

## API Endpoints

### 1. Upload Document (`/upload`)
- **Method**: `POST`
- **Description**: Upload a PDF document, process it, and store it in Pinecone.
- **Parameters**:
    - `title`: The name of the document.
    - `doc`: The PDF file to be uploaded.

### 2. Query Document (`/query`)
- **Method**: `POST`
- **Description**: Query a document using Pinecone and Google Gemini.
- **Parameters**:
    - `chat_name`: The title of the uploaded document.
    - `question`: The query question.

## Example Usage

### 1. Upload a PDF document:
```bash
curl -X POST http://127.0.0.1:5000/upload \
-F "title=MyDocument" \
-F "doc=@/path/to/your/file.pdf"
```
###2. Query the uploaded document:
```bash
Copy code
curl -X POST http://127.0.0.1:5000/query \
-F "chat_name=MyDocument" \
-F "question=What is the summary of this document?"
```
### Environment Variables
GEMINI_API_KEY: Your Google Gemini API key.
PINECONE_API_KEY: Your Pinecone API key.
