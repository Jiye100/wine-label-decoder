import os
import easyocr
import pandas as pd
import fuzzy_match
import decision_tree
import streamlit as st
from PIL import Image
from tqdm import tqdm
import joblib
import numpy as np

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
    return joblib.load('models/decision_tree_model.pkl')

# ========================
# 📂 Batch Processing Logic
# ========================

def ocr_on_batch_of_images(uploaded_files):
    """Runs OCR on a batch of uploaded images."""
    reader = load_reader()
    results = {}

    for file in tqdm(uploaded_files, desc="Extracting text from OCR images"):
        image = Image.open(file)
        result = reader.readtext(np.array(image))
        results[file.name] = [text[1] for text in result]
    
    return results

def extract_and_predict(results):
    """Extracts information and predicts labeling laws for each image."""
    final_results = []

    for filename, texts in results.items():
        # Extract information
        grape, region, country, keyword = fuzzy_match.extract_info(texts)
        designation = determine_designation(region, country)

        # Prepare DataFrame
        test_label = pd.DataFrame({
            'grape': [grape], 
            'region': [region], 
            'country': [country], 
            'designation': [designation]
        })

        # Predict using decision tree
        grape_law, region_law, vintage_law = decision_tree.predict_law(test_label)
        grape_law, region_law, vintage_law = grape_law * 100, region_law * 100, vintage_law * 100

        # Store the result
        final_results.append({
            "File": filename,
            "Grape": grape,
            "Region": region,
            "Country": country,
            "Designation": designation,
            "Grape Law": f"{grape_law}%",
            "Region Law": f"{region_law}%",
            "Vintage Law": f"{vintage_law}%"
        })
    
    return final_results

def determine_designation(region, country):
    """Determines the wine designation based on region and country."""
    designation = ""
    if not region:
        region = country

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

    return designation

# ========================
# 🖥️ Streamlit UI
# ========================
st.set_page_config(page_title="Batch Wine Label Processing", page_icon="🍷", layout="wide")

st.title("🍷 Wine Label Batch Processor")

# ========== Sidebar Options ==========
st.sidebar.header("Batch Processing Configuration")
pytesseract_path = st.sidebar.text_input("Pytesseract Path (Optional):")

# ========== Upload Files ==========
uploaded_files = st.file_uploader("Upload Multiple Wine Label Images", accept_multiple_files=True, type=["png", "jpg", "jpeg"])

# ========== Run OCR and Prediction ==========
if uploaded_files:
    if st.button("Run Batch OCR"):
        with st.spinner("Processing images..."):
            results = ocr_on_batch_of_images(uploaded_files)
            final_results = extract_and_predict(results)
            st.success("Batch Processing Complete!")

# ========== Display Results ==========
if 'final_results' in locals():
    st.subheader("Batch Processing Results")
    for result in final_results:
        st.markdown(f"**{result['File']}**")
        st.write(f"**Grape:** {result['Grape']}")
        st.write(f"**Region:** {result['Region']}")
        st.write(f"**Country:** {result['Country']}")
        st.write(f"**Designation:** {result['Designation']}")
        st.write(f"🍇 **Grape Law:** {result['Grape Law']}")
        st.write(f"📍 **Region Law:** {result['Region Law']}")
        st.write(f"🗓️ **Vintage Law:** {result['Vintage Law']}")
        st.markdown("---")
