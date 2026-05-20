import streamlit as st
import pandas as pd
from datetime import datetime, date
import time
import re
import os

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
st.sidebar.info("🌱 한국생태관광협회\n버전 4.0 - 프로그램 쉽게 수정")

# ====================== Persistent Disk ======================
DATA_DIR = "/data"
try:
    os.makedirs(DATA_DIR, exist_ok=True)
except:
    DATA_DIR = "/tmp/data"
    os.makedirs(DATA_DIR, exist_ok=True)

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

# 데이터 로드
df = load_data("신청목록.csv", ["신청시간", "프로그램", "날짜", "이름", "전화번호", "이메일", "생년월일", "요청사항", "금액", "유형"])
waitlist = load_data("대기자목록.csv", ["신청시간", "프로그램", "날짜", "이름", "전화번호", "이메일", "생년월일", "요청사항", "금액", "유형", "대기순위"])

# ====================== 프로그램 관리 (세션 상태) ======================
if "programs" not in st.session_state:
    st.session_state.programs = {
        1: {"name": "정기 생태관광(6월) 양구 1차", "period": "2026년 6월 10일 (수) (당일)", "desc": "양구 DMZ 속을 탐방하는 양구 생태관광 프로그램", "max": 12, "emoji": "🏔️", "deadline": date(2026, 6, 3), "price": "회원:30,000 / 비회원:50,000", "image": "https://raw.githubusercontent.com/sombal/ecotourism_app/main/images/1.jpg"},
        2: {"name": "정기 생태관광(6월) 양구 2차", "period": "2026년 6월 12일 (금) (당일)", "desc": "양구 DMZ 속을 탐방하는 양구 생태관광 프로그램", "max": 12, "emoji": "🌺", "deadline": date(2026, 6, 5), "price": "회원:30,000 / 비회원:50,000", "image": "https://raw.githubusercontent.com/sombal/ecotourism_app/main/images/2.png"},
        3: {"name": "정기 생태관광(6월) 양구 3차", "period": "2026년 6월 16일 (화) (당일)", "desc": "자연의 신비, 대암산 용늪으로 떠나는 양구 생태관광 프로그램", "max": 12, "emoji": "🏞️", "deadline": date(2026, 6, 1), "price": "회원:30,000 / 비회원:50,000", "image": "https://raw.githubusercontent.com/sombal/ecotourism_app/main/images/3.jpg"},
        4: {"name": "정기 생태관광(6월) 양구 4차", "period": "2026년 6월 25일 (목) (당일)", "desc": "자연의 신비, 대암산 용늪으로 떠나는 양구 생태관광 프로그램", "max": 12, "emoji": "🌲", "deadline": date(2026, 6, 10), "price": "회원:30,000 / 비회원:50,000", "image": "https://raw.githubusercontent.com/sombal/ecotourism_app/main/images/4.jpg"},
        5: {"name": "정기 생태관광(6월) 고창", "period": "2026년 6월 18일 (목) ~ 6월 19일 (금)", "desc": "나는 개똥벌레~ 여름을 맞이하는 반딧불이 생태관광 프로그램", "max": 20, "emoji": "🌲", "deadline": date(2026, 6, 11), "price": "회원:50,000 / 비회원:70,000", "image": "https://raw.githubusercontent.com/sombal/ecotourism_app/main/images/4.jpg"},
    }

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
    for idx, prog in st.session_state.programs.items():
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

