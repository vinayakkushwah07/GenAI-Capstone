def smart_chunk(text, chunk_size=500, overlap=100):
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        if len(current_chunk) + len(para) < chunk_size:
            current_chunk += " " + para
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para

    if current_chunk:
        chunks.append(current_chunk.strip())

    final_chunks = []
    for i in range(len(chunks)):
        chunk = chunks[i]
        if i > 0:
            chunk = chunks[i-1][-overlap:] + " " + chunk
        final_chunks.append(chunk.strip())

    return final_chunks

