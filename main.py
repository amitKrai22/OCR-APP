import streamlit as st
from PIL import Image
import io
import base64
import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to extract text using Gemini
def extract_text_with_gemini(image_bytes):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content([
        "Analyze the text in the provided image. Extract all readable content "
        "and present it in a structured Markdown format that is clear, concise, "
        "and well-organized. Ensure proper formatting (e.g., headings, lists, or "
        "code blocks) as necessary to represent the content effectively.",
        image
    ])
    return response.text

# Page configuration
st.set_page_config(
    page_title="Gemini Flash OCR",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description in main area
logo_path = "./assets/gemma3.jpeg"  # Replace with your Gemini Flash logo
if os.path.exists(logo_path):
    logo_base64 = base64.b64encode(open(logo_path, "rb").read()).decode()
    st.markdown(f"""
        # <img src="data:image/png;base64,{logo_base64}" width="60" height= "50" style="vertical-align: -12px; border-radius: 12px;"> Gemini Flash OCR
    """, unsafe_allow_html=True)
else:
    st.markdown("# Gemini Flash OCR")

# Add clear button
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("Clear 🗑️"):
        if 'ocr_result' in st.session_state:
            del st.session_state['ocr_result']
        st.rerun()

st.markdown('<p style="margin-top: -20px;">Extract structured text from images using Gemini Flash 2.0!</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar for uploading image
with st.sidebar:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")

        if st.button("Extract Text 🔍", type="primary"):
            with st.spinner("Processing image..."):
                try:
                    image = Image.open(uploaded_file)  # This returns a PIL.Image.Image
                    result_text = extract_text_with_gemini(image)

                    st.session_state['ocr_result'] = result_text
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")

# Main content area for results
if 'ocr_result' in st.session_state:
    st.markdown(st.session_state['ocr_result'])
else:
    st.info("Upload an image and click 'Extract Text' to see the results here.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Gemini Flash Vision Model")
