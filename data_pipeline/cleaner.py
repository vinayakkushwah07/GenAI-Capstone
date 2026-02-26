import re
from collections import Counter

def remove_numeric_garbage(text):
    lines = text.split("\n")
    cleaned = []

    for line in lines:
        digits_ratio = sum(c.isdigit() for c in line) / (len(line)+1)
        if digits_ratio < 0.6:
            cleaned.append(line)

    return "\n".join(cleaned)

def remove_toc(text):
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        if re.search(r"\.{3,}", line):
            continue
        if re.match(r"^\d+(\.\d+)+", line):
            continue
        cleaned.append(line)
    return "\n".join(cleaned)

def merge_broken_lines(text):
    lines = text.split("\n")
    merged = []
    buffer = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if buffer and not buffer.endswith(('.', '?', '!')):
            buffer += " " + line
        else:
            if buffer:
                merged.append(buffer)
            buffer = line

    if buffer:
        merged.append(buffer)

    return "\n\n".join(merged)

def clean_text(text):
    text = remove_numeric_garbage(text)
    text = remove_toc(text)
    text = merge_broken_lines(text)
    return text.strip()
