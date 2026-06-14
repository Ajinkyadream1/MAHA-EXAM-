import streamlit as st

# 1. Page Configuration Setup (Government Blue & Gold Theme Layout)
st.set_page_config(page_title="Maha Exam Tracker", page_icon="🏛️", layout="centered")

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

# 2. Setup Persistent In-Memory Database (No Google Sheets Needed)
if 'exams' not in st.session_state:
    st.session_state['exams'] = [
        {
            "id": 1, "title_en": "MPSC Civil Services Combined Prelims 2026", "title_mr": "एमपीएससी नागरी सेवा संयुक्त पूर्व परीक्षा २०२६",
            "dept": "MPSC", "start": "2026-03-01", "last": "2026-04-30", "exam": "2026-05-31",
            "link": "https://mpsc.gov.in", "status": "Closed",
            "desc_en": "Covers state-level Group A and B gazetted administrative posts.", "desc_mr": "राज्यस्तरीय गट अ आणि ब राजपत्रित प्रशासकीय पदांसाठी परीक्षा."
        },
        {
            "id": 2, "title_en": "IBPS PO (Probationary Officers) CRP XVI", "title_mr": "आयबीपीएस पीओ बँक भरती परीक्षा २०२६",
            "dept": "IBPS", "start": "2026-07-15", "last": "2026-08-10", "exam": "2026-08-22",
            "link": "https://ibps.in", "status": "Upcoming",
            "desc_en": "National bank recruitment drive for Probationary Officers.", "desc_mr": "राष्ट्रीयीकृत बँकांमध्ये प्रोबेशनरी ऑफिसर पदांसाठी भरती."
        },
        {
            "id": 3, "title_en": "RRB NTPC Undergraduate CBT-1 Exam", "title_mr": "रेल्वे एनटीपीसी अंडरग्रेजुएट परीक्षा २०२६",
            "dept": "Railways (RRB)", "start": "2026-05-10", "last": "2026-06-02", "exam": "2026-06-13",
            "link": "https://rrbcdg.gov.in", "status": "Active",
            "desc_en": "Revised Computer Based Testing timelines for Undergraduate positions.", "desc_mr": "अंडरग्रेजुएट रेल्वे पदांसाठी सुधारित संगणक आधारित परीक्षा वेळापत्रक."
        },
        {
            "id": 4, "title_en": "Maharashtra Police Constable Recruitment", "title_mr": "महारष्ट्र पोलीस शिपाई भरती प्रक्रिया",
            "dept": "Maharashtra Police", "start": "2026-01-05", "last": "2026-02-15", "exam": "2026-05-05",
            "link": "https://mahapolice.gov.in", "status": "Closed",
            "desc_en": "State-wide mega recruitment drive for Police Constables and SRPF forces.", "desc_mr": "पोलीस शिपाई आणि एसआरपीएफ दलांसाठी राज्यव्यापी मेगा भरती प्रक्रिया."
        }
    ]

# 3. Public View Top Notification Banner
st.markdown("""
    <div class="disclaimer-box">
        <h4 style="margin:0; color:#F57F17;">⚠️ IMPORTANT NOTICE / महत्वाची सूचना</h4>
        <p style="margin:5px 0 0 0; font-size:13px; color:#333;"><b>ENG:</b> This is an unofficial platform. Verify all real-time schedule changes directly on the official portal.</p>
        <p style="margin:5px 0 0 0; font-size:13px; color:#333;"><b>MAR:</b> हे एक अनधिकृत प्लॅटफॉर्म आहे. वेळापत्रकातील रिअल-टाइम बदलांसाठी कृपया अधिकृत पोर्टलवरून खात्री करून घ्यावी.</p>
    </div>
""", unsafe_allow_html=True)

# Create Navigation Tabs (Student View vs Protected Admin Control Room)
tab_student, tab_admin = st.tabs(["📝 Exam Schedules / वेळापत्रक", "🔒 Admin Dashboard / नियंत्रण कक्ष"])

