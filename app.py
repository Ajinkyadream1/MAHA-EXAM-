import streamlit as st

# 1. Page Configuration & Custom Web Typography Stylesheet Setup
st.set_page_config(page_title="Maha Exam Tracker", page_icon="🏛️", layout="centered")
st.markdown("""
    <link href="https://googleapis.com" rel="stylesheet">
    <style>
    .stApp { background-color: #F8F9FA; font-family: 'Montserrat', sans-serif !important; }
    .main-title { font-family: 'Cinzel', serif !important; color: #002F6C; font-weight: 800; text-align: center; font-size: 26px; margin-bottom: 5px; }
    .sub-title { color: #D32F2F; text-align: center; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 20px; }
    .disclaimer-box { background-color: #FFF9C4; padding: 12px; border-left: 5px solid #FBC02D; border-radius: 5px; margin-top: 30px; }
    .exam-card { background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 12px; border-top: 4px solid #002F6C; }
    .status-badge { display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; color: white; }
    </style>
""", unsafe_allow_html=True)

# 2. Setup Persistent In-Memory Database
if 'exams' not in st.session_state:
    st.session_state['exams'] = [
        {"id": 1, "title_en": "MPSC Civil Services Prelims 2026", "title_mr": "एमपीएससी नागरी सेवा पूर्व परीक्षा २०२६", "dept": "MPSC", "start": "2026-03-01", "last": "2026-04-30", "exam": "2026-05-31", "link": "https://mpsc.gov.in", "status": "Closed", "desc_en": "Covers Group A and B gazetted administrative posts.", "desc_mr": "गट अ आणि ब राजपत्रित प्रशासकीय पदांसाठी परीक्षा."},
        {"id": 2, "title_en": "IBPS PO Bank Recruitment XVI", "title_mr": "आयबीपीएस पीओ बँक भरती परीक्षा २०२६", "dept": "IBPS", "start": "2026-07-15", "last": "2026-08-10", "exam": "2026-08-22", "link": "https://ibps.in", "status": "Upcoming", "desc_en": "National recruitment drive for Probationary Officers.", "desc_mr": "राष्ट्रीयीकृत बँकांमध्ये पीओ पदांसाठी भरती."},
        {"id": 3, "title_en": "RRB NTPC Undergraduate Exam", "title_mr": "रेल्वे एनटीपीसी अंडरग्रेजुएट परीक्षा २०२६", "dept": "Railways (RRB)", "start": "2026-05-10", "last": "2026-06-02", "exam": "2026-06-13", "link": "https://rrbcdg.gov.in", "status": "Active", "desc_en": "Computer Based Testing timelines for railway positions.", "desc_mr": "रेल्वे पदांसाठी संगणक आधारित परीक्षा वेळापत्रक."},
        {"id": 4, "title_en": "Maharashtra Police Constable Bharti", "title_mr": "महाराष्ट्र पोलीस शिपाई भरती प्रक्रिया", "dept": "Maha Police", "start": "2026-01-05", "last": "2026-02-15", "exam": "2026-05-05", "link": "https://mahapolice.gov.in", "status": "Closed", "desc_en": "Mega recruitment drive for Police Constables.", "desc_mr": "पोलीस शिपाई पदांसाठी मेगा भरती प्रक्रिया."}
    ]

# 3. Layout Function for the Bottom Disclaimer Notice Box
def show_legal_banner():
    st.markdown("""
        <div class="disclaimer-box">
            <h6 style="margin:0; color:#F57F17; font-weight:700;">⚠️ IMPORTANT NOTICE / महत्वाची सूचना</h6>
            <p style="margin:4px 0 0 0; font-size:12px; color:#333;"><b>ENG:</b> This is an unofficial platform. Verify all real-time schedule changes directly on the official portal.</p>
            <p style="margin:4px 0 0 0; font-size:12px; color:#333;"><b>MAR:</b> हे एक अनधिकृत प्लॅटफॉर्म आहे. वेळापत्रकातील रिअल-टाइम बदलांसाठी कृपया अधिकृत पोर्टलवरून खात्री करून घ्यावी.</p>
        </div>
    """, unsafe_allow_html=True)

# 4. Initialize Navigation Layout Tabs
tab_student, tab_admin = st.tabs(["📝 Exam Schedules / वेळापत्रक", "🔒 Admin Dashboard / नियंत्रण कक्ष"])

