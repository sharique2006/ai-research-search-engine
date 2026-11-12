
import os
import requests
import streamlit as st

from dotenv import load_dotenv

from langchain_groq import ChatGroq

from langchain.tools import Tool

from langchain_community.utilities import ArxivAPIWrapper
from langchain_community.tools import ArxivQueryRun, DuckDuckGoSearchRun

from langchain.agents import AgentExecutor, create_tool_calling_agent

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage


# ==================================================
# 1. CONFIGURATION
# ==================================================

load_dotenv()

st.set_page_config(
    page_title="AI Research Search Engine",
    page_icon="🔍",
    layout="wide"
)


# ==================================================
# 2. CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.stApp {
    background-color: #0b1120;
    color: #f8fafc;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 7rem;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #263244;
}

section[data-testid="stSidebar"] * {
    color: #e5e7eb;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    text-align: center;
    color: #60a5fa;
    margin-bottom: 8px;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 16px;
    margin-bottom: 35px;
}

[data-testid="stChatMessage"] {
    background: #172235;
    border: 1px solid #29384d;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 16px;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3 {
    color: #f1f5f9 !important;
    line-height: 1.7;
}

[data-testid="stChatMessage"] pre {
    background: #0f172a !important;
    border: 1px solid #334155;
    border-radius: 10px;
}

[data-testid="stChatInput"] {
    background: #111827 !important;
    border: 1px solid #475569 !important;
    border-radius: 16px !important;
    padding: 5px !important;
}

[data-testid="stChatInput"] textarea {
    background: #1e293b !important;
    color: #ffffff !important;
    caret-color: #60a5fa !important;
    font-size: 16px !important;
    border: none !important;
    -webkit-text-fill-color: #ffffff !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #cbd5e1 !important;
    opacity: 1 !important;
    -webkit-text-fill-color: #cbd5e1 !important;
}

[data-testid="stChatInput"]:focus-within {
    border: 1px solid #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15);
}

[data-testid="stSidebar"] input {
    background: #1e293b !important;
    color: #ffffff !important;
}

.stButton > button {
    background: #2563eb;
    color: white !important;
    border: none;
    border-radius: 10px;
    font-weight: 600;
}

.stButton > button:hover {
    background: #1d4ed8;
    color: white !important;
}

hr {
    border-color: #334155;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# 3. HEADER
# ==================================================

st.markdown(
    '<div class="main-title">🔍 AI Research Search Engine</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your intelligent assistant for web search, '
    'Wikipedia and academic research.'
    '</div>',
    unsafe_allow_html=True
)


# ==================================================
# 4. SIDEBAR
# ==================================================

with st.sidebar:

    st.title("⚙️ Settings")

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        value=os.getenv("GROQ_API_KEY", ""),
        placeholder="Enter your Groq API key"
    )

    model_name = "openai/gpt-oss-20b"

    st.selectbox(
        "Selected AI Model",
        [model_name],
        index=0
    )

    st.caption("Powered by Groq API")

    st.divider()

    st.subheader("🛠️ Available Tools")

    st.markdown("""
    🌐 **DuckDuckGo Search**

    📚 **Wikipedia Search**

    📄 **Arxiv Research Papers**
    """)

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("AI Research Search Engine")


# ==================================================
# 5. CHAT HISTORY
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==================================================
# 6. WIKIPEDIA SEARCH FUNCTION
# ==================================================

def search_wikipedia(query):

    search_url = "https://en.wikipedia.org/w/api.php"

    headers = {
        "User-Agent": "AIResearchSearchEngine/1.0 (educational project)"
    }

    try:

        # First request: Search Wikipedia pages
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": 3,
            "format": "json"
        }

        search_response = requests.get(
            search_url,
            params=search_params,
            headers=headers,
            timeout=(5, 10)
        )

        search_response.raise_for_status()

        search_data = search_response.json()

        results = search_data.get(
            "query", {}
        ).get("search", [])

        if not results:
            return "No matching Wikipedia articles found."

        # Second request: Get article extracts
        page_ids = "|".join(
            str(item["pageid"]) for item in results
        )

        extract_params = {
            "action": "query",
            "pageids": page_ids,
            "prop": "extracts",
            "explaintext": 1,
            "exintro": 1,
            "format": "json"
        }

        extract_response = requests.get(
            search_url,
            params=extract_params,
            headers=headers,
            timeout=(5, 10)
        )

        extract_response.raise_for_status()

        extract_data = extract_response.json()

        pages = extract_data.get(
            "query", {}
        ).get("pages", {})

        output = []

        for page in pages.values():

            title = page.get("title", "Unknown")
            extract = page.get("extract", "")

            if extract:

                output.append(
                    f"Title: {title}\n"
                    f"Information: {extract[:2500]}"
                )

        if not output:
            return "Wikipedia did not return article content."

        return "\n\n".join(output)

    except requests.exceptions.Timeout:

        return (
            "Wikipedia connection timed out. "
            "Try DuckDuckGo Search for this question."
        )

    except requests.exceptions.ConnectionError:

        return (
            "Could not connect to Wikipedia. "
            "Please check your internet connection "
            "or use DuckDuckGo Search."
        )

    except requests.exceptions.HTTPError as error:

        return f"Wikipedia HTTP error: {error}"

    except ValueError:

        return "Wikipedia returned an invalid response."

    except Exception as error:

        return f"Wikipedia search failed: {str(error)}"


