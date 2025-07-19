import streamlit as st
import google.generativeai as genai

# --- Page Configuration ---
st.set_page_config(page_title="Corporate Jargon Translator", page_icon="👔")

# --- API Key Configuration ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Error configuring API key: {e}", icon="🚨")
    st.warning("Please make sure you have set your GOOGLE_API_KEY in the app's secrets.", icon="🔑")
    st.stop()

# --- The "Magic Prompt" ---
TRANSLATOR_PROMPT = """
You are the "Corporate Jargon Translator," an expert AI with a witty, blunt, and slightly cynical personality.
Your sole purpose is to translate vague, buzzword-filled corporate-speak into simple, clear, and direct English.
You must expose the underlying meaning behind the jargon. Do not be afraid to be a little humorous.

Here is an example:

Jargon: "We need to leverage our cross-functional synergies to action a paradigm shift in our value-added content creation pipeline."
Translation: "We need to get our different teams to work together to completely change how we make things for our customers."

Now, translate the following jargon:
"""

# --- AI Translation Function ---
def translate_jargon(jargon_text: str):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        # THIS IS THE CORRECTED LINE:
        full_prompt = f'{TRANSLATOR_PROMPT}\nJargon: "{jargon_text}"\nTranslation:'
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        return f"An error occurred with the AI model. Details: {e}"

# --- Streamlit App Interface ---
st.title("👔 Corporate Jargon Translator")
st.write("Tired of buzzwords and synergistic nonsense? Paste the corporate-speak below and get a translation you can actually understand.")

jargon_input = st.text_area("Enter Jargon Here:", height=150, placeholder="e.g., Let's circle back on that offline...")

if st.button("Translate", type="primary"):
    if jargon_input:
        with st.spinner("Decoding the nonsense..."):
            translation = translate_jargon(jargon_input)
            st.subheader("Here's what that actually means:")
            st.markdown(f"> {translation}")
    else:
        st.warning("Please enter some jargon to translate.")

st.markdown("---")
st.write("Built with ❤️, Python, and a touch of cynicism.")
