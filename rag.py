from uuid import uuid4

from dotenv import load_dotenv

from pathlib import Path
from langchain_classic.chains import RetrievalQAWithSourcesChain
from langchain_community.document_loaders import UnstructuredURLLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
# from langchain_ollama import ollama
# HuggingFaceEmbeddings is provided by langchain in recent versions
from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()





CHUNKS_SIZE=1000
EMBEDDING_MODEL="thenlper/gte-base"
VECTORESTORE_DIR=Path(__file__).parent / "resources/vectorestore"
COLLECTION_NAME="real_state_collection"
llm=None
vectore_store=None
def initialize_components():
    global llm,vectore_store
    if llm is None :
        llm=ChatGroq(model="llama-3.3-70b-versatile",temperature=0.9,max_tokens=500)

    ef=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL,
      model_kwargs={"trust_remote_code": True},encode_kwargs={"normalize_embeddings": True}  ) # sometimes the model is not from standard library in order to execute the code we need to set trust_remote_code to True
    vectore_store=Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=ef,
        persist_directory=str(VECTORESTORE_DIR)

    )


def process_urls(urls):
    """
    This function scraps data from a url and stores it in vector db
    :param url: input urls
    :return:
    """
    yield "Initializing components..."
    initialize_components()


    vectore_store.reset_collection()
    yield "Loading data from URLs..."
    loader=UnstructuredURLLoader(urls=urls)
    data=loader.load()

    yield "Splitting data into chunks..."
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", " "],       
        chunk_size=CHUNKS_SIZE
    )
    yield "Adding documents to vector store..."
    docs=text_splitter.split_documents(data)
    vectore_store.add_documents(docs,ids=[str(uuid4()) for _ in range(len(docs))])

    yield "Done adding documents to vector store."

def generate_amswer(query):
    if not vectore_store:
        raise RuntimeError("Vector store is not initialized. Please run process_urls first.")
    chain=RetrievalQAWithSourcesChain.from_llm(
        llm=llm,
        retriever=vectore_store.as_retriever()
    )
    result=chain.invoke({"question":query},return_only_outputs=True)
    sources=result.get("sources","")

    return result['answer'], sources






if __name__ =="__main__":
    urls=[
       "https://www.cnbc.com/2026/01/27/fed-preview-january-2026.html"
    ]


    process_urls(urls)
    answer, sources=generate_amswer("When did the U.S. Federal holds a press conference?")
    print(f"Answer:{answer}")
    print(f"Sources:{sources}")