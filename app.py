# app.py
import streamlit as st
import groq

# Page Configuration
st.set_page_config(
    page_title="AI Email Generator",
    page_icon="✉️",
    layout="centered"
)

# Initialize Session State
if "generated_email" not in st.session_state:
    st.session_state.generated_email = ""

# Security & API Key Validation
if "GROQ_API_KEY" not in st.secrets:
    st.error("⚠️ `GROQ_API_KEY` is missing from Streamlit Secrets. Please configure it to use this application.")
    st.stop()

try:
    client = groq.Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("❌ Failed to initialize the Groq client. Please check your API key configuration.")
    st.stop()

# Header Section
st.title("✉️ AI Email Generator")
st.markdown("Generate professional, personalized emails with AI.")
st.divider()

# Two-Column Layout for Inputs
col1, col2 = st.columns(2, gap="medium")

with col1:
    st.subheader("📋 Email Details")
    
    purpose = st.selectbox(
        "Email Purpose",
        [
            "Job Application",
            "Meeting Request",
            "Leave Request",
            "Thank You",
            "Complaint",
            "Follow Up",
            "Project Update",
            "Invitation",
            "Request for Information",
            "Apology",
            "Other"
        ]
    )
    
    recipient = st.text_input(
        "Recipient",
        placeholder="e.g. University Supervisor"
    )
    
    tone = st.selectbox(
        "Tone",
        [
            "Professional",
            "Formal",
            "Friendly",
            "Casual",
            "Persuasive",
            "Apologetic"
        ]
    )

with col2:
    st.subheader("⚙️ Preferences")
    
    language = st.selectbox(
        "Language",
        [
            "English",
            "Urdu",
            "Roman Urdu"
        ]
    )
    
    length = st.selectbox(
        "Email Length",
        [
            "Short",
            "Medium",
            "Long"
        ]
    )
    
    context = st.text_area(
        "What do you want to say?",
        placeholder="Describe your situation or what you want to communicate...",
        height=125
    )

st.divider()

# Generation Action Button
if st.button("✨ Generate Email", type="primary", use_container_width=True):
    if not context.strip():
        st.warning("⚠️ Please provide context or a description of what you want to communicate.")
    else:
        with st.spinner("Drafting your email..."):
            try:
                system_prompt = (
                    "You are an expert professional email writing assistant. "
                    "Your task is to generate complete, high-quality, and relevant emails "
                    "following the exact formatting, language, tone, and length requested."
                )
                
                user_prompt = f"""
Please generate an email based on the following specifications:
- Email Purpose: {purpose}
- Recipient: {recipient if recipient else "Recipient"}
- Tone: {tone}
- Language: {language}
- Email Length: {length}
- Additional Context: {context}

Follow these strict instructions:
1. Understand the user's intent.
2. Generate an appropriate email subject.
3. Generate a complete email body with a suitable greeting and professional closing.
4. Keep the text natural, human-like, and relevant to the context.
5. Do not invent sensitive private facts; use sensible placeholders if necessary.
6. Return ONLY the generated email in the exact format shown below, without any extra commentary, explanation, or conversational filler.

OUTPUT FORMAT:
SUBJECT:
<generated subject>

BODY:
<generated email body>
"""

                chat_completion = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                )
                
                response_content = chat_completion.choices[0].message.content
                st.session_state.generated_email = response_content
                
            except Exception as e:
                st.error(f"❌ An error occurred while generating the email: {e}")

# Result Section
if st.session_state.generated_email:
    st.divider()
    st.subheader("📨 Generated Email")
    
    # Editable text area maintaining state
    edited_email = st.text_area(
        "You can edit your generated email below:",
        value=st.session_state.generated_email,
        height=300
    )
    st.session_state.generated_email = edited_email
    
    # Action buttons for result
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.download_button(
            label="📥 Download Email",
            data=st.session_state.generated_email,
            file_name="generated_email.txt",
            mime="text/plain",
            use_container_width=True
        )
        
    with res_col2:
        if st.button("🗑️ Clear Email", use_container_width=True):
            st.session_state.generated_email = ""
            st.rerun()
