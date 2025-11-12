import streamlit as st

def base_layout():
    st.set_page_config(page_title="EV Dashboard", layout="wide")

    st.markdown("""
            <style>
            [data-testid="stSidebarNav"],
            [data-testid="stSidebarNavItems"],
            nav[aria-label="main navigation"],
            section[data-testid="stSidebar"] ul[role="list"]{ display:none !important; }
            </style>
            """, unsafe_allow_html=True)

    # --- 사이드바 메뉴

    with st.sidebar:
        st.page_link("app.py",                   label="Home")
        st.page_link("pages/1_find_station.py",    label="충전소 검색")
        st.page_link("pages/2_diff_charge.py",     label="요금비교")
        st.page_link("pages/3_recommend_route.py", label="경로추천")
        st.page_link("pages/4_faq_page.py",        label="FAQ")
