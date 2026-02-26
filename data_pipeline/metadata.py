import re

def detect_section_title(paragraph):
    if paragraph.isupper() and len(paragraph.split()) < 10:
        return paragraph
    if re.match(r"^\d+(\.\d+)*\s", paragraph):
        return paragraph
    return None
