# Google search using SerpAPI
import requests
import streamlit as st
from logger import logger


def search_google_serpapi(topic, api_key, num_results=5, lang_code='ar', skip_youtube=True):
    query = topic
    params = {
        "q": query,
        "hl": lang_code,
        "num": num_results,  # Request extra to account for filtered results
        "api_key": api_key,
        "engine": "google"
    }
    
    try:
        response = requests.get("https://serpapi.com/search", params=params, timeout=30)
        response.raise_for_status()
        results = response.json().get("organic_results", [])
        
        # Filter out unwanted domains and file types
        filtered_results = []
        for r in results:
            if "link" not in r:
                continue
                
            url = r["link"].lower()
            
            # Skip conditions
            if (
                skip_youtube and ("youtube.com" in url or "youtu.be" in url) or
                url.endswith(('.pdf', '.jpg', '.png', '.docx'))  # Exclude file types but allow PDFs
            ):
                continue
                
            filtered_results.append(r["link"])
        
        # Return the requested number of results
        final_results = filtered_results[:num_results]
        
        if len(final_results) < num_results:
            #st.warning(f"⚠️ Only found {len(final_results)} suitable results (skipped YouTube/PDFs)")
            logger.log(f"Only found {len(final_results)} suitable results (skipped YouTube)", "warning")

        
        return final_results
        
    except Exception as e:
        #st.error(f"🔴 Search failed: {e}")
        logger.log(f"🔴 Search failed: {e}")
        return []