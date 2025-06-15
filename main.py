# --- Configuration ---
import streamlit as st
import traceback
import os
import tempfile
import mimetypes
import my_agents  # Import your agent modules
import re
import time
from io import BytesIO

# Optional dotenv loading for local development
if os.getenv("LOCAL_DEV"):
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

# Get secrets from st.secrets or fallback to os.environ
novita_key = st.secrets.get("NOVITA_API_KEY", os.getenv("NOVITA_API_KEY"))
gemini_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="AI README Generator", layout="wide")

st.markdown("""
    <style>
    .main {background-color: #f5f7fa;}
    .stButton>button {background-color: #4F8BF9; color: white; border-radius: 8px;}
    .stMarkdown {font-size: 1.1em;}
    </style>
""", unsafe_allow_html=True)

st.title("📄 AI README Generator")

tone = st.sidebar.selectbox("Select README Tone/Style", ["Professional", "Friendly", "Minimal"])
project_name = st.text_input("Enter your project name:", value="My Project")

uploaded_files = st.file_uploader(
    "Upload one or more files or a zipped folder:",
    type=None,
    accept_multiple_files=True,
    key="file_uploader_main"
)

all_files = []
analysis = {}

def process_files(all_files, analysis, tone, project_name):
    summaries = {}

    for file_path in all_files:
        safe_file_path = os.path.normpath(file_path)
        mime_type, _ = mimetypes.guess_type(safe_file_path)
        if mime_type and (mime_type.startswith('text/') or safe_file_path.endswith(('.py', '.md', '.txt'))):
            try:
                with open(safe_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                analysis[safe_file_path] = {
                    'code_content': content,
                    'code_analysis': my_agents.code_parser.analyze_file(safe_file_path, content)
                }
            except UnicodeDecodeError:
                analysis[safe_file_path] = {'type': 'binary', 'size': os.path.getsize(safe_file_path)}
            except Exception as e:
                analysis[safe_file_path] = {'type': 'error', 'message': str(e)}
                st.error(f"Error reading file: {safe_file_path}")
                st.code(traceback.format_exc())
        else:
            pass

    st.info("Generating README... This may take a moment depending on the number and size of files.")
    with st.spinner("Processing..."):
        time.sleep(2)

    if analysis:
        summarizer_input = {
            fname: {'code': info['code_content']}
            for fname, info in analysis.items() if 'code_content' in info
        }

        if summarizer_input:
            summaries = my_agents.summarizer.summarize_files(summarizer_input, tone=tone)
            for fname, summary_text in summaries.items():
                if fname in analysis:
                    analysis[fname]['summary'] = summary_text

        st.subheader("Analyzed Files")
        for file_path, info in analysis.items():
            if 'code_content' in info:
                st.markdown(f"📄 `{os.path.basename(file_path)}`")

        progress = st.progress(0, text="Analyzing code...")
        progress.progress(33, text="Summarizing...")
        time.sleep(1)
        progress.progress(66, text="Formatting README...")

        formatted_text, _, _ = my_agents.formatter.format_readme(
            analysis, summaries, project_name=project_name, tone=tone
        )

        progress.progress(100, text="Done!")
        st.success("README generated!")

        st.subheader("README.md Preview")
        st.markdown(formatted_text)

        # Store in session_state for edit/download section
        st.session_state["generated_readme"] = True
        st.session_state["final_readme"] = formatted_text


# --- File Handling Logic ---
if uploaded_files:
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            for file in uploaded_files:
                file_path = os.path.join(temp_dir, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.read())
                all_files.append(file_path)

            if st.button("Generate README", key="generate_readme_btn_upload"):
                process_files(all_files, analysis, tone, project_name)

        except Exception as e:
            st.error(f"Failed to process uploaded files: {str(e)}")
            st.code(traceback.format_exc())

# --- Persistent Editable Area and Download ---
if st.session_state.get("generated_readme"):
    st.subheader("✏️ Edit Final README.md")
    default_text = st.session_state.get("final_readme", "")

    edited_readme = st.text_area("Make changes to your README here:", value=default_text, height=500, key="readme_editor")
    st.session_state["final_readme"] = edited_readme

    st.download_button(
        label="📥 Download README.md",
        data=BytesIO(edited_readme.encode("utf-8")),
        file_name="README.md",
        mime="text/markdown",
        key="download_btn"
    )
