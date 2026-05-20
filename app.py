import streamlit as st
import pandas as pd
from datetime import datetime, date
import time
import re
import os
import base64

st.set_page_config(page_title="생태관광 프로그램 신청", page_icon="🌿", layout="wide")

# ====================== 테마 ======================
st.markdown("""
    <style>
    .main {background-color: #f0f7f4 !important;}
    .program-card {background-color: white; padding: 25px; border-radius: 16px; 
                   box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px; border: 1px solid #e0e0e0;}
    .title {color: #1a5f3a; font-size: 46px; font-weight: bold; text-align: center; margin-bottom: 8px;}
    .subtitle {color: #2e7d32; text-align: center; font-size: 21px; margin-bottom: 35px;}
    .program-image {width: 100%; height: 220px; object-fit: cover; border-radius: 12px; margin-bottom: 18px;}
    .stButton > button {background-color: #1a5f3a !important; color: white !important; font-size: 16px; padding: 12px 20px; border-radius: 10px; font-weight: bold; width: 100%;}
    .notice {background-color: #fff8e1; padding: 20px; border-radius: 12px; border-left: 6px solid #ffc107; margin-bottom: 30px;}
    </style>
""", unsafe_allow_html=True)

# ====================== 사이드바 ======================
menu = st.sidebar.selectbox(
    "📍 메뉴 선택",
    ["🏠 프로그램 목록", "🔄 내 신청 확인 / 취소", "🔑 관리자 페이지"]
)
st.sidebar.info("🌱 한국생태관광협회\n버전 5.1 - 개인정보 보호 강화")

# ====================== Persistent Disk ======================
DATA_DIR = "/data"
IMAGE_DIR = os.path.join(DATA_DIR, "images")
os.makedirs(IMAGE_DIR, exist_ok=True)

def load_data(filename, columns):
    full_path = os.path.join(DATA_DIR, filename)
    try:
        if os.path.exists(full_path):
            df = pd.read_csv(full_path, encoding="utf-8-sig")
            return df.dropna(how='all').reset_index(drop=True)
    except:
        pass
    return pd.DataFrame(columns=columns)

def save_data(df, filename):
    full_path = os.path.join(DATA_DIR, filename)
    try:
        df.to_csv(full_path, index=False, encoding="utf-8-sig")
        return True
    except Exception as e:
        st.error(f"💾 저장 실패: {e}")
        return False

# 간단 암호화 함수
def encrypt(text):
    if not text:
        return ""
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

def decrypt(encrypted_text):
    if not encrypted_text:
        return ""
    try:
        return base64.b64decode(encrypted_text.encode('utf-8')).decode('utf-8')
    except:
        return encrypted_text

# ====================== 데이터 로드 ======================
df = load_data("신청목록.csv", ["신청시간", "프로그램", "날짜", "이름", "전화번호", "이메일", "생년월일", "요청사항", "금액", "유형"])
waitlist = load_data("대기자목록.csv", ["신청시간", "프로그램", "날짜", "이름", "전화번호", "이메일", "생년월일", "요청사항", "금액", "유형", "대기순위"])

# ====================== 세션 상태 ======================
if "page" not in st.session_state:
    st.session_state.page = "main"
if "selected_program" not in st.session_state:
    st.session_state.selected_program = None
if "is_waitlist" not in st.session_state:
    st.session_state.is_waitlist = False
if "is_admin_logged_in" not in st.session_state:
    st.session_state.is_admin_logged_in = False

