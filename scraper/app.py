import os
import time
import csv
from datetime import timedelta
from urllib.parse import urlparse
import streamlit as st
import pandas as pd
from state import scraper_state
from logger import logger
from search import search_google_serpapi
from crawling import  crawl_site_with_filter


# Create required directories if they don't exist
os.makedirs("scraped_texts", exist_ok=True)
os.makedirs("pdf", exist_ok=True)

# Sets for tracking
total_scraped_pages = 0
lang_pages_saved = 0
start_time = time.time()
before_scraping = set(os.listdir("scraped_texts")) if os.path.exists("scraped_texts") else set()

# Output CSV file setup
csv_file = "scraped_data.csv"
# At the top where CSV headers are defined:
csv_headers = ["Topic", "URL", "Title", "Date", "Content Preview", "Found Keywords"]

# And where you initialize the CSV:
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(csv_headers)

# Load previously saved URLs to avoid duplicates
if os.path.exists(csv_file):
    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            scraper_state.existing_urls.add(row['URL'])

stop_signal = False

def run_app():
    st.set_page_config(page_title="Multilingual Topic Scraper", layout="wide")
    st.title("🌐 Multilingual Topic Web Scraper")

    global stop_signal, total_scraped_pages, lang_pages_saved, start_time, before_scraping

    stop_signal = False
    scraper_state.visited_urls.clear()
    def stop_scraping():
        return stop_signal
    

    # UI Controls
    with st.form("scraper_controls"):
        language_option = st.selectbox("🌍 Select Language:", options=["Arabic", "French", "English"], index=0)
        lang_code_map = {"Arabic": "ar", "French": "fr", "English": "en"}
        selected_lang_code = lang_code_map[language_option]

        topic = st.text_input("🎯 Enter Topic (e.g., موسيقى, politique, music):", value="موسيقى")
        keyword_input = st.text_area("🧠 Additional Keywords (comma separated):", value="غناء, أنغام, أغنية, عزف, إيقاع, فن, موسيقي")
        min_keywords = st.slider("🔢 Minimum Relevant Keywords", 1, 3, 2)
        serpapi_key = st.text_input("🔑 Enter SerpAPI Key:", type="password")
        custom_site_url = st.text_input("🔗 Or enter a specific website to crawl (optional):", value="")
        num_results = st.slider("🔍 Number of Google Results", 1, 100, 5)
        crawl_depth = st.slider("📡 Crawl Depth", 1, 5, 2)
        selected_tags = st.multiselect("🏷️ HTML Tags to Scrape From", options=["p", "div", "span", "article"], default=["p"])
        skip_youtube = st.checkbox("Skip YouTube links", value=True)
        submitted = st.form_submit_button("🚀 Start Scraping")
        stop = st.form_submit_button("⏹️ Stop Scraping")
        Refresh = st.form_submit_button("🔄 Refresh Counts")

    before_scraping = set(os.listdir("scraped_texts"))

    logger.initialize()

    if submitted:
        if not serpapi_key.strip() and not custom_site_url.strip():
            st.session_state.log_content.append("🚫 Please provide a SerpAPI key or a custom site URL")
            st.session_state.log_content = []
            return

        with st.spinner("Scraping in progress..."):
            # Reset all state
            scraper_state.__init__()  # This clears all sets and counters
            start_time = time.time()
            before_scraping = set(os.listdir("scraped_texts")) if os.path.exists("scraped_texts") else set()

            keywords = [k.strip() for k in keyword_input.split(',') if k.strip()]
            topic_keywords = [topic] + keywords

            if custom_site_url.strip():
                #st.info("🌐 Crawling only the provided site.")
                logger.log("🌐 Crawling only the provided site", "info")
                try:
                    base_domain = urlparse(custom_site_url).netloc
                    crawl_site_with_filter(
                        custom_site_url.strip(), 
                        base_domain, 
                        topic_keywords, 
                        selected_tags, 
                        lang_code=selected_lang_code, 
                        depth=crawl_depth, 
                        stop_flag=stop_scraping,
                        min_keywords=min_keywords 
                    )
                except Exception as e:
                    #st.warning(f"❌ Failed to crawl the site: {e}")
                    logger.log(f"Failed to crawl the site: {e}", "error")
            else:
                urls = search_google_serpapi(topic, serpapi_key, num_results=num_results, lang_code=selected_lang_code)
                if not urls:
                        logger.log("No search results found", "warning")
                        return
                # Additional filtering (redundant but safe)
                filtered_urls = [
                    url for url in urls 
                    if url not in scraper_state.existing_urls 
                    and url not in scraper_state.visited_urls
                    and (not skip_youtube or ("youtube.com" not in url.lower() and "youtu.be" not in url.lower()))
                ]

                #st.write(f"🔍 Found {len(urls)} results ({len(filtered_urls)} after filtering)")
                logger.log(f"🔍 Found {len(urls)} results ({len(filtered_urls)} after filtering)", "info")
                for url in filtered_urls:
                    try:
                        base_domain = urlparse(url).netloc
                        crawl_site_with_filter(
                            url, 
                            base_domain, 
                            topic_keywords, 
                            selected_tags, 
                            lang_code=selected_lang_code, 
                            depth=crawl_depth, 
                            stop_flag=stop_scraping,
                            min_keywords=min_keywords
                        )
                    except Exception as e:
                        #st.warning(f"❌ Error crawling {url}: {e}")
                        logger.log(f"❌ Error crawling {url}: {e}", "error")

        # Display results using scraper_state values
        elapsed_time = str(timedelta(seconds=int(time.time() - start_time)))
        #st.success("✅ Scraping Finished!")
        logger.log(f"Scraping Finished!", "success")
        #st.info(f"✅ Total pages scraped: {scraper_state.total_scraped_pages}")
        logger.log(f"📊 Total pages scraped: {scraper_state.total_scraped_pages}", "info")
        after_scraping = set(os.listdir("scraped_texts")) if os.path.exists("scraped_texts") else set()
        new_files = [f for f in after_scraping - before_scraping if f.endswith(".txt")]
        #st.info(f"🗂 {language_option} pages saved: {scraper_state.lang_pages_saved}")
        logger.log(f"🗂 {language_option} pages saved: {new_files}", "info")
        #st.info(f"🧾 Metadata saved to: {csv_file}")
        logger.log(f"🧾 Metadata saved to: {csv_file}", "info")
        #st.info(f"⏱ Time taken: {elapsed_time}")
        logger.log(f"⏱ Time taken: {elapsed_time}", "info")
        
    if stop:
        stop_signal = True
        elapsed_time = str(timedelta(seconds=int(time.time() - start_time)))
        
        try:
            df = pd.read_csv(csv_file)
            total_in_csv = len(df)
            arabic_in_csv = len(df[df['Topic'].str.contains('|'.join(topic_keywords), case=False, na=False)])
        except Exception as e:
            logger.log(f"Could not read CSV: {e}", "warning")
            total_in_csv = 0
            arabic_in_csv = 0
        
        after_scraping = set(os.listdir("scraped_texts")) if os.path.exists("scraped_texts") else set()
        new_files = len([f for f in after_scraping - before_scraping if f.endswith(".txt")])
        
        logger.log("🛑 Scraping stopped by user")
        logger.log(f"📊 Total pages scraped: {total_in_csv}", "info")
        logger.log(f"🗂 {language_option} pages saved: {new_files if new_files > 0 else arabic_in_csv}", "info")
        logger.log(f"⏱ Time taken: {elapsed_time}", "info")

    if Refresh:
        try:
            df = pd.read_csv(csv_file)
            logger.log(f"📊 Current total in CSV: {len(df)} records", "info")
            logger.log(f"📁 Current text files: {len(os.listdir('scraped_texts')) if os.path.exists('scraped_texts') else 0}", "info")
        except Exception as e:
            logger.log(f"Could not read counts: {e}", "warning")

    if os.path.exists(csv_file):
        st.subheader("📄 Scraped Metadata Preview")
        with open(csv_file, encoding='utf-8') as f:
            rows = list(csv.reader(f))[1:]
            if rows:
                st.dataframe(rows, use_container_width=True)
            else:
                #st.info("No data available yet.")
                logger.log("ℹ️ No data available yet", "info")

if __name__ == "__main__":
    run_app()






