# Wine Information Display Page
import streamlit as st

# Set page configuration
st.set_page_config(page_title="Wine Information", page_icon="🍇")

# Title
st.title("🍷 Wine Information")
st.write("Explore different wine varieties and their flavor profiles, beautifully organized by type.")

# --- White Wine Section ---
st.header("🍏 White Wines")
st.markdown("""
**Chardonnay** — Apple, pear, pineapple, citrus, figs, melon.  
*When aged*: peach, pineapple, sage, honey, caramel.  

**Sauvignon Blanc (NZ)** — Gooseberry, guava, passion fruit, jalapeño.  
**Sauvignon Blanc (AUS)** — Kiwi, pineapple, gooseberry, passionfruit, herbs.  
            
**Chenin Blanc** — Fruit, melon, peach, apple, citrus, tropical fruit.  
*When aged*: honey, apricot, quince.  

**Semillon** — Crisp, zesty, nutty, honey, straw.  
            
**Riesling** — Citrus, apple, honey (young), aged honeyed.  
            
**German Riesling** — Apricot, peach, green apple, floral, lemon, tropical (botrytised – honey). 
             
**Gruner Vetliner** — White pepper, stone fruits, lime, spicy.  
            
**Silvaner** — Peach, passion fruit, orange blossom.  
            
**Pinot Blanc (Weissburgunder)** — Apple, pears, mineral, lemon.  
            
**Pinot Gris** — Mango, melon, apple, honey.  
            
**Melon de Bourgogne (Muscadet)** — Tart lemon, green apple, pear, salinity. 
             
**Muscat** — White flowers, grape.  
            
**Gewurztraminer** — Flowers, spices, exotic fruits, acacia, peppermint, clove, cinnamon, ginger, grapefruit, litchi, mango, pineapple, pear, quince, honeysuckle.
""")

# --- Red Wine Section ---
st.header("🍒 Red Wines")
st.markdown("""
**Pinot Noir** — Cherry, raspberry, strawberry, cola, pomegranate, mushrooms, earth, bacon, meat/game, baking spices, purple and red flowers.  

**Gamay** — Cherry, strawberry, banana, kiwi, bubble gum (if carbonic maceration).  
            
**Grenache/Garnacha** — Blackberry, currant, cinnamon, spice, strawberry.  
            
**Syrah/Shiraz** — Cherry, black pepper, spice, olives, chocolate.  
            
**Tempranillo** — Cherry, plum, leather, tobacco, vanilla, coconut (from oak).  
            
**Pinotage** — Raspberry, blackberry, toasted marshmallow, cherry covered in blue cheese.  
            
**Malbec** — Ripe plum, prunes, blueberries, even raisins, sometimes mint.  
            
**Carmenere** — Plum, green peppercorn, herbal, blackcurrants (cassis), dark fruits, tea, herbaceous (green olives), bell pepper, spicy.  
            
**Zinfandel** — Blackberry, raspberry, jammy, briary, herbaceous, eucalyptus, mint, leather, cedar, dark chocolate, cherries, black pepper, raisins.  
            
**Cabernet Sauvignon** — Blackcurrants, dark fruits, tea, herbaceous, bell pepper, spicy, dried black plums. 
             
**Cabernet Franc** — Blackcurrants, dark fruits, violets, vegetal, bell pepper, spicy, raspberries.  
            
**Carignan** — Cherry, raspberry, licorice, earth.  
            
**Blaufrankisch (Lemberger)** — Cranberry, cherry, pomegranate, exotic spice, chocolate.  
            
**Zweigelt** — Cherry, spice, pepper, black raspberry.  
""")


# --- Footer ---
st.write("---")
st.write("Learn more about each grape variety and its unique tasting notes!")
