import os
import hashlib
from state import scraper_state
import csv
import re
from bs4 import BeautifulSoup
from logger import logger
import streamlit as st

# Output CSV file setup
csv_file = "scraped_data.csv"

def save_to_csv(data):
    """Helper function to safely save data to CSV"""
    try:
        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(data)
        return True
    except Exception as e:
        #st.error(f"Failed to save to CSV: {e}")
        logger.log(f"Failed to save to CSV: {e}", "error")
        return False

def mark_keywords(text, keywords):
    """Highlight keywords in text with emoji markers"""
    marked = text
    for kw in keywords:
        marked = re.sub(
            f'({re.escape(kw)})', 
            '✨\\1✨',  # Add markers around keywords
            marked, 
            flags=re.IGNORECASE
        )
    return marked

def save_text(url, paragraphs, html, topic, topic_keywords=None):
    if not paragraphs:
        logger.log(f"No paragraphs found for {url}", "warning")
        return

    # Track found keywords (without marking them in text)
    found_keywords = set()
    cleaned_paragraphs = []
    keyword_found = False
    
    for p in paragraphs:
        clean_p = p.strip()
        if topic_keywords:
            # Check for keyword matches
            for kw in topic_keywords:
                if kw.lower() in clean_p.lower():
                    found_keywords.add(kw)
                    keyword_found = True
        cleaned_paragraphs.append(clean_p)

    if topic_keywords and not keyword_found:
        #st.warning(f"⚠️ Skipped content without keywords from: {url}")
        logger.log(f"Skipped content without keywords from: {url}", "warning")
        return

    content = "\n\n".join([p for p in cleaned_paragraphs if p])
    content_hash = hashlib.md5(content.encode("utf-8")).hexdigest()
    
    if content_hash in scraper_state.saved_hashes:
        #st.write(f"⚠️ Skipped duplicate from: {url}")
        logger.log(f"Skipped duplicate from: {url}", "warning")
        return
        
    scraper_state.saved_hashes.add(content_hash)

    # Save clean text content to file (without keyword marks)
    folder = "scraped_texts"
    os.makedirs(folder, exist_ok=True)
    safe_url = re.sub(r'[^\w\s\-]', '', url.split('//')[-1].replace('/', '_')).strip()
    filepath = os.path.join(folder, f"{safe_url[:50]}_{content_hash[:8]}.txt")

    with open(filepath, "w", encoding="utf-8") as f:
        unique_lines = list(dict.fromkeys(content.splitlines()))
        f.write("\n".join([line for line in unique_lines if line.strip()]))
    
    #st.write(f"💾 Saved content to: {filepath}")
    logger.log(f"💾 Saved content to: {filepath}", "info")
    if found_keywords:
        #st.write(f"🔍 Found keywords: {', '.join(found_keywords)}")
        logger.log(f"🔍 Found keywords: {', '.join(found_keywords)}", "info")

    # Extract metadata
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string.strip() if soup.title else "No Title"
    date_match = re.search(r'\d{4}[-/]\d{1,2}[-/]\d{1,2}', html)
    date = date_match.group() if date_match else "No Date Found"
    content_preview = content[:300]

    # Save to CSV with found keywords
    csv_data = [
        topic,
        url,
        title,
        date,
        content_preview,
        ", ".join(found_keywords) if found_keywords else "None"
    ]
    
    if save_to_csv(csv_data):
        #st.write(f"📝 Metadata saved for: {url}")
        logger.log(f"📝 Metadata saved for: {url}", "info")
    else:
        #st.warning(f"⚠️ Failed to save metadata for: {url}")
        logger.log(f"Failed to save metadata for: {url}", "error")

    scraper_state.lang_pages_saved += 1