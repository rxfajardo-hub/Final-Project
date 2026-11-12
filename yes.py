import streamlit as st

st.markdown("""
    <style>
    h1 {
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 1. INITIALIZE PAGE TRACKER & USER INFO (Our Memory Notebook)
if "page_number" not in st.session_state:
    st.session_state.page_number = 1
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "user_age" not in st.session_state:
    st.session_state.user_age = 18
if "user_gender" not in st.session_state:
    st.session_state.user_gender = "Male"
if "user_race" not in st.session_state:
    st.session_state.user_race = "Asian"

# 2. OUR DATABANK (List of scholarships with eligibility tags)
scholarships = [
    {
        "name": "HSF Scholarship",
        "type": "General / All Majors",
        "url": "https://www.scholarships.com/scholarships/hsf-scholarship",
        "min_age": 16,
        "gender": "All",
        "race": "Hispanic / Latino"
    },
    {
        "name": "WSOS Baccalaureate Scholarship",
        "type": "General / All Majors",
        "url": "https://www.scholarships.com/scholarships/wsos-baccalaureate-scholarship",
        "min_age": 16,
        "gender": "All",
        "race": "All"
    },
    {
        "name": "CCI Hispanic Scholarship",
        "type": "STEM & Computer Science",
        "url": "https://www.scholarships.com/scholarships/cci-hispanic-scholarship",
        "min_age": 16,
        "gender": "All",
        "race": "Hispanic / Latino"
    },
    {
        "name": "WISE (Women in STEM Excel) Scholarship",
        "type": "STEM & Engineering",
        "url": "https://www.scholarships.com/scholarships/wise-women-in-stem-excel-scholarship",
        "min_age": 16,
        "gender": "Female",
        "race": "All"
    },
    {
        "name": "WTS Portland Chapter Gail Achterman Leadership Scholarship",
        "type": "Minority / High School Seniors",
        "url": "https://www.scholarships.com/scholarships/wts-portland-chapter-gail-achterman-leadership-scholarship",
        "min_age": 16,
        "gender": "Female",
        "race": "All"
    },
    {
        "name": "OHDC Larry B. Sanchez Memorial Scholarship",
        "type": "Minority Students",
        "url": "https://www.scholarships.com/scholarships/ohdc-larry-b-sanchez-memorial-scholarship",
        "min_age": 16,
        "gender": "All",
        "race": "All"
    },
    {
        "name": "Kristy J. Hendrickson Scholarship",
        "type": "Arts & Creative Design",
        "url": "https://scholarships.com",
        "min_age": 16,
        "gender": "Female",
        "race": "All"
    },
]

# 3. MAIN WEBSITE LOGIC

# --- PAGE 1: THE HOME PAGE ---
if st.session_state.page_number == 1:
    st.title("🎓PNW Scholar Tracker")
    st.subheader("See if you can qualify for scholarships in your field of study!")
    
    st.write("Welcome to the platform! Click the button below to browse all listings or search for specific scholarship types.")
    
    st.write("") # Blank space for layout padding

    # Big main button to go to the profile page
    if st.button("Explore Scholarships 🚀", use_container_width=True):
        st.session_state.page_number = 2
        st.rerun()

# --- PAGE 2: TELL US ABOUT YOURSELF ---
elif st.session_state.page_number == 2:
    st.title("🔍 Tell Us About Yourself!")
    
    if st.button("⬅️ Back to Home"):
        st.session_state.page_number = 1
        st.rerun()
        
    st.write("---")

    # User Inputs
    age = st.number_input("Age:", min_value=13, max_value=100, value=st.session_state.user_age)
    
    gender_list = ["Male", "Female", "Non-binary / Other", "Prefer not to say"]
    gender = st.selectbox("Gender:", gender_list, index=gender_list.index(st.session_state.user_gender))
    
    race_list = ["Asian", "Black / African American", "Hispanic / Latino", "White", "Native American / Indigenous", "Other"]
    race = st.selectbox("Race / Ethnicity:", race_list, index=race_list.index(st.session_state.user_race))

    st.write("") # Layout spacing

    # Button to save answers and move to Page 3
    if st.button("Find My Matches 🎯", use_container_width=True):
        st.session_state.user_age = age
        st.session_state.user_gender = gender
        st.session_state.user_race = race
        st.session_state.page_number = 3
        st.rerun()

# --- PAGE 3: MATCHED SCHOLARSHIPS & SEARCH PAGE ---
elif st.session_state.page_number == 3:
    st.title("🎯 Your Eligible Scholarships")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Edit My Info"):
            st.session_state.page_number = 2
            st.rerun()
    with col2:
        if st.button("🏠 Back to Home"):
            st.session_state.search_query = ""
            st.session_state.page_number = 1
            st.rerun()

    st.info(f"**Profile:** {st.session_state.user_age} years old | {st.session_state.user_gender} | {st.session_state.user_race}")
    st.write("---")

    # Filter scholarships based on Age, Gender, and Race
    eligible_list = []
    for s in scholarships:
        age_match = st.session_state.user_age >= s["min_age"]
        gender_match = (s["gender"] == "All") or (s["gender"] == st.session_state.user_gender)
        race_match = (s["race"] == "All") or (s["race"] == st.session_state.user_race)
        
        if age_match and gender_match and race_match:
            eligible_list.append(s)

    # Keyword Search Bar on top of eligible matches
    user_input = st.text_input("Type a keyword (e.g., STEM, Minority, General):", value=st.session_state.search_query)
    query = user_input.lower().strip()

    if query:
        filtered_list = [s for s in eligible_list if query in s["name"].lower() or query in s["type"].lower()]
    else:
        filtered_list = eligible_list

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
