from sentence_transformers import SentenceTransformer
import chromadb
import uuid

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="pdf_docs"
)


def store_chunks(chunks):

    for chunk in chunks:

        embedding = model.encode(
            chunk["content"]
        ).tolist()

        collection.add(
            ids=[str(uuid.uuid4())],
            embeddings=[embedding],
            documents=[chunk["content"]],
            metadatas=[
                {
                    "file": chunk["file"],
                    "page": chunk["page"]
                }
            ]
        )


def search_docs(query):

    query_embedding = model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    return results

def keyword_search(query):

    results = collection.get()

    matched_docs = []

    for doc in results["documents"]:

        if query.lower() in doc.lower():

            matched_docs.append(doc)

    return matched_docs[:3]