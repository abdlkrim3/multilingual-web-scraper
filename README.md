# 🌍 Multilingual Topic Web Scraper

This project is a **Streamlit web application** that allows users to **scrape text content** in multiple languages (**Arabic, French, English**) based on a specific **topic** or from a **custom website**.  
It leverages **SerpAPI** to search Google and uses **BeautifulSoup** to extract and save meaningful content.  
The scraped data is stored as **text files** and summarized into a **CSV metadata file**.

---

# ✨ Features

- 📋 Preview saved metadata directly in the app.
- 🌍 Supports **Arabic**, **French**, and **English** scraping.
- 🔎 Search Google via **SerpAPI** for topic-related websites.
- 🔗 Option to **crawl a custom website** directly.
- 🧠 Provide **custom keywords** to improve content relevance.
- 📑 Choose which **HTML tags** to scrape (e.g., `<p>`, `<div>`, `<article>`).
- 🔢 Filter results based on the **minimum number of keywords found**.
- ⏹️ Ability to **Stop Scraping** at any time.
- 📊 Automatically **logs** progress and results.
- 🗂 **Text files** and **CSV metadata** saved locally.

---

# 🚀 How to Install

1. Clone the repository:
    ```bash
    git clone https://github.com/abdlkrim3/multilingual-web-scraper.git
    cd multilingual-web-scraper
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

# 📚 How to Use

1. Run the Streamlit app:
    ```bash
    cd scraper
    streamlit run app.py
    ```

---

# 🖥️ Main Interface Options

| Option                           | Description                                                              |
| -------------------------------- | ------------------------------------------------------------------------ |
| 🌍 **Select Language**           | Choose scraping language (**Arabic**, **French**, **English**)           |
| 🎯 **Enter Topic**               | Main topic you want to search for (e.g., *موسيقى*, *politique*, *music*) |
| 🧠 **Additional Keywords**       | Comma-separated keywords to strengthen relevance (e.g., *أغنية*, *عزف*)  |
| 🔢 **Minimum Relevant Keywords** | Minimum number of keywords that must be present in the text              |
| 🔑 **Enter SerpAPI Key**         | Your SerpAPI key (required if not crawling a specific site)              |
| 🔗 **Custom Site URL**           | (Optional) URL of a specific site you want to crawl                      |
| 🔍 **Number of Google Results**  | How many Google search results to fetch                                  |
| 📡 **Crawl Depth**               | How deep to crawl within a site (e.g., follow links 2–5 layers deep)     |
| 🏷️ **HTML Tags to Scrape From** | Select HTML tags to extract text from                                    |
| 🚫 **Skip YouTube Links**         | Enable to ignore YouTube links in search results                         |

---

# ⚡️ Actions

- 🚀 **Start Scraping**: Begin scraping based on provided inputs.
- ⏹️ **Stop Scraping**: Immediately stop the ongoing scraping process.
- 🔄 **Refresh Counts**: Update the stats for how many pages and metadata records have been saved.

---

# 📈 Results

- Scraped **text files** are saved in the `scraped_texts/` folder.
- Metadata is stored in `scraped_data.csv`.
- A live preview of saved metadata is displayed at the bottom of the page.

---

# 📂 Project Structure

```bash
.
├── app.py              # Main Streamlit app
├── logger.py           # Logging functionality
├── search.py           # Search with SerpAPI
├── crawling.py         # Site crawling logic
├── state.py            # Global state management during scraping
├── scraped_texts/      # Folder for saved .txt text files
├── pdf/                # Folder (reserved) for future PDF saving
└── scraped_data.csv    # CSV metadata of the scraping results
```

---

# 🔧 Requirements

- **Python 3.10+**

First, try installing all dependencies with the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

If you encounter any issues, you can manually install the main dependencies:

```bash
pip install streamlit pandas requests beautifulsoup4 serpapi
```

---

# 📑 Notes

- A **SerpAPI key** is needed for Google search functionality. You can get a free key at [serpapi.com](https://serpapi.com/).
- If you don't want to use SerpAPI, simply provide a **custom site URL** to crawl.
- The app **avoids duplicate scraping** by checking previously saved URLs.
- You can **stop scraping** at any time and the progress will be **saved**.

---

# 📈 Example Use Case

Imagine you want to build a dataset about **Arabic music**:

1. Choose language: **Arabic**
2. Enter topic: **موسيقى**
3. Add keywords: **غناء**, **أنغام**, **أغنية**, **عزف**
4. Enter your **SerpAPI key**
5. Set number of results: **10**
6. Select tags: **p**, **div**
7. Press 🚀 **Start Scraping**

The app will scrape texts about Arabic music from different websites and **save the content**!

---

# 🛠️ Future Improvements (Ideas)

- Export PDFs instead of text files.
- Add proxy support for broader scraping.
- Summarize scraped content automatically using AI.
- Add multi-language detection (auto-detect) instead of manual selection.
- Display graphs/charts about scraping progress.

---

# 📜 License

This project is licensed under the **MIT License**.

