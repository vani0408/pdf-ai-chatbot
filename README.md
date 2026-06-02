# PDF-Based AI Chatbot

## Overview

This project is a Retrieval-Augmented Generation (RAG) based PDF Chatbot that allows users to upload one or more PDF documents and ask questions about their contents using Google's Gemini LLM.

The system extracts text from PDFs, converts text into embeddings, stores them in a vector database (ChromaDB), retrieves relevant chunks using hybrid search, and generates answers with source attribution.

---

## Features

### Core Features

* Upload PDF documents (single or multiple PDFs)
* Extract text from PDFs
* Chunk document content
* Generate embeddings
* Store embeddings in ChromaDB
* Semantic retrieval using vector search
* Question answering using Gemini
* Chat history during session
* Source attribution
* Relevant excerpt display
* Public deployment ready

### Bonus Features

* Multiple PDF support
* Conversation memory
* OCR support for scanned PDFs
* Hybrid search (Keyword + Vector Search)
* Docker setup

---

## Tech Stack

### Backend

* Flask
* Python

### LLM

* Gemini 2.5 Flash

### Embedding Model

* all-MiniLM-L6-v2
* Sentence Transformers

### Vector Database

* ChromaDB

### Frontend

* HTML
* CSS
* JavaScript
* Bootstrap

### OCR

* Tesseract OCR
* pdf2image

---

## Architecture Diagram

```text
User
  |
  v
Upload PDF(s)
  |
  v
PDF Text Extraction
  |
  +-------------------+
  |                   |
  | Normal PDF        |
  | PyPDF2            |
  |                   |
  +-------------------+
          |
          v
  OCR Fallback
 (Scanned PDFs)
          |
          v
     Chunking
          |
          v
Generate Embeddings
(all-MiniLM-L6-v2)
          |
          v
      ChromaDB
          |
          v
   Hybrid Search
(Vector + Keyword)
          |
          v
 Gemini 2.5 Flash
          |
          v
Answer + Citations
```

---

## Project Structure

```text
pdfchatbot
│
├── app.py
├── requirements.txt
├── .env
├── Dockerfile
├── docker-compose.yml
│
├── uploads
├── chroma_db
│
├── templates
│   └── index.html
│
├── static
│   ├── style.css
│   └── script.js
│
└── utils
    ├── pdf_processor.py
    ├── chunker.py
    ├── embeddings.py
    └── chatbot.py
```

---

## Chunking Strategy

The extracted PDF text is split into overlapping chunks.

Configuration:

* Chunk Size: 800 characters
* Overlap: 50 characters

Reason:

* Preserves context across chunk boundaries.
* Improves retrieval quality.
* Reduces information loss.

---

## Embedding Model Choice

Model Used:

all-MiniLM-L6-v2

Reasons:

* Lightweight
* Fast embedding generation
* Strong semantic similarity performance
* Widely used in RAG applications

---

## Retrieval Approach

The system uses Hybrid Search.

### 1. Vector Search

User query is converted into embeddings.

ChromaDB retrieves the most semantically relevant chunks.

### 2. Keyword Search

Exact keyword matching is performed across stored chunks.

This improves retrieval for:

* Email addresses
* Phone numbers
* Names
* Technical terms
* Exact phrases

### 3. Result Merging

Results from both searches are merged and deduplicated before being sent to Gemini.

---

## OCR Support

For scanned PDFs:

1. PyPDF2 attempts text extraction.
2. If no text is found:

   * PDF page is converted into an image.
   * Tesseract OCR extracts text.
3. Extracted text is processed normally.

This enables support for image-based PDFs.

---

## Prompt Design

Prompt Template:

```text
Answer only using the provided context.

Context:
{retrieved_chunks}

Chat History:
{chat_history}

Question:
{user_question}
```

Reasons:

* Reduces hallucinations.
* Keeps answers grounded in documents.
* Utilizes conversation memory.

---

## Source Attribution

Each answer includes:

* Source document name
* Source page number
* Relevant excerpts

Example:

```text
Answer:
The candidate worked as a Machine Learning Intern. [1]

Sources:
[1] vani_jain_resume.pdf - Page 1

Relevant Excerpt:
Developed supervised ML models for predictive maintenance...
```

---

## Conversation Memory

Chat history is stored during the active session.

Previous user questions and chatbot responses are included in future prompts.

This enables contextual follow-up questions.

---

## Docker Setup

Build:

```bash
docker build -t pdf-chatbot .
```

Run:

```bash
docker run -p 5000:5000 pdf-chatbot
```

Using Docker Compose:

```bash
docker-compose up --build
```

---

## Installation

### Clone Repository

```bash
git clone <repository_url>
cd pdfchatbot
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create:

```text
.env
```

Add:

```text
GEMINI_API_KEY=YOUR_API_KEY
```

### Run Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## Future Improvements

* Streaming responses
* Citation highlighting inside PDFs
* User authentication
* Persistent user sessions
* Advanced reranking
* Cloud vector database integration

---

## Author

Vani Jain
