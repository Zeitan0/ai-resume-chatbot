# 🤖 RESUME_BOT.SYS | AI-Powered Assistant

A retro-inspired **RAG (Retrieval-Augmented Generation)** application that allows users to chat with my professional resume in real-time. This system bridges the gap between static PDF data and interactive AI inference.

---

## 👾 System Overview
* **Core Engine:** Python / Flask
* **AI Logic:** Ollama (Llama 3)
* **UI Aesthetic:** Pink Pixel / ZL_WEB_OS
* **Data Source:** `Zengtao_Liang_Resume.pdf`

---

## 🚀 Key Features
* **PDF Context Injection:** Automatically parses and extracts text from my resume using **PyPDF2** to provide the LLM with ground-truth data.
* **Local Inference:** Powered by **Ollama**, ensuring all data processing stays local and private (no API keys or external data leaks).
* **Reactive UI:** A custom pixel-art frontend featuring "System Thinking" states and flashing CSS animations to handle model latency.
* **Retro UX:** Optimized for the **ZL Web.SYS** ecosystem with signature pink gradients and blocky borders.

---

## 🛠️ Tech Stack
* **Backend:** [Flask](https://flask.palletsprojects.com/) (Python)
* **LLM:** [Llama 3](https://ollama.com/library/llama3) via Ollama
* **PDF Processing:** [PyPDF2](https://pypi.org/project/PyPDF2/)
* **Frontend:** HTML5 / CSS3 (Pixel-Art Engine) / Vanilla JS

---

## ⚙️ Installation & Boot Sequence

### 1. Prerequisite: Local LLM
Download and install [Ollama](https://ollama.com/). Once installed, pull the model:
```bash
ollama pull llama3
```

### 2. Clone & Setup
# Clone the repository
```bash
git clone [https://github.com/Zeitan0/my-portfolio.git](https://github.com/Zeitan0/my-portfolio.git)
cd my-portfolio
```
# Install Python dependencies
```bash
pip install flask requests pypdf2
```

### 3. Initialize System
Make sure your resume file is named Zengtao_Liang_Resume.pdf and is located in the root directory.
```bash
# Run the Flask server
python app.py
The terminal will initialize at http://127.0.0.1:5000
```