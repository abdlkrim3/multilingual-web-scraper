# Shared state across modules
class ScraperState:
    def __init__(self):
        self.total_scraped_pages = 0
        self.lang_pages_saved = 0
        self.visited_urls = set()
        self.saved_hashes = set()
        self.existing_urls = set()

scraper_state = ScraperState()