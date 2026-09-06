import os
import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="AI Email Generator", page_icon="✉️", layout="centered"
)

st.title("✉️ AI Email Generator")
st.markdown(
    "Generate professional, persuasive, or casual emails instantly using the"
    " Groq API."
)

# Initialize Groq client using Streamlit secrets
try:
  api_key = st.secrets["GROQ_API_KEY"]
  client = Groq(api_key=api_key)
except Exception as e:
  st.error(
      "Groq API key not found in Streamlit secrets. Please configure it."
  )
  st.stop()

# User Inputs Form
with st.form("email_form"):
  recipient_name = st.text_input("Recipient Name / Title", "Hiring Manager")
  email_topic = st.text_input(
      "Email Topic / Purpose",
      "Application for Software Engineering Intern Position",
  )
  tone = st.selectbox(
      "Select Tone", ["Professional", "Friendly", "Formal", "Persuasive", "Casual"]
  )
  key_points = st.text_area(
      "Key Points to Include",
      "- 3+ years experience in Python & AI\n- Built scalable REST APIs\n- Excited"
      " to contribute to your team",
  )

  submitted = st.form_submit_button("Generate Email", type="primary")

if submitted:
  if not email_topic.strip():
    st.warning("Please enter an email topic.")
  else:
    with st.spinner("Drafting your email..."):
      prompt = f"""
            Write a complete, ready-to-send email based on the following details:
            - Recipient: {recipient_name}
            - Topic/Purpose: {email_topic}
            - Tone: {tone}
            - Key Points to cover:
            {key_points}
            
            Include a compelling Subject Line followed by the Email Body.
            """

      try:
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert professional copywriter and"
                        " communication assistant skilled at crafting clear,"
                        " engaging emails."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        email_output = chat_completion.choices[0].message.content

        st.success("Email generated successfully!")
        st.subheader("Draft Result")
        st.code(email_output, language="markdown")

      except Exception as e:
        st.error(f"An error occurred while calling the Groq API: {e}")
