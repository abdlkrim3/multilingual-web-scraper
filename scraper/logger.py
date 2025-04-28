# logger.py
import streamlit as st

class ScraperLogger:
    MAX_LOG_LENGTH = 200  # Maximum number of log messages to keep

    def __init__(self):
        self.log_container = None
        self.log_content = []

    def initialize(self):
        self._setup_styles()
        self.log_container = st.empty()

    def _setup_styles(self):
        st.markdown("""
            <style>
                .log-container {
                    height: 300px;
                    overflow-y: scroll;
                    border: 1px solid #ccc;
                    padding: 10px;
                    border-radius: 5px;
                    background-color: #f9f9f9;
                    margin-bottom: 20px;
                    font-family: monospace;
                }
                .log-warning { color: orange; }
                .log-success { color: green; }
                .log-error { color: red; }
                .log-info { color: blue; }
            </style>
        """, unsafe_allow_html=True)

    def _auto_scroll(self):
        st.markdown("""
            <script>
            const logContainer = window.parent.document.querySelector('.log-container');
            if (logContainer) {
                logContainer.scrollTop = logContainer.scrollHeight;
            }
            </script>
        """, unsafe_allow_html=True)

    def log(self, message, msg_type="info"):
        if self.log_container is None:
            raise RuntimeError("Logger not initialized. Please call 'logger.initialize()' first.")

        prefix = ""
        if msg_type == "warning":
            prefix = "⚠️ "
        elif msg_type == "success":
            prefix = "✅ "
        elif msg_type == "error":
            prefix = "❌ "
        
        self.log_content.append(f"{prefix}{message}")

        # Keep only the latest MAX_LOG_LENGTH messages
        if len(self.log_content) > self.MAX_LOG_LENGTH:
            self.log_content = self.log_content[-self.MAX_LOG_LENGTH:]

        self.log_container.markdown(
            f'<div class="log-container">{"<br>".join(self.log_content)}</div>',
            unsafe_allow_html=True
        )
        self._auto_scroll()

    def clear(self):
        """Clear all logs."""
        self.log_content = []
        self.log_container.empty()

# Singleton instance
logger = ScraperLogger()

