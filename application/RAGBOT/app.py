from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters.character import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

load_dotenv()

class LlamaChat:
    def __init__(self):
        self.working_dir = os.path.dirname(os.path.abspath(__file__))
    
    def load_document(self, file_path):
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            return documents
        except Exception as e:
            print(f"Error loading document: {e}")
            return None

    def setup_vectorstore(self, documents):
        try:
            embeddings = HuggingFaceEmbeddings()
            text_splitter = CharacterTextSplitter(
                separator='\n',
                chunk_size=1000,
                chunk_overlap=200
            )
            doc_chunks = text_splitter.split_documents(documents)
            vectorstore = FAISS.from_documents(doc_chunks, embeddings)
            return vectorstore
        except Exception as e:
            print(f"Error setting up vectorstore: {e}")
            return None

    def create_chain(self, vectorstore):
        try:
            llm = ChatGroq(
                model="llama-3.1-70b-versatile",
                temperature=0
            )
            retriever = vectorstore.as_retriever()
            memory = ConversationBufferMemory(
                llm=llm,
                output_key="answer",
                memory_key="chat_history",
                return_messages=True
            )
            chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=retriever,
                chain_type="map_reduce",
                memory=memory,
                verbose=True
            )
            return chain
        except Exception as e:
            print(f"Error creating chain: {e}")
            return None

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'fallback_secret_key')

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/uploadFile", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        session['file_path'] = file_path
        session['chat_history'] = []
        return jsonify({"success": True, "message": "File uploaded successfully", "filename": filename}), 200
    else:
        return jsonify({"success": False, "message": "File type not allowed"}), 400

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('question')
    file_path = session.get('file_path')

    if not user_input:
        return jsonify({"success": False, "message": "No user input provided"}), 400
    
    if not file_path:
        return jsonify({"success": False, "message": "No file uploaded"}), 400

    try:
        llama_chat = LlamaChat()
        documents = llama_chat.load_document(file_path)
        if documents is None:
            raise ValueError("Error loading document")

        vectorstore = llama_chat.setup_vectorstore(documents)
        if vectorstore is None:
            raise ValueError("Error setting up vectorstore")

        conversation_chain = llama_chat.create_chain(vectorstore)
        if conversation_chain is None:
            raise ValueError("Error creating conversation chain")

        response = conversation_chain({"question": user_input})
        assistant_response = response['answer']

        if 'chat_history' not in session:
            session['chat_history'] = []
        
        session['chat_history'].append({"role": "user", "content": user_input})
        session['chat_history'].append({"role": "assistant", "content": assistant_response})
        session.modified = True

        return jsonify({
            "success": True,
            "user_input": user_input,
            "assistant_response": assistant_response,
            "chat_history": session['chat_history']
        })
    except Exception as e:
        print(f"Error in chat: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=3000)