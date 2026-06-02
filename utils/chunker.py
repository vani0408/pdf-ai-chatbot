def create_chunks(
    pages,
    chunk_size=800,
    overlap=50
):

    chunks = []

    for page_data in pages:

        page_num = page_data["page"]

        text = page_data["text"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end]

            chunks.append({
                "page": page_num,
                "content": chunk_text
            })

            start += (chunk_size - overlap)

    return chunks