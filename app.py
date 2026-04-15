import streamlit as st
import pandas as pd
from datetime import datetime, date
import time

st.set_page_config(page_title="생태관광 프로그램 신청", page_icon="🌿", layout="wide")

st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .program-card {background-color: white; padding: 20px; border-radius: 12px; 
                   box-shadow: 0 3px 10px rgba(0,0,0,0.08); margin-bottom: 15px; border: 1px solid #e0e0e0;}
    .title {color: #1a5f3a; font-size: 42px; font-weight: bold; text-align: center; margin-bottom: 10px;}
    .subtitle {color: #2e7d32; text-align: center; font-size: 20px; margin-bottom: 30px;}
    .program-image {width: 100%; height: 210px; object-fit: cover; border-radius: 10px; margin-bottom: 15px;}
    .deadline {color: #d32f2f; font-weight: bold;}
    .full {color: #d32f2f; font-weight: bold;}
    .notice {background-color: #fff3cd; padding: 18px; border-radius: 10px; border-left: 6px solid #ffc107; margin-bottom: 25px;}
    </style>
""", unsafe_allow_html=True)

# ====================== 사이드바 ======================
menu = st.sidebar.selectbox(
    "📍 메뉴 선택",
    ["🏠 프로그램 목록", "🔄 내 신청 확인 / 취소", "🔑 관리자 페이지"]
)
st.sidebar.info("🌱 생태관광 프로그램 신청 시스템\n버전 1.3 - 별도 신청 페이지")

# ====================== 데이터 불러오기 ======================
try:
    df = pd.read_csv("신청목록.csv", encoding="utf-8-sig")
except:
    df = pd.DataFrame(columns=["신청시간", "프로그램", "날짜", "이름", "전화번호", "이메일", "생년월일", "요청사항", "금액", "유형"])

try:
    waitlist = pd.read_csv("대기자목록.csv", encoding="utf-8-sig")
except:
    waitlist = pd.DataFrame(columns=["신청시간", "프로그램", "날짜", "이름", "전화번호", "이메일", "생년월일", "요청사항", "금액", "유형", "대기순위"])

# ====================== 프로그램 목록 ======================
if menu == "🏠 프로그램 목록":
    st.markdown('<p class="title">🌿 생태관광</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">자연과 주민, 여행자가 함께하는 특별한 여행</p>', unsafe_allow_html=True)

    st.markdown("""
        <div class="notice">
            <strong>📢 공지사항 및 안내</strong><br>
            • 모든 프로그램은 <strong>선착순</strong>으로 진행됩니다.<br>
            • 정원이 마감된 프로그램은 <strong>대기자 신청</strong>이 가능합니다.<br>
            • 대기자는 신청 순서대로 우선순위가 부여됩니다.<br>
            • 문의 : 02-723-8677
        </div>
    """, unsafe_allow_html=True)

    programs = {
        1: {"name": "정기 생태관광(5월)", "period": "2026년 5월 22일 (금) ~ 23일 (토)", "desc": "대암산 용늪과 함께하는 양구 생태관광 프로그램", "max": 20, "emoji": "🏔️", "deadline": date(2026, 5, 7), "price": 60000, "image": "https://raw.githubusercontent.com/sombal/ecotourism-app/main/images/1.jpg"},
        2: {"name": "정기 생태관광(6월)", "period": "2026년 6월 19일 (금) ~ 20일 (토)", "desc": "고창의 주민들과 함께하는 힐링 생태관광 프로그램", "max": 20, "emoji": "🌺", "deadline": date(2026, 6, 11), "price": 60000, "image": "https://raw.githubusercontent.com/sombal/ecotourism-app/main/images/2.png"},
        3: {"name": "정기 생태관광(7월)", "period": "2026년 7월 17일 (금) ~ 18일 (토)", "desc": "여름 하늘처럼 시원한 괴산호 트레킹 생태관광 프로그램", "max": 20, "emoji": "🏞️", "deadline": date(2026, 7, 9), "price": 60000, "image": "https://raw.githubusercontent.com/sombal/ecotourism-app/main/images/3.jpg"},
        4: {"name": "정기 생태관광(9월)", "period": "2026년 9월 11일 (금) ~ 12일 (토)", "desc": "국토 정중앙 양구의 가을을 만끽할 수 있는 생태관광 프로그램", "max": 20, "emoji": "🌲", "deadline": date(2026, 9, 3), "price": 60000, "image": "https://raw.githubusercontent.com/sombal/ecotourism-app/main/images/4.jpg"},
        5: {"name": "정기 생태관광(10월)", "period": "2026년 10월 16일 (금) ~ 17일 (토)", "desc": "생태수도, 순천만의 아름다운 가을을 만나볼 수 있는 생태관광 프로그램", "max": 20, "emoji": "🍁", "deadline": date(2026, 10, 7), "price": 60000, "image": "https://raw.githubusercontent.com/sombal/ecotourism-app/main/images/5.jpg"}
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
                        st.switch_page("신청하기.py")   # ← 여기서 별도 페이지로 이동
                else:
                    if st.button(f"✨ {prog['name']} 신청하기", key=f"apply_{idx}", use_container_width=True):
                        st.session_state.selected_program = prog
                        st.session_state.is_waitlist = False
                        st.switch_page("신청하기.py")   # ← 별도 페이지로 이동

# ====================== 나머지 메뉴 ======================
elif menu == "🔄 내 신청 확인 / 취소":
    st.title("🔄 내 신청 확인 / 취소")
    phone = st.text_input("📱 전화번호를 입력하세요", placeholder="010-1234-5678")
    # (기존 코드 유지)

elif menu == "🔑 관리자 페이지":
    st.title("🔑 관리자 페이지")
    # (기존 코드 유지)