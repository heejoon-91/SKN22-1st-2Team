import streamlit as st

def base_layout():
    st.set_page_config(page_title="EV Dashboard", layout="wide")

    st.markdown("""
            <style>
             /* 무지개 줄 스타일 */
            .sidebar-gradient-line {
                margin-top:350px;
                width: 100%;
                height: 4px;
                border-radius: 999px;
                background: linear-gradient(90deg,
                    #ff6b6b,
                    #feca57,
                    #1dd1a1,
                    #54a0ff,
                    #5f27cd,
                    #ff6b6b
                );
                background-size: 300% 300%;
                animation: sidebarMove 5s ease infinite;
            }

            @keyframes sidebarMove {
                0%   { background-position: 0% 50%; }
                50%  { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }    


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
        st.sidebar.markdown('<div class="sidebar-gradient-line"></div>', unsafe_allow_html=True)