# from flask import Flask, request, jsonify
# from PyPDF2 import PdfReader
# from pinecone_manager import create_pinecone_index, query_pinecone
# from firebase_manager import store_metadata_in_firebase, get_index_from_firebase
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from sentence_transformers import SentenceTransformer
# import os
# import google.generativeai as genai
# import requests
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import PromptTemplate
# from langchain.chains.question_answering import load_qa_chain
# from langchain.schema import Document


# app = Flask(__name__)
# #transformer
# model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# # Google Gemini settings
# GEMINI_API_KEY = "AIzaSyD4ry3f0t7swJKMDaDeuFdy0jZbB3Gsf-Y"  # Replace with your actual Google Gemini API key
# GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyD4ry3f0t7swJKMDaDeuFdy0jZbB3Gsf-Y"
# genai.configure(api_key=GEMINI_API_KEY)

# # Initialize the Google Generative AI model with the API key
# model1 = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, google_api_key=GEMINI_API_KEY)

# #prompt
# prompt_template = """
# Use the following context to answer the question:

# Context: {context}

# Question: {question}

# Provide a clear, concise answer.
# """
# prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

# # Load the QA chain using the model1 and prompt
# chain = load_qa_chain(model1, chain_type="stuff", prompt=prompt)

# def validate_question(question):
#     # Implement your validation logic here
#     if not question or len(question.strip()) == 0:
#         return False, "Question cannot be empty."
#     if len(question) > 500:
#         return False, "Question is too long. Please keep it under 500 characters."
#     # Add more validation rules as needed
#     return True, "Valid question."

# # Function to embed text chunks using SentenceTransformer
# def vectorize_chunk(chunk):
#     return model.encode(chunk).tolist()

# # Function to extract text from a PDF file
# def extract_text_from_pdf(file):
#     reader = PdfReader(file)
#     text = ''
#     for page in reader.pages:
#         text += page.extract_text()  # Extract text from each page
#     return text

# # Chunking text using RecursiveCharacterTextSplitter
# def chunk_data(text, chunk_size=800, chunk_overlap=50):
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
#     return text_splitter.split_text(text)

# # Function to call Google Gemini (GenAI) for generating a response
# def generate_gemini_response(relevant_chunks, question):
#     # Combine the relevant chunks for context
#     input_text = [Document(page_content=chunk) for chunk in relevant_chunks]
    
#     try:    
#         # Generate the response using LangChain's QA chain
#         response = chain({"input_documents": input_text, "question": question}, return_only_outputs=True)
#         return response
#     except Exception as e:
#         return f"Error during LangChain Google Gemini API call: {str(e)}"

# # Function to retrieve answers from Pinecone and generate response using Google Gemini
# def retrieve_answers(query, index_name):
#     # Encode 
#     query_vector = model.encode(query).tolist()

#     # Query Pinecone 
#     query_result = query_pinecone(index_name, query_vector=query_vector)
    
#     # Extract relevant chunks 
#     relevant_chunks = [match['metadata']['text'] for match in query_result['matches'] if 'metadata' in match and 'text' in match['metadata']]

#     # Generate response 
#     gemini_response = generate_gemini_response(relevant_chunks, query)

#     return gemini_response, relevant_chunks

# # Upload route to process PDF and store chunks in Pinecone

# @app.route('/upload', methods=['POST'])
# def upload():
#     try:
#         title = request.form.get('title')
#         uploaded_file = request.files.get('doc')

#         if not title or not uploaded_file:
#             return jsonify({"error": "Please provide both title and document"}), 400

#         # Extract text from the uploaded PDF
#         text = extract_text_from_pdf(uploaded_file)

#         # Chunk the extracted text
#         chunks = chunk_data(text, chunk_size=800, chunk_overlap=50)

#         # Get embeddings for each chunk using SentenceTransformer
#         vectorized_chunks = [vectorize_chunk(chunk) for chunk in chunks]

#         # Create index in Pinecone and upload vectors
#         index_name = create_pinecone_index(title, vectorized_chunks, chunks)

#         # Store metadata in Firebase
#         success = store_metadata_in_firebase(title, index_name)

#         if success:
#             return jsonify({
#                 "message": "Document successfully processed and indexed",
#                 "title": title,
#                 "chunks": len(chunks),
#                 "vectors": vectorized_chunks
#             }), 200
#         else:
#             return jsonify({"error": "Error uploading vectors to Pinecone"}), 500

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Query route to retrieve answers from Pinecone based on a question
# @app.route('/query', methods=['POST'])
# def query():
#     try:
#         chat_name = request.form.get('chat_name')
#         question = request.form.get('question')

