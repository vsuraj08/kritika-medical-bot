from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load the Gemini model and get a response
def get_medical_response(text_input, image_data, context):
    try:
        # Configure the GenerativeModel
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Construct the inputs
        inputs = [text_input, context]
        if image_data:
            inputs.insert(1, image_data)
        
        # Generate content
        response = model.generate_content(inputs)
        
        # Validate and return the response
        if response and hasattr(response, 'text'):
            return response.text
        else:
            return "The model could not generate a valid response. Please try again."
    except Exception as e:
        return f"Error in generating response: {e}"

# Function to process uploaded image
def process_uploaded_image(uploaded_file):
    if uploaded_file:
        bytes_data = uploaded_file.getvalue()
        return {
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }
    return None

# Streamlit app configuration
st.set_page_config(page_title="Medical Chatbot", layout="centered")
st.title("Medical Chatbot")
st.write("Upload medical images or enter text queries for analysis.")

# Input sections
text_query = st.text_input("Enter your query here:")
uploaded_image = st.file_uploader("Upload a medical image (e.g., X-ray, MRI, prescription)", type=["jpg", "jpeg", "png"])
submit_button = st.button("Analyze")

# Display uploaded image
if uploaded_image:
    st.image(Image.open(uploaded_image), caption="Uploaded Image", use_column_width=True)

# Predefined context for medical analysis
medical_context = """
You are a highly advanced medical chatbot specializing in analyzing text inputs and medical images such as prescriptions, medical reports, and X-rays.
- For text inputs, provide detailed, efficient, and accurate medical advice, including how the condition can be treated and a recommended diet plan.
- For images, analyze the content and provide relevant medical insights. Always include a diet plan for any condition diagnosed.
- If the query is not related to medical topics, respond with: "I'm a medical assistant and can only help with medical-related queries."
"""

# Process user input upon submission
if submit_button:
    image_data = process_uploaded_image(uploaded_image)
    response = get_medical_response(text_query, image_data, medical_context)
    
    st.subheader("Response:")
    st.write(response)