# ====================== 2. 신청 페이지 ======================
elif st.session_state.page == "apply":
    if st.session_state.selected_program is None:
        st.error("잘못된 접근입니다.")
        if st.button("← 돌아가기"):
            st.session_state.page = "main"
            st.rerun()
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

    if st.button("✅ 최종 신청하기" if not is_wait else "⏳ 대기자로 신청하기", type="primary", use_container_width=True):
        phone_pattern = r"^010-\d{4}-\d{4}$"
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not 이름.strip():
            st.error("이름을 입력해주세요.")
        elif not re.match(phone_pattern, 전화번호.strip()):
            st.error("전화번호는 '010-1234-5678' 형식으로 입력해주세요.")
        elif not re.match(email_pattern, 이메일.strip()):
            st.error("올바른 이메일 형식을 입력해주세요.")
        else:
            신청시간 = datetime.now().strftime("%Y-%m-%d %H:%M")
            유형 = "대기자" if is_wait else "정상신청"
            current_wait = len(waitlist[waitlist["프로그램"] == prog["name"]]) if not waitlist.empty else 0
            대기순위 = current_wait + 1 if is_wait else None

            새신청 = pd.DataFrame([{
                "신청시간": 신청시간, "프로그램": prog["name"], "날짜": prog["period"],
                "이름": 이름.strip(), "전화번호": 전화번호.strip(), "이메일": 이메일.strip(),
                "생년월일": 생년월일, "요청사항": 요청사항, "금액": prog["price"],
                "유형": 유형, "대기순위": 대기순위
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

# ====================== 3. 관리자 페이지 (프로그램 관리 포함) ======================
elif menu == "🔑 관리자 페이지":
    st.title("🔑 관리자 페이지")
    admin_id = st.text_input("관리자 아이디", placeholder="admin")
    admin_pw = st.text_input("관리자 비밀번호", type="password")

    if st.button("로그인", type="primary", use_container_width=True):
        if admin_id.strip() == "admin" and admin_pw == "ecotour8677!":
            st.success("✅ 관리자 로그인 성공!")
            st.divider()

            tab1, tab2, tab3 = st.tabs(["📋 전체 신청", "📝 프로그램 관리", "⏳ 대기자 목록"])

            with tab1:
                st.subheader("전체 신청 목록")
                if df.empty:
                    st.info("아직 신청이 없습니다.")
                else:
                    st.dataframe(df.sort_values(by="신청시간", ascending=False), use_container_width=True)
                    csv = df.to_csv(index=False, encoding="utf-8-sig")
                    st.download_button("📥 CSV 다운로드", csv, "전체신청목록.csv", "text/csv")

            with tab2:
                st.subheader("📝 프로그램 관리")
                st.info("여기서 프로그램을 추가·수정·삭제할 수 있습니다.")

                # 새 프로그램 추가
                with st.expander("➕ 새 프로그램 추가"):
                    n_name = st.text_input("프로그램 이름*")
                    n_period = st.text_input("기간* (예: 2026년 8월 10일)")
                    n_desc = st.text_area("설명*")
                    n_max = st.number_input("최대 인원*", min_value=1, value=15)
                    n_deadline = st.date_input("신청 마감일*")
                    n_price = st.text_input("참가비*", "회원:30,000 / 비회원:50,000")
                    n_image = st.text_input("사진 URL*", "https://raw.githubusercontent.com/sombal/ecotourism_app/main/images/new.jpg")

                    if st.button("✅ 프로그램 추가하기"):
                        if n_name and n_period and n_desc:
                            new_id = max(st.session_state.programs.keys()) + 1
                            st.session_state.programs[new_id] = {
                                "name": n_name, "period": n_period, "desc": n_desc,
                                "max": int(n_max), "emoji": "🌿", "deadline": n_deadline,
                                "price": n_price, "image": n_image
                            }
                            st.success("새 프로그램이 추가되었습니다!")
                            st.rerun()

                # 기존 프로그램 수정/삭제
                st.subheader("기존 프로그램 목록")
                for pid, p in list(st.session_state.programs.items()):
                    with st.expander(f"📌 {p['name']}"):
                        edit_name = st.text_input("이름", p['name'], key=f"e_name_{pid}")
                        edit_period = st.text_input("기간", p['period'], key=f"e_period_{pid}")
                        edit_desc = st.text_area("설명", p['desc'], key=f"e_desc_{pid}")
                        edit_image = st.text_input("사진 URL", p['image'], key=f"e_image_{pid}")

                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button("💾 수정 저장", key=f"save_{pid}"):
                                st.session_state.programs[pid] = {**p, "name": edit_name, "period": edit_period, 
                                                                "desc": edit_desc, "image": edit_image}
                                st.success("수정 완료!")
                                st.rerun()
                        with col_b:
                            if st.button("🗑 삭제", key=f"del_{pid}"):
                                if st.checkbox("정말 삭제하시겠습니까?", key=f"chk_{pid}"):
                                    del st.session_state.programs[pid]
                                    st.success("프로그램이 삭제되었습니다!")
                                    st.rerun()

            with tab3:
                st.subheader("대기자 목록")
                st.dataframe(waitlist, use_container_width=True)

        else:
            st.error("❌ 로그인 정보가 올바르지 않습니다.")

# ====================== 4. 내 신청 확인 / 취소 ======================
elif menu == "🔄 내 신청 확인 / 취소":
    st.title("🔄 내 신청 확인 / 취소")
    phone = st.text_input("📱 전화번호를 입력하세요", placeholder="010-1234-5678")

    if phone:
        my_normal = df[df["전화번호"].astype(str).str.strip() == phone.strip()]
        my_wait = waitlist[waitlist["전화번호"].astype(str).str.strip() == phone.strip()] if not waitlist.empty else pd.DataFrame()

        if my_normal.empty and my_wait.empty:
            st.warning("신청 내역이 없습니다.")
        else:
            if not my_normal.empty:
                st.subheader("✅ 정상 신청")
                for i, row in my_normal.iterrows():
                    with st.container(border=True):
                        st.write(f"**{row['프로그램']}** | {row['날짜']}")
                        st.write(f"신청일시: {row['신청시간']}")
                        if st.button(f"❌ 취소하기", key=f"cancel_n_{i}"):
                            df = df.drop(i)
                            save_data(df, "신청목록.csv")
                            st.success("취소되었습니다!")
                            st.rerun()

            if not my_wait.empty:
                st.subheader("⏳ 대기자 신청")
                for i, row in my_wait.iterrows():
                    with st.container(border=True):
                        st.write(f"**{row['프로그램']}** 대기자 | {row.get('대기순위', '')}순위")
                        st.write(f"신청일시: {row['신청시간']}")
                        if st.button(f"❌ 취소하기", key=f"cancel_w_{i}"):
                            waitlist = waitlist.drop(i)
                            save_data(waitlist, "대기자목록.csv")
                            st.success("대기자 신청이 취소되었습니다!")
                            st.rerun()