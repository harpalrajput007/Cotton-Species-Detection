import streamlit as st
from PIL import Image
import cv2
import numpy as np
from ultralytics import YOLO
import tempfile
import random
import base64

# Load YOLOv8 model
model = YOLO("last.pt")

# Page config
st.set_page_config(page_title="Cotton Species Detection", layout="centered", initial_sidebar_state="collapsed")

# Set background
def set_background(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

set_background("cotton_bg.jpg")

# Navbar
st.markdown("""
    <style>
        .navbar {
            background-color: #4caf50;
            padding: 1rem;
            text-align: center;
            border-radius: 10px;
            color: white;
            font-size: 28px;
            font-weight: bold;
            font-family: 'Segoe UI', sans-serif;
            margin-bottom: 20px;
        }
    </style>
    <div class="navbar">🌿 Cotton Species Detection for Farmers</div>
""", unsafe_allow_html=True)

# File uploader
st.markdown("""
    <style>
        section[data-testid="stFileUploader"] > div {
            background-color: #fff8e1 !important;
            border: 2px dashed #a5d6a7;
            padding: 1.5rem;
            border-radius: 15px;
            color: #1b5e20;
            font-weight: bold;
        }
        .uploadedFileName {
            color: #33691e;
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📤 Upload an Image", type=["jpg", "jpeg", "png"])

cotton_facts = [
    "Cotton is a natural fiber that grows on the seed of the cotton plant.",
    "There are over 50 species of cotton, but only four are commercially cultivated.",
    "India is one of the largest producers of cotton in the world.",
    "Cotton fibers are made of cellulose, a carbohydrate that gives them strength and durability.",
    "Cotton was domesticated independently in both the Old and New Worlds.",
    "The cotton gin, invented by Eli Whitney in 1793, revolutionized cotton processing.",
    "Cotton can absorb up to 27 times its weight in water.",
    "Cottonseed is used to make oil, animal feed, and even cosmetics.",
    "Egyptian cotton is known for its long fibers and luxurious feel.",
    "Cotton is biodegradable and recyclable, making it environmentally friendly.",
    "The word 'cotton' comes from the Arabic word 'qutn'.",
    "Cotton farming supports the livelihood of over 250 million people worldwide.",
    "Cotton is used in making textiles, medical supplies, and even currency paper.",
    "Denim jeans are traditionally made from cotton twill fabric.",
    "Cotton breathes well and is hypoallergenic, making it ideal for clothing.",
    "Cotton lint refers to the white fiber used to make fabric.",
    "Gossypium hirsutum accounts for about 90% of global cotton production.",
    "Cotton grows best in warm climates with adequate rainfall.",
    "Cotton bolls burst open when mature, revealing fluffy fibers.",
    "India, China, the USA, and Pakistan are top cotton producers.",
    "Cotton has been cultivated for over 7,000 years.",
    "Organic cotton is grown without synthetic chemicals or pesticides.",
    "Cotton is used in making bandages and gauze due to its absorbency.",
    "Cotton has high tensile strength, making it durable in fabrics.",
    "Mercerization is a process that improves the luster and dye affinity of cotton.",
    "Cotton is a renewable resource and can be grown annually.",
    "Cottonseed hulls are used as livestock feed.",
    "The largest consumers of cotton are China and India.",
    "Cotton fabrics are soft, strong, and breathable.",
    "Cotton flowers are typically white or yellow and bloom for a single day.",
]

# Function definitions
def show_crop_calendar(species_name):
    calendars = {
        "G-arboreum": {
            "January": ["Land preparation", "Soil health analysis"],
            "February": ["Start sowing in warmer zones"],
            "March": ["Seed treatment", "Sowing in central zones"],
            "April": ["Thinning", "First irrigation", "Weed removal"],
            "May": ["Fertilizer application", "Monitor early pests"],
            "June": ["Regular irrigation", "Spray bio-pesticides"],
            "July": ["Full vegetative growth", "Fertilizer top-up"],
            "August": ["Flowering begins", "Insect control"],
            "September": ["Boll formation", "Less irrigation"],
            "October": ["Harvesting begins", "Dry cotton properly"],
            "November": ["Final picking", "Field cleaning"],
            "December": ["Crop rotation prep", "Off-season planning"]
        },
        "G-herbaceum": {
            "January": ["Send soil for testing", "Prepare compost"],
            "February": ["Early sowing in southern India"],
            "March": ["Sowing in main belts", "Set up drip irrigation"],
            "April": ["Thin plants", "Apply bio-fertilizers"],
            "May": ["Check for weeds and pests", "Apply foliar spray"],
            "June": ["Boost with fertilizer", "Set up insect traps"],
            "July": ["Support vegetative phase", "Irrigate frequently"],
            "August": ["Monitor full bloom", "Apply potassium nitrate"],
            "September": ["Reduce irrigation", "Check for boll rot"],
            "October": ["Harvest mid-month", "Sort cotton"],
            "November": ["Clear fields", "Sell produce"],
            "December": ["Plough fields", "Plan next cycle"]
        },
        "G-hirsutum": {
            "January": ["Control pre-sowing weeds", "Plant green manure"],
            "February": ["Sow in Tamil Nadu/Andhra"],
            "March": ["Main season sowing", "Plan fertilizers"],
            "April": ["Start irrigation", "Control weeds"],
            "May": ["Monitor early insects"],
            "June": ["Apply top-dressing fertilizers", "Irrigate weekly"],
            "July": ["Support growth", "Spray micronutrients"],
            "August": ["Protect heavy flowering from bollworms"],
            "September": ["Monitor maturing bolls", "Check weather"],
            "October": ["Harvest mid to late month", "Dry cotton"],
            "November": ["Complete harvest", "Clear fields"],
            "December": ["Prepare fields for next cycle"]
        },
        "G-barbadense": {
            "January": ["Prepare soil", "Plan fertilization"],
            "February": ["Sow in southern zones"],
            "March": ["Treat seeds", "Sow in warmer climates"],
            "April": ["Begin irrigation", "Control early pests"],
            "May": ["Maintain irrigation", "Monitor pests/diseases"],
            "June": ["Spray foliar fertilizers", "Ensure water levels"],
            "July": ["Support vegetative growth", "Monitor water needs"],
            "August": ["Control insects during boll formation"],
            "September": ["Reduce irrigation", "Monitor boll growth"],
            "October": ["Start harvesting", "Dry cotton"],
            "November": ["Finish picking", "Store and gin cotton"],
            "December": ["Plan next season", "Prepare fields"]
        }
    }

    if species_name in calendars:
        # Build the calendar content as a static string first
        calendar_content = ""
        for month, tasks in calendars[species_name].items():
            calendar_content += f"<p><strong>{month}</strong></p>"
            for task in tasks:
                calendar_content += f"<p>&nbsp;&nbsp;&nbsp;&nbsp;• {task}</p>"

        # Embed the content into the card HTML, matching the style of other cards
        st.markdown(f"""
            <style>
                .card {{
                    background-color: #f1f8e9;
                    border-left: 6px solid #66bb6a;
                    padding: 20px;
                    border-radius: 15px;
                    box-shadow: 2px 4px 10px rgba(0,0,0,0.1);
                    margin: 20px 0;
                    font-family: 'Segoe UI', sans-serif;
                }}
                .card h3 {{
                    color: #2e7d32;
                    margin-bottom: 10px;
                }}
                .card p {{
                    color: #33691e;
                    font-size: 16px;
                    line-height: 1.6;
                }}
            </style>
            <div class="card">
                <h3>📅 {species_name} Crop Calendar</h3>
                {calendar_content}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("No calendar available for this species.")

def display_species_card(species_code, common_name, origin, climate, staple_length, yield_range, image_url):
    st.markdown(f"""
        <style>
            .species-card {{
                background-color: #f1f8e9;
                padding: 15px;
                border-radius: 15px;
                margin-bottom: 20px;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            }}
            .species-title {{
                font-size: 24px;
                color: #1b5e20;
                font-weight: bold;
            }}
            .species-detail {{
                font-size: 16px;
                color: #4e342e;
                margin: 5px 0;
            }}
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='species-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='species-title'>🌿 {species_code}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='species-detail'><b>Common Name:</b> {common_name}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='species-detail'><b>Origin:</b> {origin}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='species-detail'><b>Climate:</b> {climate}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='species-detail'><b>Staple Length:</b> {staple_length}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='species-detail'><b>Yield Range:</b> {yield_range}</div>", unsafe_allow_html=True)
        if image_url:
            st.image(image_url, use_column_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="📸 Uploaded Image", use_container_width=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        image.save(tmp.name)
        tmp_path = tmp.name

    results = model(tmp_path)[0]
    result_image = results.plot()
    detected_classes = list(set([model.names[int(cls)] for cls in results.boxes.cls]))

    st.image(result_image, caption="🔍 Detected Cotton Species", use_container_width=True)

    species = detected_classes[0] if detected_classes else None

    def display_species_card(title, origin, traits, tips, uses, extra=""):
        st.markdown(f"""
            <style>
                .card {{
                    background-color: #f1f8e9;
                    border-left: 6px solid #66bb6a;
                    padding: 20px;
                    border-radius: 15px;
                    box-shadow: 2px 4px 10px rgba(0,0,0,0.1);
                    margin: 20px 0;
                    font-family: 'Segoe UI', sans-serif;
                }}
                .card h3 {{
                    color: #2e7d32;
                    margin-bottom: 10px;
                }}
                .card p {{
                    color: #33691e;
                    font-size: 16px;
                    line-height: 1.6;
                }}
            </style>
            <div class="card">
                <h3>{title}</h3>
                <p><strong>🌍 Origin:</strong> {origin}</p>
                <p><strong>🌤 Traits:</strong> {traits}</p>
                <p><strong>💧 Care Tips:</strong> {tips}</p>
                <p><strong>🧵 Use Cases:</strong> {uses}</p>
                <p><strong>🌱 Bonus:</strong> {extra}</p>
            </div>
        """, unsafe_allow_html=True)

    if species == "G-arboreum":
        display_species_card(
            "🧬 Gossypium arboreum (Desi Cotton)",
            "India & Pakistan",
            "Naturally drought-resistant and pest-tolerant. Ideal for arid regions with less rainfall.",
            "Requires minimal irrigation, grows well in dry and semi-dry climates. Use organic compost to enhance growth.",
            "Hand-spun cotton, Ayurvedic products, eco-friendly fabrics.",
            "Supports biodiversity and traditional farming methods."
        )
        show_crop_calendar("G-arboreum")
    elif species == "G-barbadense":
        display_species_card(
            "🌱 Gossypium barbadense (Pima/Egyptian Cotton)",
            "South America",
            "Extra-long fibers, silky texture, high durability.",
            "Thrives in well-irrigated, nutrient-rich soil with moderate climate.",
            "Luxury garments, premium bedding and textiles.",
            "Known for soft feel and strength."
        )
        show_crop_calendar("G-barbadense")
    elif species == "G-herbaceum":
        display_species_card(
            "🌾 Gossypium herbaceum",
            "Africa and South Asia",
            "Short staple fiber, hardy plant, tolerates heat and drought.",
            "Minimal water required, prefers well-drained soil.",
            "Used in traditional textiles and handicrafts.",
            "Adaptable to poor soil conditions."
        )
        show_crop_calendar("G-herbaceum")
    elif species == "G-hirsutum":
        display_species_card(
            "☁️ Gossypium hirsutum (Upland Cotton)",
            "Central America",
            "High yield, medium fiber length, adaptable.",
            "Needs moderate water, grows in various soils.",
            "Most common cotton in clothing and textiles.",
            "Preferred by commercial cotton farmers."
        )
        show_crop_calendar("G-hirsutum")
    else:
        st.warning("⚠️ Could not identify the cotton species. Please try another image.")

    cotton_fact = random.choice(cotton_facts)
    st.markdown(f"""
    <div class="card">
        <h3>🧠 Fact about Cotton</h3>
        <p>{cotton_fact}</p>
    </div>
    """, unsafe_allow_html=True)