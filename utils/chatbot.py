import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def answer_question(
    question,
    docs,
    history=None
):

    if history is None:
        history = []

    context = "\n".join(docs)

    previous_chat = ""

    for msg in history[-5:]:

        previous_chat += (
            f"User: {msg['question']}\n"
            f"Assistant: {msg['answer']}\n"
        )

    prompt = f"""
    Answer ONLY using the context.

    Previous Conversation:
    {previous_chat}

    Context:
    {context}

    Question:
    {question}

    If the answer is not found,
    say:
    'Information not found in the uploaded documents.'
    """

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"Gemini Error: {str(e)}"