import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase app
cred = credentials.Certificate(r'C:\Users\gajen\Downloads\rag-chatbot-aaddf-firebase-adminsdk-ho2xt-382e716d23.json')
 # Use your Firebase credentials
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

def store_metadata_in_firebase(chat_name, index_name):
    try:
        print(f"Storing metadata for chat_name: {chat_name}, index_name: {index_name}")
        doc_ref = db.collection('chat_indexes').document(chat_name)
        doc_ref.set({
            'chat_name': chat_name,
            'index_name': index_name,
            'status': 'indexed'
        })
        print(f"Stored metadata for chat_name: {chat_name} in Firebase")
        return True
    except Exception as e:
        raise Exception(f"Error storing metadata in Firebase: {e}")\
        

def get_index_from_firebase(chat_name):
    try:
        doc_ref = db.collection('chat_indexes').document(chat_name)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict().get('index_name')
        else:
            return None
    except Exception as e:
        raise Exception(f"Error retrieving index from Firebase: {e}")

