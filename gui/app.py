from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QTextBrowser,
    QPushButton,
    QLabel,
)
from PyQt6.QtCore import QThread, pyqtSignal
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


class RAGApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("🎬 RAG Movie Search")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.query_input = QLineEdit(self)
        self.query_input.setPlaceholderText("Enter a movie or TV show...")
        layout.addWidget(self.query_input)

        self.search_button = QPushButton("🔍 Search", self)
        self.search_button.clicked.connect(self.run_query)
        layout.addWidget(self.search_button)

        self.result_display = QTextBrowser(self)
        self.result_display.setOpenExternalLinks(True)
        layout.addWidget(self.result_display)

        self.tool_label = QLabel(self)
        layout.addWidget(self.tool_label)

        self.setLayout(layout)

    def run_query(self):
        query = self.query_input.text().strip()
        if query:
            self.result_display.setText("🔍 Searching... Please wait.")
            self.tool_label.setText("")
            self.search_button.setEnabled(False)

            self.query_thread = QueryThread(query)
            self.query_thread.result_ready.connect(self.display_response)
            self.query_thread.start()

    def display_response(self, result):
        self.search_button.setEnabled(True)
        ai_response = result.get("ai_response", "No AI response available.")
        tools_used = result.get("tools_used", "Unknown Tools")

        final_text = (
            f"<b>🛠️ Tools Used: {tools_used}</b><br><br>"
            f"<b>📚 Result:</b><br>{ai_response}"
        )

        self.result_display.setHtml(final_text)


if __name__ == "__main__":
    app = QApplication([])
    window = RAGApp()
    window.show()
    app.exec()