# ==================================================
# 7. CREATE SEARCH TOOLS
# ==================================================

@st.cache_resource
def create_tools():

    # Wikipedia
    wikipedia_tool = Tool(
        name="Wikipedia",
        func=search_wikipedia,
        description=(
            "Search Wikipedia for general knowledge, "
            "science, history, people, places and concepts. "
            "Input should be a clear search query."
        )
    )

    # Arxiv
    arxiv_wrapper = ArxivAPIWrapper(
        top_k_results=3,
        doc_content_chars_max=3000
    )

    arxiv_tool = ArxivQueryRun(
        api_wrapper=arxiv_wrapper,
        name="Arxiv",
        description=(
            "Search academic research papers, "
            "Artificial Intelligence, Machine Learning "
            "and scientific publications."
        )
    )

    # DuckDuckGo
    duckduckgo_tool = DuckDuckGoSearchRun()

    duckduckgo_tool.name = "DuckDuckGo"

    duckduckgo_tool.description = (
        "Search the internet for websites, recent information, "
        "news and general queries."
    )

    return [
        wikipedia_tool,
        arxiv_tool,
        duckduckgo_tool
    ]


# ==================================================
# 8. CREATE AI AGENT
# ==================================================

def create_search_agent(api_key):

    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="openai/gpt-oss-20b",
        temperature=0
    )

    tools = create_tools()

    prompt = ChatPromptTemplate.from_messages([

        (
            "system",
            """
            You are an intelligent AI Research Assistant.

            You can use these tools:

            1. Wikipedia:
               Search general knowledge and explanations.

            2. DuckDuckGo:
               Search the internet for current information.

            3. Arxiv:
               Search scientific and academic research papers.

            INSTRUCTIONS:

            - Respond directly to greetings.
            - Do not use tools unnecessarily.
            - Use Wikipedia for general knowledge.
            - Use DuckDuckGo for web searches and recent information.
            - Use Arxiv for research paper questions.
            - Never invent search results.
            - If one tool fails, try another relevant tool.
            - Explain results in simple and clear language.
            - Use headings and bullet points when appropriate.
            - Maintain conversation context.
            """
        ),

        MessagesPlaceholder(
            variable_name="chat_history",
            optional=True
        ),

        ("human", "{input}"),

        MessagesPlaceholder(
            variable_name="agent_scratchpad"
        )

    ])

    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        max_iterations=5,
        handle_parsing_errors=True
    )

    return executor


# ==================================================
# 9. DISPLAY PREVIOUS MESSAGES
# ==================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ==================================================
# 10. CHAT INPUT
# ==================================================

user_prompt = st.chat_input(
    "Message AI Research Assistant..."
)


# ==================================================
# 11. PROCESS USER QUERY
# ==================================================

if user_prompt:

    if not api_key:

        st.error("Please enter your Groq API key in the sidebar.")

        st.stop()

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_prompt
    })

    with st.chat_message("user"):
        st.markdown(user_prompt)

    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good evening",
        "good afternoon"
    ]

    # Direct greeting
    if user_prompt.lower().strip() in greetings:

        response = (
            "Hello! 👋 Welcome to AI Research Search Engine. "
            "How can I help you today?"
        )

        with st.chat_message("assistant"):
            st.markdown(response)

    else:

        with st.chat_message("assistant"):

            try:

                with st.spinner("🤖 AI is researching..."):

                    executor = create_search_agent(api_key)

                    # Build previous conversation
                    chat_history = []

                    for message in st.session_state.messages[:-1]:

                        if message["role"] == "user":

                            chat_history.append(
                                HumanMessage(
                                    content=message["content"]
                                )
                            )

                        elif message["role"] == "assistant":

                            chat_history.append(
                                AIMessage(
                                    content=message["content"]
                                )
                            )

                    # Execute agent
                    result = executor.invoke({
                        "input": user_prompt,
                        "chat_history": chat_history
                    })

                    response = result["output"]

                st.markdown(response)

            except Exception as error:

                response = (
                    "Something went wrong.\n\n"
                    f"Error details: `{str(error)}`"
                )

                st.error(response)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
