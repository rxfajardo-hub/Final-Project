import base64
import streamlit as st

# --- NEW: BACKGROUND IMAGE FUNCTION ---
def set_background(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.55), rgba(0, 0, 0, 0.55)), url(data:image/png;base64,{b64_encoded});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        [data-testid="stHeader"] {{
            background: rgba(0,0,0,0);
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

# Replace "background.png" with your exact image file name
set_background("background.jpg")
# --------------------------------------

# 1. INITIALIZE PAGE TRACKER (Our Memory Notebook)
if "page_number" not in st.session_state:
    st.session_state.page_number = 1
if "search_query" not in st.session_state:
    st.session_state.search_query = ""

# 2. OUR DATABANK (List of scholarships)
scholarships = [
    {"name": "HSF Scholarship", "type": "General / All Majors", "url": "https://www.scholarships.com/scholarships/hsf-scholarship"},
    {"name": "WSOS Baccalaureate Scholarship", "type": "General / All Majors", "url": "https://www.scholarships.com/scholarships/wsos-baccalaureate-scholarship"},
    {"name": "CCI Hispanic Scholarship", "type": "STEM & Computer Science", "url": "https://www.scholarships.com/scholarships/cci-hispanic-scholarship"},
    {"name": "WISE (Women in STEM Excel) Scholarship", "type": "STEM & Engineering", "url": "https://www.scholarships.com/scholarships/wise-women-in-stem-excel-scholarship"},
    {"name": "WTS Portland Chapter Gail Achterman Leadership Scholarship", "type": "Minority / High School Seniors", "url": "https://www.scholarships.com/scholarships/wts-portland-chapter-gail-achterman-leadership-scholarship"},
    {"name": "OHDC Larry B. Sanchez Memorial Scholarship", "type": "Minority Students", "url": "https://www.scholarships.com/scholarships/ohdc-larry-b-sanchez-memorial-scholarship"},
    {"name": "Kristy J. Hendrickson Scholarship", "type": "Arts & Creative Design", "url": "https://scholarships.com"},
]

# 3. MAIN WEBSITE LOGIC

# --- PAGE 1: THE HOME PAGE ---
if st.session_state.page_number == 1:
    st.title("🎓 Smart Scholarship Finder")
    st.subheader("Discover financial aid opportunities for your future.")
    
    st.write("Welcome to the platform! Click the button below to browse all listings or search for specific scholarship types.")
    
    st.write("") # Blank space for layout padding

    # Big main button to go to the search page
    if st.button("Explore Scholarships 🚀", use_container_width=True):
        st.session_state.page_number = 2
        st.rerun()

# --- PAGE 2: THE SEARCH & LIST PAGE ---
elif st.session_state.page_number == 2:
    st.title("🔍 Search Scholarships")
    
    # Simple link back to the homepage at the top
    if st.button("⬅️ Back to Home"):
        st.session_state.search_query = "" # Clear old search text
        st.session_state.page_number = 1
        st.rerun()
        
    st.write("---")

    # Center Search Bar
    user_input = st.text_input("Type a keyword (e.g., STEM, Minority, General):", value=st.session_state.search_query)

    # Every time they type, we update the search filter instantly
    query = user_input.lower().strip()

    # Python Filter Logic
    if query:
        filtered_list = [s for s in scholarships if query in s["name"].lower() or query in s["type"].lower()]
    else:
        filtered_list = scholarships # If search is empty, show everything

    st.write("") # Layout spacing

    # Display the results
    if not filtered_list:
        st.warning("⚠️ No matching scholarship categories found. Try a different word!")
    else:
        for item in filtered_list:
            st.markdown(f"### [{item['name']}]({item['url']})")
            st.write(f"**Focus Category:** {item['type']}")
            st.write(f"🔗 [Visit Official Website]({item['url']})")
            st.write("---")
