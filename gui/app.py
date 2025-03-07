from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QTextBrowser,
    QPushButton,
)
from PyQt6.QtCore import QThread, pyqtSignal
from urllib.parse import quote
from ml.main_runner import RAGAgent


class QueryThread(QThread):
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

        self.result_display = QTextBrowser(self)
        self.result_display.setOpenExternalLinks(True)
        layout.addWidget(self.result_display)

        self.setLayout(layout)

    def run_query(self):
        query = self.query_input.text().strip()
        if query:
            self.result_display.setText("🔍 Searching... Please wait.")
            self.search_button.setEnabled(False)
            self.query_thread = QueryThread(query)
            self.query_thread.result_ready.connect(self.display_result)
            self.query_thread.start()

    def display_result(self, result):
        self.search_button.setEnabled(True)

        imdb_info = result.get("movie_info", {})
        trailer_info = result.get("trailer_url", "Not available")
        web_results = result.get("web_results", [])
        ai_response = result.get("ai_response", "No AI response available.")

        final_text = self.format_imdb_info(imdb_info)
        final_text += self.format_trailer_info(trailer_info)
        final_text += self.format_web_results(web_results)
        final_text += self.format_ai_response(ai_response)

        self.result_display.setHtml(final_text)

    def format_imdb_info(self, imdb_info):
        if imdb_info is None:
            return "<b>🎬 Movie info not available.</b><br>"

        imdb_url = self.safely_quote(imdb_info.get("url", "#"))
        imdb_text = f"<b>🎬 {imdb_info.get('title', 'Unknown')}</b> ({imdb_info.get('year', 'N/A')})<br>"
        imdb_text += f"⭐ Rating: {imdb_info.get('rating', 'N/A')}<br>"
        imdb_text += f"🎭 Genres: {', '.join(imdb_info.get('genres', []))}<br>"
        imdb_text += f"📖 Plot: {imdb_info.get('plot', 'No plot available.')}<br>"
        imdb_text += f"IMDb Link: <a href='{imdb_url}'> {imdb_info.get('title', 'Unknown')} on IMDb</a><br><br>"
        return imdb_text

    def format_trailer_info(self, trailer_info):
        if trailer_info != "Not available":
            trailer_url = self.safely_quote(trailer_info.get("url", "Not available"))
            trailer_title = trailer_info.get("title", "No trailer title available")
            trailer_text = f"<b>🎥 Trailer:</b> <a href='{trailer_url}'> {trailer_title} </a><br><br>"
        else:
            trailer_text = "<b>🎥 Trailer:</b> Not available.<br><br>"
        return trailer_text

    def format_web_results(self, web_results):
        web_text = "<b>🌐 Web Results:</b><br>"
        if web_results:
            for res in web_results[:3]:
                web_text += f"{res['title']} - {res['url']}<br>{res['snippet']}<br><br>"
        else:
            web_text += "No web results found.<br><br>"
        return web_text

    def format_ai_response(self, ai_response):
        return f"<b>🤖 AI Response:</b><br>{ai_response}"

    def safely_quote(self, url):
        if isinstance(url, str) and url not in ["Not available", "#"]:
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            return quote(url, safe=":/?&=")
        return url


if __name__ == "__main__":
    app = QApplication([])
    window = RAGApp()
    window.show()
    app.exec()
