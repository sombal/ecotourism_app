import streamlit as st
import pandas as pd
from datetime import datetime, date
import time

# ====================== 페이지 설정 ======================
st.set_page_config(
    page_title="생태관광 프로그램 신청",
    page_icon="🌿",
    layout="wide"
)

# ====================== 예쁜 테마 ======================
st.markdown("""
    <style>
    .main {background-color: #f0f7f4 !important;}
    
    .program-card {
        background-color: white; 
        padding: 25px; 
        border-radius: 16px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
        margin-bottom: 20px; 
        border: 1px solid #e0e0e0;
        transition: transform 0.2s;
    }
    .program-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .title {color: #1a5f3a; font-size: 46px; font-weight: bold; text-align: center; margin-bottom: 8px;}
    .subtitle {color: #2e7d32; text-align: center; font-size: 21px; margin-bottom: 35px;}
    
    .program-image {
        width: 100%; 
        height: 220px; 
        object-fit: cover; 
        border-radius: 12px; 
        margin-bottom: 18px;
    }
    
    .stButton > button {
        background-color: #1a5f3a !important;
        color: white !important;
        font-size: 16px;
        padding: 12px 20px;
        border-radius: 10px;
        font-weight: bold;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #14532d !important;
    }
    
    .notice {
        background-color: #fff8e1; 
        padding: 20px; 
        border-radius: 12px; 
        border-left: 6px solid #ffc107;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# ====================== 사이드바 ======================
menu = st.sidebar.selectbox(
    "📍 메뉴 선택",
    ["🏠 프로그램 목록", "🔄 내 신청 확인 / 취소", "🔑 관리자 페이지"]
)
st.sidebar.info("🌱 생태관광 프로그램 신청 시스템\n버전 1.6 - 예쁜 테마")

# ====================== 데이터 불러오기 ======================
try:
    df = pd.read_csv("신청목록.csv", encoding="utf-8-sig")
except:
    df = pd.DataFrame(columns=["신청시간", "프로그램", "날짜", "이름", "전화번호", "이메일", "생년월일", "요청사항", "금액", "유형"])

try:
    waitlist = pd.read_csv("대기자목록.csv", encoding="utf-8-sig")
except:
    waitlist = pd.DataFrame(columns=["신청시간", "프로그램", "날짜", "이름", "전화번호", "이메일", "생년월일", "요청사항", "금액", "유형", "대기순위"])

# ====================== 페이지 상태 ======================
if "page" not in st.session_state:
    st.session_state.page = "main"

# ====================== 프로그램 목록 ======================
if st.session_state.page == "main":
    st.markdown('<p class="title">🌿 생태관광</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">자연과 주민, 여행자가 함께하는 특별한 여행</p>', unsafe_allow_html=True)

    st.markdown("""
        <div class="notice">
            <strong>📢 공지사항 및 안내</strong><br>
            • 모든 프로그램은 선착순 접수입니다.<br>
            • 정원이 마감된 프로그램은 대기자 신청이 가능합니다.<br>
            • 대기자는 신청 순서대로 우선순위가 부여됩니다.<br>
            • 문의 : 02-723-8677
        </div>
    """, unsafe_allow_html=True)

    programs = {
        1: {"name": "정기 생태관광(5월)", "period": "2026년 5월 22일 (금) ~ 23일 (토)", "desc": "대암산 용늪과 함께하는 양구 생태관광 프로그램", "max": 20, "emoji": "🏔️", "deadline": date(2026, 5, 7), "price": 60000, "image": "https://raw.githubusercontent.com/sombal/ecotourism_app/main/images/1.jpg"},
        2: {"name": "정기 생태관광(6월)", "period": "2026년 6월 19일 (금) ~ 20일 (토)", "desc": "고창의 주민들과 함께하는 힐링 생태관광 프로그램", "max": 20, "emoji": "🌺", "deadline": date(2026, 6, 11), "price": 60000, "image": "https://raw.githubusercontent.com/sombal/ecotourism_app/main/images/2.png"},
        3: {"name": "정기 생태관광(7월)", "period": "2026년 7월 17일 (금) ~ 18일 (토)", "desc": "여름 하늘처럼 시원한 괴산호 트레킹 생태관광 프로그램", "max": 20, "emoji": "🏞️", "deadline": date(2026, 7, 9), "price": 60000, "image": "https://raw.githubusercontent.com/sombal/ecotourism_app/main/images/3.jpg"},
        4: {"name": "정기 생태관광(9월)", "period": "2026년 9월 11일 (금) ~ 12일 (토)", "desc": "국토 정중앙 양구의 가을을 만끽할 수 있는 생태관광 프로그램", "max": 20, "emoji": "🌲", "deadline": date(2026, 9, 3), "price": 60000, "image": "https://raw.githubusercontent.com/sombal/ecotourism_app/main/images/4.jpg"},
        5: {"name": "정기 생태관광(10월)", "period": "2026년 10월 16일 (금) ~ 17일 (토)", "desc": "생태수도, 순천만의 아름다운 가을을 만나볼 수 있는 생태관광 프로그램", "max": 20, "emoji": "🍁", "deadline": date(2026, 10, 7), "price": 60000, "image": "https://raw.githubusercontent.com/sombal/ecotourism_app/main/images/5.jpg"}
    }

    cols = st.columns(2)

    for idx, prog in programs.items():
        current = len(df[df["프로그램"] == prog["name"]]) if not df.empty else 0
        wait_count = len(waitlist[waitlist["프로그램"] == prog["name"]]) if not waitlist.empty else 0
        is_closed = date.today() > prog["deadline"]
        is_full = current >= prog["max"]

        with cols[(idx-1) % 2]:
            with st.container(border=True):
                st.markdown(f'<img src="{prog["image"]}" class="program-image">', unsafe_allow_html=True)
                
                st.markdown(f"""
                    <h3>{prog['emoji']} {prog['name']}</h3>
                    <p><strong>📅 {prog['period']}</strong></p>
                    <p>{prog['desc']}</p>
                    <p><small>참가비: {prog['price']:,}원 | 최대 인원: {prog['max']}명 | 현재 신청: {current}명 | 대기자: {wait_count}명</small></p>
                """, unsafe_allow_html=True)

                if is_closed:
                    st.markdown(f'<p class="deadline">🔒 접수 마감되었습니다 ({prog["deadline"]})</p>', unsafe_allow_html=True)
                    st.button("신청 불가", disabled=True, use_container_width=True)
                elif is_full:
                    st.markdown('<p class="full">🔒 정원이 마감되었습니다</p>', unsafe_allow_html=True)
                    if st.button(f"⏳ 대기자로 신청하기 (현재 {wait_count}명 대기)", key=f"wait_{idx}", use_container_width=True):
                        st.session_state.selected_program = prog
                        st.session_state.is_waitlist = True
                        st.session_state.page = "apply"
                        st.rerun()
                else:
                    if st.button(f"✨ {prog['name']} 신청하기", key=f"apply_{idx}", use_container_width=True):
                        st.session_state.selected_program = prog
                        st.session_state.is_waitlist = False
                        st.session_state.page = "apply"
                        st.rerun()

# ====================== 신청 페이지 ======================
elif st.session_state.page == "apply":
    if "selected_program" not in st.session_state:
        st.error("잘못된 접근입니다.")
        if st.button("← 프로그램 목록으로 돌아가기"):
            st.session_state.page = "main"
            st.rerun()
        st.stop()

    prog = st.session_state.selected_program
    is_wait = st.session_state.get("is_waitlist", False)

    st.subheader(f"📝 {prog['name']} {'대기자' if is_wait else ''} 신청하기")
    st.success(f"📅 신청 날짜: **{prog['period']}** | 참가비: **{prog['price']:,}원**")

    col1, col2 = st.columns(2)
    with col1:
        이름 = st.text_input("이름", placeholder="오기석")
    with col2:
        전화번호 = st.text_input("전화번호", placeholder="010-1234-5678")

    col3, col4 = st.columns(2)
    with col3:
        이메일 = st.text_input("이메일", placeholder="example@email.com")
    with col4:
        생년월일 = st.date_input("생년월일", value=date(2000, 1, 1))

    요청사항 = st.text_area("추가 요청사항 (선택)", placeholder="예: 채식