# =========================================================
#                    STUDENT DISPLAY MODULE
# =========================================================
with tab_student:
    lang = st.radio("Select Language / भाषा", ["English", "मराठी"], horizontal=True, key="user_lang")
    st.markdown(f'<div class="main-title">{"MAHA EXAM GATEWAY" if lang=="English" else "महाराष्ट्र परीक्षा पोर्टल"}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-title">{"Live Timelines for Recruitments" if lang=="English" else "स्पर्धा परीक्षांचे अधिकृत वेळापत्रक"}</div>', unsafe_allow_html=True)
    
    search = st.text_input("", placeholder="Search exam or department..." if lang=="English" else "परीक्षा किंवा विभाग शोधा...", key="find")
    
    for item in st.session_state['exams']:
        title = item["title_en"] if lang == "English" else item["title_mr"]
        desc = item["desc_en"] if lang == "English" else item["desc_mr"]
        if search.lower() in title.lower() or search.lower() in item["dept"].lower():
            color = "#4CAF50" if item["status"] in ["Open", "Active"] else "#FF9800" if item["status"] == "Upcoming" else "#757575"
            st.markdown(f"""
                <div class="exam-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <b style="font-size:15px; color:#111; flex:1;">{title}</b>
                        <span class="status-badge" style="background-color:{color};">{item['status']}</span>
                    </div>
                    <p style="color:#666; font-size:11px; margin:4px 0;"><b>Dept:</b> {item['dept']}</p>
                    <p style="font-size:12px; color:#333; margin-bottom:8px;">{desc}</p>
                    <hr style="margin:6px 0; border:none; border-top:1px solid #EEE;"/>
                    <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; font-size:11px; text-align:center;">
                        <div><b>Form Start</b><br/>{item['start']}</div>
                        <div><b style="color:#D32F2F;">Last Date</b><br/>{item['last']}</div>
                        <div><b style="color:#002F6C;">Exam Date</b><br/>{item['exam']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.link_button("Go to Official Application Portal ↗" if lang=="English" else "अधिकृत अर्ज पोर्टलवर जा ↗", item["link"], use_container_width=True)
    show_legal_banner()

# =========================================================
#                    ADMIN MANAGEMENT MODULE
# =========================================================
with tab_admin:
    st.subheader("Database Control Panel")
    pin = st.text_input("Enter Admin Security Pin", type="password", key="gate")
    if pin == "admin123":
        st.success("Authorized Access.")
        with st.expander("➕ Add New Competitive Exam Entry"):
            add_en = st.text_input("Exam Name (English)")
            add_mr = st.text_input("Exam Name (मराठी)")
            add_dept = st.selectbox("Body", ["MPSC", "IBPS", "Railways (RRB)", "Maha Police", "Other"])
            c1, c2, c3 = st.columns(3)
            v_start = c1.text_input("Form Start Date", value="2026-01-01")
            v_last = c2.text_input("Last Date", value="2026-01-31")
            v_exam = c3.text_input("Exam Date", value="2026-06-01")
            add_link = st.text_input("Portal Link URL", value="https://")
            add_state = st.selectbox("Status", ["Upcoming", "Active", "Open", "Closed"])
            info_en = st.text_area("Details (EN)")
            info_mr = st.text_area("Details (MR)")
            if st.button("Save Entry"):
                if add_en and add_mr:
                    st.session_state['exams'].append({"id": len(st.session_state['exams'])+1, "title_en": add_en, "title_mr": add_mr, "dept": add_dept, "start": v_start, "last": v_last, "exam": v_exam, "link": add_link, "status": add_state, "desc_en": info_en, "desc_mr": info_mr})
                    st.rerun()

        if st.session_state['exams']:
            st.markdown("---")
            lookup = {f"{x['id']}: {x['title_en']}": i for i, x in enumerate(st.session_state['exams'])}
            pick = st.selectbox("Select Record to Update", list(lookup.keys()))
            idx = lookup[pick]
            st.session_state['exams'][idx]["title_en"] = st.text_input("Edit Name (EN)", value=st.session_state['exams'][idx]["title_en"])
            st.session_state['exams'][idx]["title_mr"] = st.text_input("Edit Name (MR)", value=st.session_state['exams'][idx]["title_mr"])
            bx1, bx2, bx3 = st.columns(3)
            st.session_state['exams'][idx]["start"] = bx1.text_input("Edit Start", value=st.session_state['exams'][idx]["start"])
            st.session_state['exams'][idx]["last"] = bx2.text_input("Edit Deadline", value=st.session_state['exams'][idx]["last"])
            st.session_state['exams'][idx]["exam"] = bx3.text_input("Edit Test", value=st.session_state['exams'][idx]["exam"])
            st.session_state['exams'][idx]["status"] = st.selectbox("Status Badge", ["Upcoming", "Active", "Open", "Closed"], index=["Upcoming", "Active", "Open", "Closed"].index(st.session_state['exams'][idx]["status"]))
            st.session_state['exams'][idx]["link"] = st.text_input("Update Target URL", value=st.session_state['exams'][idx]["link"])
            if st.button("Remove Record", type="primary"):
                st.session_state['exams'].pop(idx)
                st.rerun()
    elif pin != "":
        st.error("Invalid Pin.")
    show_legal_banner()
