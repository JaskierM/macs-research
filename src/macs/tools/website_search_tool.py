from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.tools import Tool

MAX_CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def search_website_and_answer(question: str, url: str, llm, embeddings_model) -> str:
    try:
        loader = WebBaseLoader(url)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=MAX_CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
        )
        chunks = splitter.split_documents(documents)

        vectorstore = FAISS.from_documents(chunks, embedding=embeddings_model)
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm, retriever=vectorstore.as_retriever(), chain_type="map_reduce"
        )
        result = qa_chain.invoke({"query": question})
        return result["result"].strip()
    except Exception as e:
        return f"Error: {e}"


def get_website_search_tool(llm, embeddings_model) -> Tool:
    return Tool(
        name="WebsiteSearchTool",
        func=lambda input: search_website_and_answer(
            input["question"], input["url"], llm, embeddings_model
        ),
        description="Answers a question using the content of the provided website. Input must include 'question' and 'url'.",
    )
