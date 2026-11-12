# ai-research-search-engine
An AI-powered research search engine built with LangChain, Groq GPT-OSS 20B, Streamlit, DuckDuckGo, Wikipedia, and Arxiv for intelligent web search and academic research.


# 🔍 AI Research Search Engine

An AI-powered research search engine built with **Python, LangChain, Groq GPT-OSS 20B, and Streamlit**. It combines Large Language Models (LLMs) with external search tools to provide intelligent answers, web search results, and academic research information.

## ✨ Features

- 🤖 **AI-Powered Chat:** Uses Groq's GPT-OSS 20B model to generate intelligent responses.
- 🌐 **Web Search:** Search the internet using DuckDuckGo.
- 📚 **Wikipedia Search:** Retrieve information about general knowledge, science, history, and technology.
- 📄 **Research Paper Search:** Find academic and scientific papers using Arxiv.
- 🧠 **AI Tool Calling:** LangChain agents select and execute relevant search tools.
- 💬 **Chat History:** Maintains conversation context during the session.
- 🎨 **Modern UI:** Interactive Streamlit interface with a dark theme.
- ⚡ **Error Handling:** Handles external search service failures gracefully.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Frontend and user interface |
| LangChain | LLM application framework |
| Groq API | Model inference |
| GPT-OSS 20B | Large Language Model |
| DuckDuckGo | Web search |
| Wikipedia API | Knowledge retrieval |
| Arxiv | Academic research search |

## 🏗️ Project Architecture

```text
User Query
    |
    v
Streamlit Chat Interface
    |
    v
Groq GPT-OSS 20B
    |
    v
LangChain Tool-Calling Agent
    |
    +-------------------+
    |                   |
    v                   v
DuckDuckGo          Wikipedia
    |
    v
Arxiv Research Search
    |
    v
Retrieved Information
    |
    v
LLM Response Generation
    |
    v
Final Answer to User
```

## 📂 Project Structure

```text
AI-Research-Search-Engine/
│
├── app.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/ai-research-search-engine.git
```

### 2. Navigate to the project directory

```bash
cd ai-research-search-engine
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure API key

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key
```

Get your API key from:

[Groq Console](https://console.groq.com/)

### 7. Run the application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

## 🔎 Available Search Tools

### 1. DuckDuckGo Search
Searches the internet for websites, general information, and current topics.

### 2. Wikipedia Search
Retrieves introductory information about knowledge topics, history, science, and technology.

### 3. Arxiv Research Search
Searches academic publications and scientific research papers, including Artificial Intelligence and Machine Learning.

## 🧠 How It Works

1. The user submits a question through the Streamlit interface.
2. GPT-OSS 20B processes the query.
3. The LangChain agent decides whether external information is required.
4. The agent selects an appropriate search tool.
5. The selected tool retrieves relevant information.
6. The LLM generates a response using the retrieved information.
7. The final answer appears in the chat interface.

## 🚀 Future Enhancements

- Implement Retrieval-Augmented Generation (RAG).
- Add persistent chat history using a database.
- Integrate additional search engines and APIs.
- Display clickable source links and citations.
- Implement multi-agent workflows using LangGraph.
- Deploy the application to a cloud platform.

## 🔐 Security

- Store API keys in environment variables.
- Never commit `.env` or virtual environment folders.
- Keep API credentials private.

## 🤝 Contributing

Contributions and suggestions are welcome!

1. Fork this repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a Pull Request.

---

**Built with ❤️ using Python, LangChain, Groq and Streamlit.**
