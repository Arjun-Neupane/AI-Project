import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY not found in .env file.")
    st.stop()

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.6-flash"


st.set_page_config(
    page_title="Email-to-Task Generator",
    page_icon=""
)

st.title("Email-to-Task Generator")

st.write(
    "Paste an email and AI will extract actionable "
    "tasks, deadlines, priorities, and responsible people."
)


email = st.text_area(
    "Paste Email",
    height=250,
    placeholder="""Place email here"""
)


def extract_tasks(email_text):

    prompt = f"""
You are an intelligent email task extraction assistant.

Analyze the following email and identify all actionable tasks.

EMAIL:
{email_text}

For every task, extract:

1. Task
2. Responsible person
3. Deadline
4. Reason/context

If information is not available, write "Not specified".

Return the result in Markdown table format.

Use this format:

| Task | Person | Deadline | Context |
|------|--------|----------|---------|

Do not invent information.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text


if st.button(
    "Extract Tasks",
    type="primary",
    use_container_width=True
):

    if not email.strip():

        st.warning(
            "Please paste an email first."
        )

    else:

        with st.spinner(
            "Analyzing email..."
        ):

            try:

                result = extract_tasks(
                    email
                )

                st.session_state["result"] = result

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )


if "result" in st.session_state:

    st.divider()

    st.subheader(
        " Extracted Tasks"
    )

    st.markdown(
        st.session_state["result"]
    )


if st.button(" Clear"):

    if "result" in st.session_state:
        del st.session_state["result"]

    st.rerun()



st.divider()

st.caption(
    "Email-to-Task Generator"
)
