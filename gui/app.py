from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QTextBrowser,
    QPushButton,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl
from ml.main_runner import RAGAgent
from urllib.parse import quote


class QueryThread(QThread):
    """Thread to run the query asynchronously."""

    result_ready = pyqtSignal(dict)

    def __init__(self, query):
        super().__init__()
        self.query = query
        self.agent = RAGAgent()

    def run(self):
        result = self.agent.process_query(self.query)
        self.result_ready.emit(result)


class RAGApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("RAG Movie Search")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.query_input = QLineEdit(self)
        self.query_input.setPlaceholderText("Enter a movie or TV show...")
        layout.addWidget(self.query_input)

        self.search_button = QPushButton("Search", self)
        self.search_button.clicked.connect(self.run_query)
        layout.addWidget(self.search_button)

        self.result_display = QTextBrowser(
            self
        )  # Changed from QTextEdit to QTextBrowser
        self.result_display.setOpenExternalLinks(True)  # Enable external link handling
        layout.addWidget(self.result_display)

        self.setLayout(layout)

    def run_query(self):
        query = self.query_input.text().strip()
        if query:
            self.result_display.setText(
                "🔍 Searching... Please wait."
            )  # Show loading state
            self.search_button.setEnabled(False)  # Disable button during search

            # Run query in a separate thread
            self.query_thread = QueryThread(query)
            self.query_thread.result_ready.connect(self.display_result)
            self.query_thread.start()

    def display_result(self, result):
        """Format and display the results."""
        self.search_button.setEnabled(True)  # Re-enable search button

        imdb_info = result.get("movie_info", {})
        trailer_info = result.get("trailer_url", "Not available")
        web_results = result.get("web_results", [])
        ai_response = result.get("ai_response", "No AI response available.")

        imdb_url = self.safely_quote(imdb_info.get("url", "#"))
        trailer_url = self.safely_quote(trailer_info.get("url", "Not available"))
        trailer_title = trailer_info.get("title", "No trailer title available")

        # IMDb Info Formatting with clickable IMDb link
        imdb_text = (
            f"<b>🎬 {imdb_info.get('title', 'Unknown')}</b> ({imdb_info.get('year', 'N/A')})<br>"
            f"⭐ Rating: {imdb_info.get('rating', 'N/A')}<br>"
            f"🎭 Genres: {', '.join(imdb_info.get('genres', []))}<br>"
            f"📖 Plot: {imdb_info.get('plot', 'No plot available.')}<br>"
            f"IMDb Link: <a href='{imdb_url}'> {imdb_info.get('title', 'Unknown')} on IMDb</a><br><br>"
        )

        # Trailer Info Formatting (only showing link and title)
        trailer_text = (
            f"<b>🎥 Trailer:</b> <a href='{trailer_url}'> {trailer_title} </a><br><br>"
            if trailer_url != "Not available"
            else "<b>🎥 Trailer:</b> Not available.<br><br>"
        )

        # Web Results Formatting
        web_text = "<b>🌐 Web Results:</b><br>"
        if web_results:
            for res in web_results[:3]:  # Show only top 3 results
                web_text += f"{res['title']} - {res['url']}<br>{res['snippet']}<br><br>"
        else:
            web_text += "No web results found.<br><br>"

        # AI Response
        ai_text = f"<b>🤖 AI Response:</b><br>{ai_response}"

        # Combine all parts and display
        final_text = imdb_text + trailer_text + web_text + ai_text
        self.result_display.setHtml(final_text)

    def safely_quote(self, url):
        """Safely encode URL to avoid invalid characters."""
        if isinstance(url, str) and url not in ["Not available", "#"]:
            # Add http:// if no protocol is present
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            return quote(url, safe=":/?&=")
        return url  # Return the URL as is if it is not valid or available


if __name__ == "__main__":
    app = QApplication([])
    window = RAGApp()
    window.show()
    app.exec()
