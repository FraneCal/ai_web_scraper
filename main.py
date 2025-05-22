import streamlit as st
from urllib.parse import urlparse

from scrape import (
    scrape_website,
    split_dom_content,
    clean_body_content,
    extract_body_content
)
from parse import parse_with_deepseek

st.set_page_config(page_title="AI Web Scraper", layout="wide")
st.title("🕸️ AI Web Scraper with DeepSeek")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "dom_content" not in st.session_state:
    st.session_state.dom_content = ""

# Function to validate URL format
def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return all([parsed.scheme in ["http", "https"], parsed.netloc])
    except:
        return False

# URL input and scraping
url = st.text_input("Enter a website URL:")

if st.button("Scrape Site"):
    if not url:
        st.warning("Please enter a URL before scraping.")
    elif not is_valid_url(url):
        st.error("Invalid URL format. Please enter a valid URL (e.g., https://example.com).")
    else:
        st.write("🔍 Scraping the website...")
        result = scrape_website(url)
        body_content = extract_body_content(result)
        cleaned_content = clean_body_content(body_content)
        st.session_state.dom_content = cleaned_content

        with st.expander("📄 View DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=300)

# Parsing section
if st.session_state.dom_content:
    parse_description = st.text_area("📝 Describe what you want to parse:")

    if st.button("Parse Content"):
        if parse_description:
            st.write("🧠 Parsing the content...")
            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_deepseek(dom_chunks, parse_description)
            st.session_state.chat_history.append({
                "prompt": parse_description,
                "response": result
            })
            st.write("✅ Result:")
            st.write(result)
        else:
            st.warning("Please describe what you want to parse.")

# Optional: Display chat history
with st.expander("🗂️ Show Chat History"):
    if st.session_state.chat_history:
        for i, entry in enumerate(st.session_state.chat_history, 1):
            st.markdown(f"**{i}. Prompt:** {entry['prompt']}")
            st.markdown(f"**Response:** {entry['response']}")
            st.markdown("---")
    else:
        st.write("No chat history yet.")
