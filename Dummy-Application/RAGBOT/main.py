import os

from dotenv import load_dotenv
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters.character import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


# load the environment variables
load_dotenv()

class LlamaChat:
    def __init__(self):
        self.working_dir = os.path.dirname(os.path.abspath(__file__))
        load_dotenv()
        self.document=self.load_document()
        self.vectoreStore=self.setup_vectorStore()
        self.chain = self.create_chain(self)
    def load_document(self,file_path):
        loader=None
        try:
            loader=PyPDFLoader(file_path)
        except Exception:
            print(Exception)

        documents=loader.load()
        return documents

    def setup_vectorstore(self,documents):
        try:
            embeddings=HuggingFaceEmbeddings()
            text_spiltter= CharacterTextSplitter(
                separator='/n',
                chunk_size=1000,
                chunk_overlap=200
            )
            doc_chunks=text_spiltter.split_documents(documents)
            vectorstore=FAISS.from_documents(doc_chunks,embeddings)
        except Exception:
            print(Exception)
        return vectorstore

    def create_chain(self,vectorstore):
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



""" 
st.set_page_config(
    page_title="Chat with Doc",
    page_icon="📄",
    layout="centered"
)

st.title("🦙 Chat with Doc - LLAMA 3.1")

# initialize the chat history in streamlit session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


uploaded_file = st.file_uploader(label="Upload your pdf file", type=["pdf"])

if uploaded_file:
    file_path = f"{working_dir}/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        print('its here')

    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = setup_vectorstore(load_document(file_path))
        print('its also here')

    if "conversation_chain" not in st.session_state:
        print("undobtebly here aswell")
        st.session_state.conversation_chain = create_chain(st.session_state.vectorstore)

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_input = st.chat_input("Ask Llama...")


if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)


    with st.chat_message("assistant"):
        response = st.session_state.conversation_chain({"question": user_input})
        assistant_response = response["answer"]
        st.markdown(assistant_response)
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
 """