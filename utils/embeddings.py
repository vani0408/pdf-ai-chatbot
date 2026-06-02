from sentence_transformers import SentenceTransformer
import chromadb
import uuid

model = None
client = None
collection = None


def get_model():

    global model

    if model is None:

        model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    return model


def get_collection():

    global client
    global collection

    if collection is None:

        client = chromadb.PersistentClient(
            path="chroma_db"
        )

        collection = client.get_or_create_collection(
            name="pdf_docs"
        )

    return collection


def store_chunks(chunks):

    collection = get_collection()

    for chunk in chunks:

        embedding = get_model().encode(
            chunk["content"]
        ).tolist()

        metadata = {
            "page": chunk["page"]
        }

        if "file" in chunk:

            metadata["file"] = chunk["file"]

        collection.add(
            ids=[str(uuid.uuid4())],
            embeddings=[embedding],
            documents=[chunk["content"]],
            metadatas=[metadata]
        )


def search_docs(query):

    collection = get_collection()

    query_embedding = get_model().encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    return results


def keyword_search(query):

    collection = get_collection()

    results = collection.get()

    matched_docs = []

    for doc in results["documents"]:

        if query.lower() in doc.lower():

            matched_docs.append(doc)

    return matched_docs[:3]