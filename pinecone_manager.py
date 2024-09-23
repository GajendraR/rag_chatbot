import os
from pinecone import Pinecone, ServerlessSpec
import re
import numpy as np

# Initialize Pinecone
pc = Pinecone(api_key="2154d54e-5bb6-470d-9fac-761efd8f0882")

def create_pinecone_index(chat_name, embeddings, chunks):
    try:
        print("Step 1: Function called")  
        if not embeddings or len(embeddings) == 0:
            print("Embeddings are empty or None")
            return "problem_getting_index_name"

        # pinecone name rules
        sanitized_chat_name = re.sub(r'[^a-z0-9-]', '-', chat_name.lower())  
        index_name = f"index-{sanitized_chat_name[:50]}"
        print(f"Step 2: Index name generated as {index_name}") 

        # Fetch the existing indexes
        existing_indexes = pc.list_indexes() 
        print(f"Step 3: Existing indexes: {existing_indexes}")

        if index_name not in existing_indexes:
            print(f"Step 3.1: Index {index_name} does not exist, creating a new one")
            try:
                # Create a new index
                pc.create_index(
                    name=index_name,
                    dimension=len(embeddings[0]), 
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
                    )
                )
                print(f"Step 3.2: Index {index_name} created successfully")
            except Exception as index_create_error:
                print(f"Error creating index: {str(index_create_error)}")
                return "problem_getting_index_name"
        else:
            print(f"Step 3.3: Index {index_name} already exists, skipping creation")

        # Connect to index
        index = pc.Index(index_name)
        print(f"Step 4: Connected to index {index_name}")

        vectors = [
            {
                "id": f"{chat_name}_{i}",
                "values": embedding if isinstance(embedding, list) else embedding.tolist(),
                "metadata": {"text": chunk}  # Attach the chunk as metadata
            }
            for i, (embedding, chunk) in enumerate(zip(embeddings, chunks))
        ]
        print(f"Step 5: Prepared {len(vectors)} vectors for upsert")

        try:
            upsert_response = index.upsert(vectors)
            print(f"Step 6: Upsert response: {upsert_response}")
        except Exception as upsert_error:
            print(f"Error upserting vectors: {str(upsert_error)}")
            return "problem_getting_index_name"

        # print(f"Successfully indexed document under chat_name: {chat_name}")
        return str(index_name)

    except Exception as e:
        # print(f"Error at step: {str(e)}")
        return "problem_getting_index_name"
    
def query_pinecone(index_name, query_vector, top_k=5):
    try:
        # Fetch the index
        index = pc.Index(index_name)
        print(f"Querying index: {index_name}")

        # Perform the query using keyword arguments
        query_result = index.query(
            vector=query_vector,  
            top_k=top_k,          
            include_metadata=True 
        )

        print(f"Query result: {query_result}")
        return query_result
    except Exception as e:
        print(f"Error querying Pinecone: {str(e)}")
        raise Exception(f"Error querying Pinecone: {str(e)}")
