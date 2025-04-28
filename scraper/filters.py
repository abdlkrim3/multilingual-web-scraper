from urllib.parse import urlparse
from logger import logger

def is_valid_internal_link(link, base_domain):
    parsed = urlparse(link)
    return (parsed.netloc == '' or base_domain in parsed.netloc) and not link.endswith(('.jpg', '.png', '.pdf', '.mp4', '.gif'))

def is_pdf_link(url):
    return url.lower().endswith('.pdf')

def is_relevant_text(text_list, topic_keywords, min_keywords=1):
    """Check if text contains at least min_keywords different keywords"""
    found_keywords = set()
    for paragraph in text_list:
        for keyword in topic_keywords:
            if keyword.lower() in paragraph.lower():
                found_keywords.add(keyword.lower())
                if len(found_keywords) >= min_keywords:
                    return True
    return False