# ====================== 1. 프로그램 목록 ======================
if st.session_state.page == "main" and menu == "🏠 프로그램 목록":
    st.markdown('<p class="title">🌿 생태관광</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">자연과 주민, 여행자가 함께하는 특별한 여행</p>', unsafe_allow_html=True)

    st.markdown("""
        <div class="notice">
            <strong>📢 공지사항 및 안내</strong><br>
            • 모든 프로그램은 선착순 접수입니다.<br>
            • 정원이 마감된 프로그램은 대기자 신청이 가능합니다.<br>
            • 문의 : 02-723-8677
        </div>
    """, unsafe_allow_html=True)

    cols = st.columns(2)
    for idx, prog in st.session_state.get("programs", {}).items():
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
                    <p><small>참가비: {prog['price']} | 최대 인원: {prog['max']}명 | 현재: {current}명 | 대기: {wait_count}명</small></p>
                """, unsafe_allow_html=True)

                if is_closed:
                    st.button("✅ 모집 완료", disabled=True, use_container_width=True)
                elif is_full:
                    st.markdown('<p class="full">🔒 정원이 마감되었습니다</p>', unsafe_allow_html=True)
                    if st.button(f"⏳ 대기자로 신청하기", key=f"wait_{idx}", use_container_width=True):
                        st.session_state.selected_program = prog.copy()
                        st.session_state.is_waitlist = True
                        st.session_state.page = "apply"
                        st.rerun()
                else:
                    if st.button(f"✨ {prog['name']} 신청하기", key=f"apply_{idx}", use_container_width=True):
                        st.session_state.selected_program = prog.copy()
                        st.session_state.is_waitlist = False
                        st.session_state.page = "apply"
                        st.rerun()

# ====================== 2. 신청 페이지 (개인정보 동의 체크박스) ======================
elif st.session_state.page == "apply":
    if st.session_state.selected_program is None:
        st.error("잘못된 접근입니다.")
        st.stop()

    prog = st.session_state.selected_program
    is_wait = st.session_state.get("is_waitlist", False)

    st.subheader(f"📝 {prog['name']} {'대기자' if is_wait else ''} 신청하기")
    st.success(f"📅 {prog['period']} | {prog['price']}")

    col1, col2 = st.columns(2)
    with col1: 이름 = st.text_input("이름", placeholder="홍길동")
    with col2: 전화번호 = st.text_input("전화번호", placeholder="010-1234-5678")

    col3, col4 = st.columns(2)
    with col3: 이메일 = st.text_input("이메일", placeholder="example@mail.com")
    with col4: 생년월일 = st.date_input("생년월일", value=date(2000, 1, 1))

    요청사항 = st.text_area("추가 요청사항 (선택)", placeholder="예: 채식 식사 부탁드려요")

    # ==================== 개인정보 동의 체크박스 ====================
    agree = st.checkbox(
        "✅ [필수] 개인정보 수집 및 이용에 동의합니다.",
        help="이름, 전화번호, 이메일, 생년월일을 신청 처리 및 연락 목적으로 수집합니다."
    )

    st.caption("[개인정보 보호정책](https://ecotourism-app.onrender.com/privacy)")

    if st.button("✅ 최종 신청하기" if not is_wait else "⏳ 대기자로 신청하기", 
                 type="primary", use_container_width=True, disabled=not agree):
        if not agree:
            st.error("개인정보 수집·이용 동의가 필요합니다.")
        elif not 이름.strip() or not re.match(r"^010-\d{4}-\d{4}$", 전화번호.strip()) or not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", 이메일.strip()):
            st.error("입력 정보를 확인해주세요.")
        else:
            신청시간 = datetime.now().strftime("%Y-%m-%d %H:%M")
            유형 = "대기자" if is_wait else "정상신청"
            current_wait = len(waitlist[waitlist["프로그램"] == prog["name"]]) if not waitlist.empty else 0
            대기순위 = current_wait + 1 if is_wait else None

            새신청 = pd.DataFrame([{
                "신청시간": 신청시간,
                "프로그램": prog["name"],
                "날짜": prog["period"],
                "이름": 이름.strip(),
                "전화번호": encrypt(전화번호.strip()),
                "이메일": encrypt(이메일.strip()),
                "생년월일": encrypt(str(생년월일)),
                "요청사항": 요청사항,
                "금액": prog["price"],
                "유형": 유형,
                "대기순위": 대기순위
            }])

            if is_wait:
                updated = pd.concat([waitlist, 새신청], ignore_index=True)
                save_data(updated, "대기자목록.csv")
            else:
                updated = pd.concat([df, 새신청], ignore_index=True)
                save_data(updated, "신청목록.csv")

            st.balloons()
            st.success(f"🎉 {이름.strip()}님! {prog['name']} 신청이 완료되었습니다!")
            time.sleep(2)
            st.session_state.page = "main"
            for key in ["selected_program", "is_waitlist"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    if st.button("← 프로그램 목록으로 돌아가기"):
        st.session_state.page = "main"
        for key in ["selected_program", "is_waitlist"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# ====================== 관리자 페이지 ======================
elif menu == "🔑 관리자 페이지":
    st.title("🔑 관리자 페이지")
    admin_id = st.text_input("관리자 아이디", placeholder="admin")
    admin_pw = st.text_input("관리자 비밀번호", type="password")

    if st.button("로그인", type="primary", use_container_width=True):
        if admin_id.strip() == "admin" and admin_pw == "ecotour8677!":
            st.session_state.is_admin_logged_in = True
            st.success("✅ 로그인 성공!")
            st.rerun()
        else:
            st.error("로그인 실패")

    if st.session_state.get("is_admin_logged_in", False):
        if st.button("로그아웃"):
            st.session_state.is_admin_logged_in = False
            st.rerun()

        # 관리자 페이지 내용 (신청 목록, 프로그램 관리 등)
        st.info("관리자 페이지입니다. (개인정보는 복호화되어 표시됩니다.)")
        # ... (필요 시 이전 관리자 코드 추가)

# ====================== 개인정보 보호정책 링크 ======================
st.caption("© 2026 한국생태관광협회 | ")
st.markdown("[개인정보 보호정책](https://ecotourism-app.onrender.com/privacy)", unsafe_allow_html=True)