#         if not chat_name or not question:
#             return jsonify({"error": "Please provide both chat_name and question"}), 400

#         # Retrieve index_name from Firebase
#         index_name = get_index_from_firebase(chat_name)

#         if not index_name:
#             return jsonify({"error": f"Index not found for chat_name: {chat_name}"}), 404
        
#         is_valid, validation_message = validate_question(question)
#         if not is_valid:
#             return jsonify({"error": validation_message}), 400

#         # Retrieve answers using Pinecone and Google Gemini
#         response, relevant_chunks = retrieve_answers(question, index_name)

#         return jsonify({
#             "message": "Query successful",
#             "question": question,
#             "response": response,
#             "relevant_chunks": relevant_chunks
#         }), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify, render_template
from PyPDF2 import PdfReader
from pinecone_manager import create_pinecone_index, query_pinecone
from firebase_manager import store_metadata_in_firebase, get_index_from_firebase
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.schema import Document

app = Flask(__name__)
# transformer
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Google Gemini settings
GEMINI_API_KEY = "AIzaSyD4ry3f0t7swJKMDaDeuFdy0jZbB3Gsf-Y"  # Replace with your actual Google Gemini API key
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Google Generative AI model with the API key
model1 = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, google_api_key=GEMINI_API_KEY)

# prompt
prompt_template = """
Use the following context to answer the question:

Context: {context}

Question: {question}

Provide a clear, concise answer.
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

# Load the QA chain using the model1 and prompt
chain = load_qa_chain(model1, chain_type="stuff", prompt=prompt)


# Function to embed text chunks using SentenceTransformer
def vectorize_chunk(chunk):
    return model.encode(chunk).tolist()

# Function to extract text from a PDF file
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()  # Extract text from each page
    return text

# Chunking text using RecursiveCharacterTextSplitter
def chunk_data(text, chunk_size=800, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_text(text)

# Function to call Google Gemini (GenAI) for generating a response
def generate_gemini_response(relevant_chunks, question):
    # Combine the relevant chunks for context
    input_text = [Document(page_content=chunk) for chunk in relevant_chunks]
    
    try:    
        # Generate the response using LangChain's QA chain
        response = chain({"input_documents": input_text, "question": question}, return_only_outputs=True)
        return response
    except Exception as e:
        return f"Error during LangChain Google Gemini API call: {str(e)}"

# Function to retrieve answers from Pinecone and generate response using Google Gemini
def retrieve_answers(query, index_name):
    # Encode 
    query_vector = model.encode(query).tolist()

    # Query Pinecone 
    query_result = query_pinecone(index_name, query_vector=query_vector)
    
    # Extract relevant chunks 
    relevant_chunks = [match['metadata']['text'] for match in query_result['matches'] if 'metadata' in match and 'text' in match['metadata']]

    # Generate response 
    gemini_response = generate_gemini_response(relevant_chunks, query)

    return gemini_response, relevant_chunks

# Upload route to process PDF and store chunks in Pinecone

@app.route('/upload', methods=['POST'])
def upload():
    try:
        title = request.form.get('title')
        uploaded_file = request.files.get('doc')

        if not title or not uploaded_file:
            return jsonify({"error": "Please provide both title and document"}), 400

        # Extract text from the uploaded PDF
        text = extract_text_from_pdf(uploaded_file)

        # Chunk the extracted text
        chunks = chunk_data(text, chunk_size=800, chunk_overlap=50)

        # Get embeddings for each chunk using SentenceTransformer
        vectorized_chunks = [vectorize_chunk(chunk) for chunk in chunks]

        # Create index in Pinecone and upload vectors
        index_name = create_pinecone_index(title, vectorized_chunks, chunks)

        # Store metadata in Firebase
        success = store_metadata_in_firebase(title, index_name)

        if success:
            return jsonify({"message": "Document uploaded and processed successfully"}), 200
        else:
            return jsonify({"error": "Failed to store metadata in Firebase"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Query route to answer questions using Pinecone and Google Gemini
@app.route('/query', methods=['POST'])
def query():
    try:
        chat_name = request.form.get('chat_name')
        question = request.form.get('question')

        if not chat_name or not question:
            return jsonify({"error": "Please provide both chat name and question"}), 400

        # Get Pinecone index from Firebase metadata
        index_name = get_index_from_firebase(chat_name)

        if not index_name:
            return jsonify({"error": "Index not found for the given chat name"}), 404

        # Retrieve answers and generate response using Google Gemini
        gemini_response, relevant_chunks = retrieve_answers(question, index_name)

        return jsonify({"response": gemini_response, "relevant_chunks": relevant_chunks}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to render the frontend
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
