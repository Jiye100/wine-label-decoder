import os
import easyocr
import pandas as pd
import fuzzy_match
import decision_tree
import streamlit as st
from PIL import Image
import numpy as np
import torch
from io import BytesIO

# ========================
# 🚀 Caching Expensive Operations
# ========================

@st.cache_resource
def load_reader():
    """Loads the EasyOCR reader (cached for efficiency)."""
    return easyocr.Reader(['en'])

@st.cache_resource
def load_model():
    """Loads the decision tree model (if needed)."""
    return decision_tree

def extract_information(image_array):
    """Runs OCR on the image and extracts relevant information."""
    reader = load_reader()
    result = reader.readtext(image_array)
    result = [text[1] for text in result]
    if len(result) == 0:
        return None, None, None, None, None
    grape, region, country, keyword = fuzzy_match.extract_info(result)
    return result, grape, region, country, keyword


def determine_designation(region, country):
    """Determines the wine designation based on region and country."""
    designation = ""
    if not region:
        region = country
        st.warning(f"No specific region found, using country '{country}' as the region.")

    if country in fuzzy_match.state:
        if region:
            designation = "AVA"
        else:
            designation = "Country"
    else:
        if not region:
            region = country
            designation = "Country" if country in ["argentina", "chile", "south africa"] else "Unknown"
        else:
            if region in fuzzy_match.country_to_region['chile']:
                designation = "DO"
            elif region in fuzzy_match.country_to_region['argentina']:
                designation = "DOC" if region in ["luján de cuyo", "san rafael"] else "IG"
            elif region in fuzzy_match.country_to_region['south africa']:
                designation = "WO"

    if not designation or designation == 'Unknown':
        designation = "Country" if country in ["argentina", "chile", "south africa", "australia", "new zealand"] else "Unknown"

    return region, designation

def predict_labeling_laws(grape, region, country, designation):
    """Runs decision tree prediction and displays results."""
    test_label = pd.DataFrame({
        'grape': [grape], 
        'region': [region], 
        'country': [country], 
        'designation': [designation]
    })
    
    model = load_model()
    grape_law, region_law, vintage_law = model.predict_law(test_label)
    grape_law, region_law, vintage_law = grape_law * 100, region_law * 100, vintage_law * 100

    return grape_law, region_law, vintage_law

# ========================
# 🖥️ Streamlit UI
# ========================

st.title("🍷 Wine Label Decoder")

# Initialize Session State
if 'parsed_data' not in st.session_state:
    st.session_state.parsed_data = None
if 'last_uploaded' not in st.session_state:
    st.session_state.last_uploaded = None
if 'image_data' not in st.session_state:
    st.session_state.image_data = None

# File uploader
uploaded_file = st.file_uploader("Upload a wine label image", type=["png", "jpg", "jpeg"])

# Check if the uploaded file is new
new_image = uploaded_file is not None and uploaded_file != st.session_state.last_uploaded

if new_image:
    # Save the image in memory (to survive reruns)
    st.session_state.last_uploaded = uploaded_file
    image = Image.open(uploaded_file)
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    st.session_state.image_data = img_byte_arr.getvalue()
    
    # === Invalidate the cache ===
    st.session_state.parsed_data = None  

# --- Display Image if Available ---
if st.session_state.image_data:
    # Reconstruct the image from bytes
    image = Image.open(BytesIO(st.session_state.image_data))
    st.image(image, caption="Uploaded Wine Label", use_container_width=True)

    if st.session_state.parsed_data is None:
        # Only parse the image if it's not cached
        image_array = np.array(image)
        
        # Attempt to extract information
        result, grape, region, country, keyword = extract_information(image_array)
        
        # If extraction failed, warn and do not proceed
        if not grape or not region or not country:
            st.warning("Could not extract valid wine information. Please try a different image.")
            st.session_state.parsed_data = None
            st.stop()
        
        # Otherwise, continue with processing
        region, designation = determine_designation(region, country)
        st.session_state.parsed_data = (result, grape, region, country, keyword, designation)

# Display if parsed data is available
if st.session_state.parsed_data:
    result, grape, region, country, keyword, designation = st.session_state.parsed_data

    st.subheader("Wine Information")
    st.write(f"**Grape Variety:** {grape.title()}")
    st.write(f"**Region:** {region.title()}")
    st.write(f"**Country/State:** {country.title()}")
    st.write(f"**Designation:** {designation}")
    
    if keyword:
        st.write(f"**Keywords Detected:** {keyword}")

    # Run prediction
    grape_law, region_law, vintage_law = predict_labeling_laws(grape, region, country, designation)

    st.success("Labeling Law Requirements:")
    st.write(f"🍇 **{grape_law}%** of the grapes must be **{grape.title()}**")
    st.write(f"📍 **{region_law}%** of the grapes must come from **{region.title()}**")
    st.write(f"🗓️ **{vintage_law}%** of the grapes must be from the stated vintage")

    # --- Only show extracted text when checkbox is checked ---
    if st.checkbox('Feeling nerdy?', key='nerdy_checkbox'):
        st.subheader("Extracted Text")
        st.write(result)
