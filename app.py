from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os

from utils.pdf_processor import extract_text
from utils.chunker import create_chunks
from utils.chatbot import answer_question
from utils.embeddings import (
    store_chunks,
    search_docs,
    keyword_search
)

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

chat_history = []


@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route("/upload", methods=["POST"])
def upload():

    files = request.files.getlist(
        "pdfs"
    )

    if len(files) == 0:

        return jsonify({
            "error":
            "No PDFs uploaded"
        }), 400

    all_chunks = []

    for file in files:

        if file.filename == "":
            continue

        filename = secure_filename(
            file.filename
        )

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        file.save(filepath)

        pages = extract_text(
            filepath
        )

        chunks = create_chunks(
            pages
        )

        for chunk in chunks:

            chunk["file"] = filename

        all_chunks.extend(
            chunks
        )

    store_chunks(
        all_chunks
    )



    return jsonify({
        "message":
        f"{len(files)} PDF(s) uploaded successfully"
    })


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    question = data.get(
        "question"
    )

    if not question:

        return jsonify({
            "error":
            "Question required"
        }), 400

    results = search_docs(
        question
    )
    keyword_docs = keyword_search(question)

    print("\nQUESTION:", question)
    print("KEYWORD MATCHES FOUND:", len(keyword_docs))
    print(keyword_docs)

    docs = results["documents"][0]

    docs.extend(
        keyword_docs

    )

    

    docs = list(
        dict.fromkeys(docs)
    )

    sources = []

    seen = set()

    for metadata in results["metadatas"][0]:
        file_name = metadata.get(
            "file",
            "Uploaded Document"
        )

        page_num = metadata.get(
            "page",
            "Unknown"
        
        )

        key = (
            file_name,
            page_num

        )

        if key not in seen:
            seen.add(key)
            sources.append({
                "file": file_name,
                "page": page_num

            })

    answer = answer_question(
        question,
        docs,
        chat_history
    )

    chat_history.append({

        "question":
        question,

        "answer":
        answer
    })

    short_docs = []

    for doc in docs:
        short_docs.append(
            doc[:300]
        )

    return jsonify({

        "answer":
        answer,

        "sources":
        sources,

        "excerpt":
        short_docs,

        "chat_history":
        chat_history
    })


@app.route("/history")
def history():

    return jsonify(
        chat_history
    )



if __name__ == "__main__":

    import os

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )