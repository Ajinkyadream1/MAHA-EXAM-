import streamlit as st
import pandas as pd

# Set mobile-responsive page configuration matching the official look
st.set_page_config(page_title="Maha Exam Tracker", page_icon="🏛️", layout="centered")

# --- PLACE YOUR PUBLIC GOOGLE SHEET LINK HERE ---
# Paste your copied Google Sheet sharing URL inside the quotes below:
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1w_AXMeBluB5sM_soDDlH1Q3HmQ2HqixV1sx0kmzLEbI/edit?usp=sharing"

@st.cache_data(ttl=60)  # Automate live tracking: Refreshes data cache automatically every 60 seconds
def load_live_data(sheets_url):
    try:
        # Convert the standard sharing link into a direct clean CSV export endpoint
        csv_url = sheets_url.split('/edit')[0] + '/gviz/tq?tqx=out:csv'
        df = pd.read_csv(csv_url)
        # Standardize column naming rules by removing blank spacing or casing issues
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        return None

# Fetch data from the live online source spreadsheet
df_exams = load_live_data(GOOGLE_SHEET_URL)

# Custom injection CSS styling to mirror a polished government portal interface
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    .main-title { color: #002F6C; font-weight: bold; text-align: center; font-size: 24px; margin-bottom: 5px; }
    .sub-title { color: #D32F2F; text-align: center; font-size: 14px; font-weight: bold; margin-bottom: 20px; }
    .disclaimer-box { background-color: #FFF9C4; padding: 15px; border-left: 5px solid #FBC02D; border-radius: 5px; margin-bottom: 20px; }
    .exam-card { background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 15px; border-top: 4px solid #002F6C; }
    .status-badge { display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; color: white; }
    </style>
""", unsafe_allow_html=True)

# 1. Legal Bilingual Disclaimer Banner (Always fixed to top)
st.markdown("""
    <div class="disclaimer-box">
        <h4 style="margin:0; color:#F57F17;">⚠️ IMPORTANT NOTICE / महत्वाची सूचना</h4>
        <p style="margin:5px 0 0 0; font-size:13px; color:#333;"><b>ENG:</b> This is an unofficial platform. Verify all real-time schedule changes directly on the official portal.</p>
        <p style="margin:5px 0 0 0; font-size:13px; color:#333;"><b>MAR:</b> हे एक अनधिकृत प्लॅटफॉर्म आहे. वेळापत्रकातील रिअल-टाइम बदलांसाठी कृपया अधिकृत पोर्टलवरून खात्री करून घ्यावी.</p>
    </div>
""", unsafe_allow_html=True)

# 2. Setup Interactive Language Switcher 
lang = st.radio("Select Language / भाषा निवडा", ["English", "मराठी"], horizontal=True)

if lang == "English":
    st.markdown('<div class="main-title">Maharashtra Competitive Exams Tracker</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Official Timelines & Application Gateways</div>', unsafe_allow_html=True)
    search_placeholder = "Search exams by name or department..."
    no_results = "No active exam schedules found matching your query."
else:
    st.markdown('<div class="main-title">महाराष्ट्र स्पर्धा परीक्षा ट्रॅकर</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">अधिकृत वेळापत्रक आणि अर्ज लिंक्स</div>', unsafe_allow_html=True)
    search_placeholder = "परीक्षा किंवा विभागाद्वारे शोधा..."
    no_results = "तुमच्या शोधाशी जुळणारे कोणतेही वेळापत्रक सापडले नाही."

# 3. Validation fallback if the Google link fails
if df_exams is None or df_exams.empty:
    st.error("Unable to stream data. Please double-check your Google Sheet link permissions.")
else:
    # 4. Search Filter Input Box Setup
    search_query = st.text_input("", placeholder=search_placeholder)

    # 5. Process and display rows automatically
    for index, row in df_exams.iterrows():
        # Fallback fields to prevent system crashes if the sheet has empty rows
        title_en = str(row.get('Exam Name (EN)', ''))
        title_mr = str(row.get('Exam Name (MR)', ''))
        dept = str(row.get('Department', ''))
        start_date = str(row.get('Start Date', ''))
        last_date = str(row.get('Last Date', ''))
        exam_date = str(row.get('Exam Date', ''))
        apply_link = str(row.get('Apply Link', 'https://maharashtra.gov.in'))
        status = str(row.get('Status', 'Upcoming'))
        desc_en = str(row.get('Details (EN)', ''))
        desc_mr = str(row.get('Details (MR)', ''))

        # Match localized text depending on language selection switch
        display_title = title_en if lang == "English" else title_mr
        display_desc = desc_en if lang == "English" else desc_mr

        # Filter row logic based on user text entries
        if search_query.lower() in display_title.lower() or search_query.lower() in dept.lower():
            # Apply color dynamic markers matching Glide's visual style rules
            if status in ["Open", "Registration Open"]:
                badge_color = "#4CAF50" # Green
            elif status in ["Admit Card Out", "Active"]:
                badge_color = "#3F51B5" # Deep Blue
            elif status in ["Upcoming", "Tentative"]:
                badge_color = "#FF9800" # Amber Orange
            else:
                badge_color = "#757575" # Muted Gray

            card_html = f"""
            <div class="exam-card">
                <div style="display:flex; justify-content:space-between; align-items:center; gap: 10px;">
                    <b style="font-size:16px; color:#111;">{display_title}</b>
                    <span class="status-badge" style="background-color:{badge_color}; white-space: nowrap;">{status}</span>
                </div>
                <p style="color:#666; font-size:12px; margin: 5px 0 10px 0;"><b>Department / विभाग:</b> {dept}</p>
                <p style="font-size:13px; color:#333; margin:0 0 10px 0;">{display_desc}</p>
                <hr style="margin:10px 0; border:none; border-top:1px solid #EEE;"/>
                <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:10px; font-size:12px; text-align:center;">
                    <div><b style="color:#555;">Form Start</b><br/>{start_date}</div>
                    <div><b style="color:#555;">Last Date</b><br/>{last_date}</div>
                    <div><b style="color:#2E7D32;">Exam Date</b><br/>{exam_date}</div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Application outbound portal redirect anchor action item button
            btn_label = "Go to Official Application Portal ↗" if lang == "English" else "अधिकृत अर्ज पोर्टलवर जा ↗"
            st.link_button(btn_label, apply_link, use_container_width=True)
            st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)
