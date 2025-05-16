# Home.py
import streamlit as st
from menu import menu

# Set up the main app page
st.title("🍷 Wine Label Decoder")
st.write("Welcome to the Wine Label Decoder application!")

# Display main content
st.image("15_bottles_red_1.png")
st.markdown("""
### Select a page from the sidebar to get started!
- **Wine Reader**: Upload and extract wine label information.
- **Wine Information**: Learn about flavor profiles for different grapes.
- **Read Multiple Images**: Upload multiple images to be read!
""")



st.markdown("""
<style>
.footnote {
    font-size: 0.8em;
    color: gray;
    margin-top: -10px;
}
</style>
<p class="footnote">
    Image courtesy of <a href="https://wineonsale.com/products/15-bottles-of-award-winning-red-wine-for-winter-750-ml" target="_blank">
    Wine on Sale</a>.
</p>
""", unsafe_allow_html=True)
