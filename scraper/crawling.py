import requests
from state import scraper_state
from logger import logger
from urllib.parse import urljoin
from filters import is_pdf_link, is_valid_internal_link, is_relevant_text
from save import save_text
from extraction import download_pdf, extract_language_paragraphs
from bs4 import BeautifulSoup
import streamlit as st
import random
import time

def crawl_site_with_filter(url, base_domain, topic_keywords, tags, lang_code="ar", depth=2, stop_flag=None, min_keywords=1):
    if depth == 0 or url in scraper_state.visited_urls or url in scraper_state.existing_urls:
        return
    
    try:
        if stop_flag and stop_flag():
            logger.log("⏹️ Scraping stopped by user.")
            return

        scraper_state.visited_urls.add(url)
        scraper_state.total_scraped_pages += 1
        #st.write(f"🌐 Crawling ({depth}): {url}")
        logger.log(f"🌐 Crawling ({depth}): {url}", "info")
        
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # Raise exception for bad status codes
        html = response.text

        if is_pdf_link(url):
            download_pdf(url)
            return

        paragraphs = extract_language_paragraphs(html, lang_code=lang_code, tags=tags, topic_keywords=topic_keywords)
        if not paragraphs or not is_relevant_text(paragraphs, topic_keywords, min_keywords):
            logger.log(f"Skipped irrelevant content from: {url}", "warning")
            return

        # Pass the full topic_keywords list to save_text
        save_text(url, paragraphs, html, topic_keywords[0], topic_keywords)

        # Continue crawling
        soup = BeautifulSoup(html, "html.parser")
        for link in soup.find_all("a", href=True):
            href = link['href']
            full_url = urljoin(url, href.split('#')[0].split('?')[0])
            if is_valid_internal_link(full_url, base_domain):
                crawl_site_with_filter(
                    full_url, 
                    base_domain, 
                    topic_keywords, 
                    tags, 
                    lang_code=lang_code, 
                    depth=depth - 1, 
                    stop_flag=stop_flag
                )

    except requests.exceptions.RequestException as e:
        #st.warning(f"❌ Network error crawling {url}: {e}")
        logger.log(f"Network error crawling {url}: {e}", "error")
    except Exception as e:
        #st.warning(f"❌ Error crawling {url}: {e}")
        logger.log(f"Error crawling {url}: {e}", "error")
    finally:
        time.sleep(random.uniform(1, 3))