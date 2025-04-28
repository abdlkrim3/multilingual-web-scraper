import os
import re
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from langdetect import detect
from logger import logger
import streamlit as st
from logger import logger

def extract_language_paragraphs(html, lang_code="ar", tags=["p"], topic_keywords=None):
    soup = BeautifulSoup(html, "html.parser")
    seen_texts = set()
    selected_texts = []
    
    # Use only the tags selected in the Streamlit UI
    for tag in tags:
        elements = soup.find_all(tag)
        for el in elements:
            raw_text = el.get_text(separator='\n').strip()
            if not raw_text or len(raw_text) < 30:  # Slightly reduced minimum length
                continue
                
            try:
                # Language detection
                detected_lang = detect(raw_text)
                if detected_lang != lang_code:
                    continue
                    
                # Language-specific cleaning
                if lang_code == 'ar':
                    clean_text = re.sub(r'[^\u0600-\u06FF\u0750-\u08FF\s]', '', raw_text)
                else:
                    clean_text = re.sub(r'[^\w\s]', '', raw_text)
                
                clean_text = re.sub(r'\s+', ' ', clean_text).strip()
                
                # Early keyword filtering if keywords provided
                if topic_keywords:
                    if not any(kw.lower() in clean_text.lower() for kw in topic_keywords):
                        continue
                
                # Final quality checks
                if len(clean_text) >= 30 and clean_text not in seen_texts:
                    seen_texts.add(clean_text)
                    selected_texts.append(clean_text)
                    
            except Exception as e:
                #st.warning(f"⚠️ Extraction warning: {str(e)}")
                logger.log(f"Extraction warning: {str(e)}", "error")
                continue
    
    # Fallback for very short but relevant content
    if not selected_texts and topic_keywords:
        body_text = soup.get_text(separator='\n').strip()
        if body_text and any(kw.lower() in body_text.lower() for kw in topic_keywords):
            selected_texts.append(body_text[:1000])  # Take first 1000 chars as fallback
            
    return selected_texts

def download_pdf(url):
    folder = "pdf"
    os.makedirs(folder, exist_ok=True)
    pdf_name = os.path.join(folder, os.path.basename(urlparse(url).path))

    try:
        response = requests.get(url, timeout=10, stream=True)
        if response.status_code == 200:
            with open(pdf_name, 'wb') as pdf_file:
                for chunk in response.iter_content(1024):
                    pdf_file.write(chunk)
            #st.write(f"💾 PDF saved to: {pdf_name}")
            logger.log(f"💾 PDF saved to: {pdf_name}", "success")
        else:
            #st.warning(f"❌ Failed to download PDF from: {url}")
            logger.log(f"Failed to download PDF from: {url}", "error")
    except Exception as e:
        #st.warning(f"❌ Error downloading PDF from {url}: {e}")
        logger.log(f"Error downloading PDF from {url}: {e}", "error")
        