# =========================================================
#                    STUDENT VIEW TAB
# =========================================================
with tab_student:
    lang = st.radio("Select Interface Language / भाषा निवडा", ["English", "मराठी"], horizontal=True, key="student_lang")
    
    if lang == "English":
        st.markdown('<div class="main-title">Maharashtra Exam Gateway</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-title">Live Timelines for Competitive Recruitments</div>', unsafe_allow_html=True)
        search_placeholder = "Search by exam name or department..."
    else:
        st.markdown('<div class="main-title">महाराष्ट्र परीक्षा पोर्टल</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-title">स्पर्धा परीक्षांचे अधिकृत वेळापत्रक</div>', unsafe_allow_html=True)
        search_placeholder = "परीक्षा किंवा विभागाचे नाव शोधा..."

    search_query = st.text_input("", placeholder=search_placeholder, key="search_bar")

    # Dynamic Exam Card Builder
    for exam in st.session_state['exams']:
        title = exam["title_en"] if lang == "English" else exam["title_mr"]
        desc = exam["desc_en"] if lang == "English" else exam["desc_mr"]
        
        if search_query.lower() in title.lower() or search_query.lower() in exam["dept"].lower():
            if exam["status"] in ["Open", "Active"]:
                badge_color = "#4CAF50"
            elif exam["status"] == "Upcoming":
                badge_color = "#FF9800"
            else:
                badge_color = "#757575"
                
            card_html = f"""
            <div class="exam-card">
                <div style="display:flex; justify-content:space-between; align-items:center; gap:10px;">
                    <b style="font-size:16px; color:#111;">{title}</b>
                    <span class="status-badge" style="background-color:{badge_color}; white-space: nowrap;">{exam['status']}</span>
                </div>
                <p style="color:#666; font-size:12px; margin: 5px 0 10px 0;"><b>Department / विभाग:</b> {exam['dept']}</p>
                <p style="font-size:13px; color:#333; margin:0 0 10px 0;">{desc}</p>
                <hr style="margin:10px 0; border:none; border-top:1px solid #EEE;"/>
                <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:10px; font-size:12px; text-align:center;">
                    <div><b style="color:#555;">Form Start</b><br/>{exam['start']}</div>
                    <div><b style="color:#D32F2F;">Last Date</b><br/>{exam['last']}</div>
                    <div><b style="color:#002F6C;">Exam Date</b><br/>{exam['exam']}</div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            btn_label = "Go to Official Application Portal ↗" if lang == "English" else "अधिकृत अर्ज पोर्टलवर जा ↗"
            st.link_button(btn_label, exam["link"], use_container_width=True)
            st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)

# =========================================================
#                    ADMIN CONTROL TAB (FIXED MIGRATION)
# =========================================================
with tab_admin:
    st.subheader("Manage Database Manually")
    
    # Simple Gatekeeper Passcode Check
    admin_password = st.text_input("Enter Admin Security Pin", type="password", key="admin_pin")
    
    if admin_password == "admin123":
        st.success("Access Granted! You can modify or add data entries below.")
        
        # --- ACTION SECTION 1: ADD NEW EXAM ---
        with st.expander("➕ Add New Competitive Exam Entry"):
            new_en = st.text_input("Exam Name (English)")
            new_mr = st.text_input("Exam Name (Marathi / मराठी)")
            new_dept = st.selectbox("Department / Body", ["MPSC", "IBPS", "Railways (RRB)", "Maharashtra Police", "Other"])
            col_d1, col_d2, col_d3 = st.columns(3)
            new_start = col_d1.text_input("Form Start Date", value="2026-01-01")
            new_last = col_d2.text_input("Last Date to Apply", value="2026-01-31")
            new_exam = col_d3.text_input("Written Exam Date", value="2026-06-01")
            new_link = st.text_input("Official Portal Link URL", value="https://")
            new_status = st.selectbox("Current Status", ["Upcoming", "Active", "Open", "Closed"])
            new_desc_en = st.text_area("Details Brief (English)")
            new_desc_mr = st.text_area("Details Brief (Marathi / मराठी)")
            
            if st.button("Save New Entry to Database"):
                if new_en and new_mr:
                    new_id = len(st.session_state['exams']) + 1
                    st.session_state['exams'].append({
                        "id": new_id, "title_en": new_en, "title_mr": new_mr,
                        "dept": new_dept, "start": new_start, "last": new_last, "exam": new_exam,
                        "link": new_link, "status": new_status, "desc_en": new_desc_en, "desc_mr": new_desc_mr
                    })
                    st.success("Successfully added! Switch to the Student View tab to verify.")
                    st.rerun()
                else:
                    st.error("Please complete the Exam Name fields before saving.")

        # --- ACTION SECTION 2: EDIT EXISTING EXAMS ---
        if st.session_state['exams']:
            st.markdown("---")
            st.subheader("📝 Edit or Delete Active Records")
            
            exam_options = {f"{e['id']}: {e['title_en']}": idx for idx, e in enumerate(st.session_state['exams'])}
            selected_exam_str = st.selectbox("Select Record to Update", list(exam_options.keys()))
            target_idx = exam_options[selected_exam_str]
            
            # Form fields securely nested inside the password loop context block
            st.session_state['exams'][target_idx]["title_en"] = st.text_input("Edit Name (EN)", value=st.session_state['exams'][target_idx]["title_en"])
