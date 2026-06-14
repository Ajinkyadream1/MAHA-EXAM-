import streamlit as st

# Set mobile-responsive page config with government aesthetic colors
st.set_page_config(page_title="Maha Exam Tracker", page_icon="🏛️", layout="centered")

# Custom CSS to apply government theme style (Deep Blue and Gold accents)
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

# 1. Legal Bilingual Disclaimer Banner
st.markdown("""
    <div class="disclaimer-box">
        <h4 style="margin:0; color:#F57F17;">⚠️ IMPORTANT NOTICE / महत्वाची सूचना</h4>
        <p style="margin:5px 0 0 0; font-size:13px; color:#333;"><b>ENG:</b> This is an unofficial platform. Verify all real-time schedule changes directly on the official portal.</p>
        <p style="margin:5px 0 0 0; font-size:13px; color:#333;"><b>MAR:</b> हे एक अनधिकृत प्लॅटफॉर्म आहे. वेळापत्रकातील रिअल-टाइम बदलांसाठी कृपया अधिकृत पोर्टलवरून खात्री करून घ्यावी.</p>
    </div>
""", unsafe_allow_html=True)

# 2. Language Selection Toggle
lang = st.radio("Select Language / भाषा निवडा", ["English", "मराठी"], horizontal=True)

if lang == "English":
    st.markdown('<div class="main-title">Maharashtra Competitive Exams Tracker</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Official Timelines & Application Gateways</div>', unsafe_allow_html=True)
    search_placeholder = "Search exams by name or department..."
else:
    st.markdown('<div class="main-title">महाराष्ट्र स्पर्धा परीक्षा ट्रॅकर</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">अधिकृत वेळापत्रक आणि अर्ज लिंक्स</div>', unsafe_allow_html=True)
    search_placeholder = "परीक्षा किंवा विभागाद्वारे शोधा..."

# 3. Real Maharashtra Exam Data
exams_data = [
    {
        "title_en": "MPSC Civil Services Prelims 2026", "title_mr": "एमपीएससी नागरी सेवा पूर्व परीक्षा २०२६",
        "dept": "MPSC", "start": "15 Dec 2025", "last": "15 Jan 2026", "exam": "31 May 2026",
        "link": "https://mpsconline.gov.in", "status": "Closed",
        "desc_en": "Covers Group A and B gazetted posts.", "desc_mr": "गट अ आणि गट ब राजपत्रित पदांसाठी."
    },
    {
        "title_en": "MPSC Group B Combined Prelims 2026", "title_mr": "एमपीएससी गट ब संयुक्त पूर्व परीक्षा २०२६",
        "dept": "MPSC", "start": "10 Jan 2026", "last": "12 Feb 2026", "exam": "14 Jun 2026",
        "link": "https://mpsconline.gov.in", "status": "Admit Card Out",
        "desc_en": "Recruitment for PSI, STI, and ASO posts.", "desc_mr": "पीएसआय, एसटीआय आणि एएसओ पदांसाठी भरती."
    },
    {
        "title_en": "MPSC Group C Combined Prelims 2026", "title_mr": "एमपीएससी गट क संयुक्त पूर्व परीक्षा २०२६",
        "dept": "MPSC", "start": "01 Feb 2026", "last": "05 Mar 2026", "exam": "12 Jul 2026",
        "link": "https://mpsconline.gov.in", "status": "Open",
        "desc_en": "Covers Tax Assistant and Clerk-Typist posts.", "desc_mr": "कर सहाय्यक आणि लिपिक-टंकलेखक पदांसाठी."
    },
    {
        "title_en": "Maharashtra Teacher Eligibility Test (MahaTET)", "title_mr": "महाराष्ट्र शिक्षक पात्रता परीक्षा (महाटीईटी)",
        "dept": "MSCE Pune", "start": "20 Aug 2026", "last": "22 Sep 2026", "exam": "15 Nov 2026",
        "link": "https://mahatet.in", "status": "Upcoming",
        "desc_en": "Mandatory certification for teaching roles in Maharashtra.", "desc_mr": "शिक्षक भरतीसाठी आवश्यक पात्रता परीक्षा."
    },
    {
        "title_en": "Maharashtra Police Constable Bharti", "title_mr": "महाराष्ट्र पोलीस शिपाई भरती",
        "dept": "Home Dept", "start": "05 Sep 2026", "last": "08 Oct 2026", "exam": "20 Dec 2026",
        "link": "https://mahapolicerecruitment.org", "status": "Upcoming",
        "desc_en": "Mega recruitment drive for Constable positions.", "desc_mr": "पोलीस शिपाई पदांसाठी मेगा भरती."
    }
]

# 4. Search Filter
search_query = st.text_input("", placeholder=search_placeholder)

# 5. Render Dynamic Cards
for exam in exams_data:
    title = exam["title_en"] if lang == "English" else exam["title_mr"]
    desc = exam["desc_en"] if lang == "English" else exam["desc_mr"]
    
    # Filter matching
    if search_query.lower() in title.lower() or search_query.lower() in exam["dept"].lower():
        # Color codes for statuses
        badge_color = "#4CAF50" if exam["status"] == "Open" else "#3F51B5" if exam["status"] == "Admit Card Out" else "#FF9800" if exam["status"] == "Upcoming" else "#757575"
        
        card_html = f"""
        <div class="exam-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <b style="font-size:16px; color:#111;">{title}</b>
                <span class="status-badge" style="background-color:{badge_color};">{exam['status']}</span>
            </div>
            <p style="color:#666; font-size:12px; margin: 5px 0 10px 0;"><b>Department / विभाग:</b> {exam['dept']}</p>
            <p style="font-size:13px; color:#333; margin:0 0 10px 0;">{desc}</p>
            <hr style="margin:10px 0; border:none; border-top:1px solid #EEE;"/>
            <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:10px; font-size:12px; text-align:center;">
                <div><b style="color:#555;">Form Start</b><br/>{exam['start']}</div>
                <div><b style="color:#555;">Last Date</b><br/>{exam['last']}</div>
                <div><b style="color:#2E7D32;">Exam Date</b><br/>{exam['exam']}</div>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Authentic Portal Link Button
        btn_label = "Go to Official Application Portal ↗" if lang == "English" else "अधिकृत अर्ज पोर्टलवर जा ↗"
        st.link_button(btn_label, exam["link"], use_container_width=True)
        st.markdown("<br/>", unsafe_data_allowed=True)
