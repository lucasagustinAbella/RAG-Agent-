from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QTextBrowser,
    QPushButton,
)
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QTextCursor
from ml.rag_agent import RAGAgent


class QueryThread(QThread):
    result_ready = pyqtSignal(dict)

    def __init__(self, query):
        super().__init__()
        self.query = query
        self.agent = RAGAgent()

    def run(self):
        try:
            result = self.agent.process_query(self.query)
        except Exception as e:
            result = {"ai_response": f"Error: {str(e)}", "tools_used": "None"}
        self.result_ready.emit(result)


class RAGChat(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("🎬 RAG Chat")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.chat_display = QTextBrowser(self)
        self.chat_display.setOpenExternalLinks(True)
        self.chat_display.setStyleSheet(
            "background-color: #f4f4f4; padding: 10px; border-radius: 10px;"
        )
        layout.addWidget(self.chat_display)

        self.query_input = QLineEdit(self)
        self.query_input.setPlaceholderText("Ask about a movie or TV show...")
        self.query_input.setStyleSheet(
            "padding: 8px; border-radius: 10px; border: 1px solid #ccc;"
        )
        layout.addWidget(self.query_input)

        self.send_button = QPushButton("Send", self)
        self.send_button.setStyleSheet(
            "background-color: #007bff; color: white; padding: 8px; border-radius: 10px;"
        )
        self.send_button.clicked.connect(self.run_query)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def run_query(self):
        query = self.query_input.text().strip()
        if query:
            self.append_message("🧑‍💻 You", query, "#d1e7dd")
            self.query_input.clear()

            self.query_thread = QueryThread(query)
            self.query_thread.result_ready.connect(self.display_response)
            self.query_thread.start()

    def display_response(self, result):
        ai_response = result.get("ai_response", "No AI response available.")
        tools_used = result.get("tools_used", "Unknown Tools")
        formatted_response = (
            f"<div style='background-color: #e1f5fe; padding: 10px; border-radius: 10px; margin: 5px 0;'>"
            f"<b>🤖 AI</b> | 🛠️ <b>Tools Used:</b> {tools_used}<br><br>{ai_response}</div>"
        )

        self.chat_display.setHtml(self.chat_display.toHtml() + formatted_response)

    def append_message(self, sender, message, bg_color):
        formatted_message = (
            f"<div style='background-color: {bg_color}; padding: 10px; border-radius: 10px; margin: 5px 0;'>"
            f"<b>{sender}:</b> {message}</div>"
        )
        self.chat_display.setHtml(self.chat_display.toHtml() + formatted_message)


if __name__ == "__main__":
    app = QApplication([])
    window = RAGChat()
    window.show()
    app.exec()
