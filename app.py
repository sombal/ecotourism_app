import streamlit as st
import pandas as pd
from datetime import datetime, date
import time
import re
import os
import json

st.set_page_config(page_title="생태관광 프로그램 신청", page_icon="🌿", layout="wide")

# ====================== 테마 ======================
st.markdown("""
    <style>
    .main {background-color: #f0f7f4 !important;}
    .program-card {background-color: white; padding: 25px; border-radius: 16px; 
                   box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px; border: 1px solid #e0e0e0;}
    .title {color: #1a5f3a; font-size: 46px; font-weight: bold; text-align: center; margin-bottom: 8px;}
    .subtitle {color: #2e7d32; text-align: center; font-size: 21px; margin-bottom: 35px;}
    .notice {background-color: #fff8e1; padding: 20px; border-radius: 12px; border-left: 6px solid #ffc107; margin-bottom: 30px;}
    .consent-box {background-color: #f0f8f0; padding: 20px; border-radius: 12px; border: 1px solid #c8e6c9;}
    </style>
""", unsafe_allow_html=True)

# ====================== 사이드바 ======================
menu = st.sidebar.selectbox(
    "📍 메뉴 선택",
    ["🏠 프로그램 목록", "🔄 내 신청 확인 / 취소", "🔑 관리자 페이지"]
)
st.sidebar.info("🌱 한국생태관광협회\n버전 6.1 - 프로그램 영구 저장")

# ====================== Persistent Disk ======================
DATA_DIR = "/data"
IMAGE_DIR = os.path.join(DATA_DIR, "images")
PROGRAM_FILE = os.path.join(DATA_DIR, "programs.json")
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

# ====================== 프로그램 영구 저장/로드 ======================
def load_programs():
    if os.path.exists(PROGRAM_FILE):
        try:
            with open(PROGRAM_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # deadline을 date 객체로 변환
                for p in data.values():
                    if isinstance(p.get("deadline"), str):
                        p["deadline"] = date.fromisoformat(p["deadline"])
                return data
        except:
            pass
    # 기본 프로그램
    return {
        1: {"name": "정기 생태관광(6월) 양구 1차", "period": "2026년 6월 10일 (수) (당일)", "desc": "양구 DMZ 속을 탐방하는 양구 생태관광 프로그램", "max": 12, "emoji": "🏔️", "deadline": date(2026, 6, 3), "price": "회원:30,000 / 비회원:50,000", "image": "https://raw.githubusercontent.com/sombal/ecotourism_app/main/images/1.jpg"},
        2: {"name": "정기 생태관광(6월) 양구 2차", "period": "2026년 6월 12일 (금) (당일)", "desc": "양구 DMZ 속을 탐방하는 양구 생태관광 프로그램", "max": 12, "emoji": "🌺", "deadline": date(2026, 6, 5), "price": "회원:30,000 / 비회원:50,000", "image": "https://raw.githubusercontent.com/sombal/ecotourism_app/main/images/2.png"},
        3: {"name": "정기 생태관광(6월) 양구 3차", "period": "2026년 6월 16일 (화) (당일)", "desc": "자연의 신비, 대암산 용늪으로 떠나는 양구 생태관광 프로그램", "max": 12, "emoji": "🏞️", "deadline": date(2026, 6, 1), "price": "회원:30,000 / 비회원:50,000", "image": "https://raw.githubusercontent.com/sombal/ecotourism_app/main/images/3.jpg"},
        4: {"name": "정기 생태관광(6월) 양구 4차", "period": "2026년 6월 25일 (목) (당일)", "desc": "자연의 신비, 대암산 용늪으로 떠나는 양구 생태관광 프로그램", "max": 12, "emoji": "🌲", "deadline": date(2026, 6, 10), "price": "회원:30,000 / 비회원:50,000", "image": "https://raw.githubusercontent.com/sombal/ecotourism_app/main/images/4.jpg"},
        5: {"name": "정기 생태관광(6월) 고창", "period": "2026년 6월 18일 (목) ~ 6월 19일 (금)", "desc": "나는 개똥벌레~ 여름을 맞이하는 반딧불이 생태관광 프로그램", "max": 20, "emoji": "🌲", "deadline": date(2026, 6, 11), "price": "회원:50,000 / 비회원:70,000", "image": "https://raw.githubusercontent.com/sombal/ecotourism_app/main/images/4.jpg"},
    }

def save_programs(programs):
    try:
        # date 객체를 문자열로 변환해서 저장
        data_to_save = {}
        for k, v in programs.items():
            data_to_save[k] = v.copy()
            if isinstance(data_to_save[k].get("deadline"), date):
                data_to_save[k]["deadline"] = data_to_save[k]["deadline"].isoformat()
        with open(PROGRAM_FILE, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

# ====================== 프로그램 로드 ======================
if "programs" not in st.session_state:
    st.session_state.programs = load_programs()

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
    for idx, prog in st.session_state.programs.items():
        current = len(df[df["프로그램"] == prog["name"]]) if not df.empty else 0
        wait_count = len(waitlist[waitlist["프로그램"] == prog["name"]]) if not waitlist.empty else 0
        is_closed = date.today() > prog["deadline"]
        is_full = current >= prog["max"]

        with cols[(idx-1) % 2]:
            with st.container(border=True):
                try:
                    st.image(prog["image"], width=600)
                except:
                    st.image("https://via.placeholder.com/600x220?text=사진+준비중", width=600)

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

    st.markdown("---")
    st.markdown('<div class="consent-box">', unsafe_allow_html=True)
    st.markdown("**📋 개인정보 제공 동의**")
    consent = st.checkbox("**개인정보 수집 및 이용에 동의합니다.** (필수)", 
                         help="이름, 연락처, 이메일 등 신청에 필요한 정보를 수집·이용하는 데 동의합니다.")

    st.markdown("""
    **수집하는 개인정보**  
    • 이름, 전화번호, 이메일, 생년월일  

    **이용 목적**  
    • 프로그램 신청 접수 및 참가자 관리  
    • 행사 안내 및 긴급 연락  

    **보유 기간**  
    • 프로그램 종료 후 1년간 보관 후 파기합니다.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("✅ 최종 신청하기" if not is_wait else "⏳ 대기자로 신청하기", 
                 type="primary", use_container_width=True, disabled=not consent):
        phone_pattern = r"^010-\d{4}-\d{4}$"
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not 이름 or not 전화번호 or not 이메일:
            st.error("모든 필수 항목을 입력해주세요.")
        elif not re.match(phone_pattern, 전화번호.strip()):
            st.error("전화번호 형식을 확인해주세요.")
        elif not re.match(email_pattern, 이메일.strip()):
            st.error("이메일 형식을 확인해주세요.")
        elif not consent:
            st.error("개인정보 제공 동의가 필요합니다.")
        else:
            신청시간 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            유형 = "대기자" if is_wait else "정상신청"
            current_wait = len(waitlist[waitlist["프로그램"] == prog["name"]]) if not waitlist.empty else 0
            대기순위 = current_wait + 1 if is_wait else None

            새신청 = pd.DataFrame([{
                "신청시간": 신청시간,
                "프로그램": prog["name"],
                "날짜": prog["period"],
                "이름": 이름.strip(),
                "전화번호": 전화번호.strip(),
                "이메일": 이메일.strip(),
                "생년월일": str(생년월일),
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

# ====================== 3. 관리자 페이지 ======================
elif menu == "🔑 관리자 페이지":
    st.title("🔑 관리자 페이지")

    if not st.session_state.is_admin_logged_in:
        admin_id = st.text_input("관리자 아이디", placeholder="admin")
        admin_pw = st.text_input("관리자 비밀번호", type="password")

        if st.button("로그인", type="primary", use_container_width=True):
            if admin_id.strip() == "admin" and admin_pw == "ecotour8677!":
                st.session_state.is_admin_logged_in = True
                st.success("✅ 로그인 성공!")
                st.rerun()
            else:
                st.error("❌ 아이디 또는 비밀번호가 틀렸습니다.")
    else:
        st.success("✅ 관리자 로그인 상태")
        if st.button("로그아웃"):
            st.session_state.is_admin_logged_in = False
            st.rerun()

        st.divider()
        tab1, tab2 = st.tabs(["📋 신청 관리", "📝 프로그램 관리"])

        with tab1:
            st.subheader("전체 신청 목록")
            if df.empty:
                st.info("아직 신청이 없습니다.")
            else:
                st.dataframe(df.sort_values(by="신청시간", ascending=False), use_container_width=True)

        with tab2:
            st.subheader("📝 프로그램 관리")

            # 새 프로그램 추가
            with st.expander("➕ 새 프로그램 추가"):
                n_name = st.text_input("프로그램 이름")
                n_period = st.text_input("기간")
                n_desc = st.text_area("설명")
                n_max = st.number_input("최대 인원", min_value=1, value=15)
                n_deadline = st.date_input("마감일")
                n_price = st.text_input("참가비")
                uploaded_file = st.file_uploader("사진 업로드", type=["jpg", "png", "jpeg"])

                if st.button("✅ 프로그램 추가"):
                    if n_name and n_period and uploaded_file:
                        image_path = os.path.join(IMAGE_DIR, uploaded_file.name)
                        with open(image_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        new_id = max(st.session_state.programs.keys()) + 1
                        st.session_state.programs[new_id] = {
                            "name": n_name, "period": n_period, "desc": n_desc,
                            "max": n_max, "emoji": "🌿", "deadline": n_deadline,
                            "price": n_price, "image": image_path
                        }
                        save_programs(st.session_state.programs)
                        st.success("✅ 새 프로그램이 추가되었습니다!")
                        st.rerun()

            # 기존 프로그램 관리
            for pid in list(st.session_state.programs.keys()):
                prog = st.session_state.programs[pid]
                with st.expander(f"📌 {prog['name']}"):
                    edit_name = st.text_input("이름", prog["name"], key=f"name_{pid}")
                    edit_period = st.text_input("기간", prog["period"], key=f"period_{pid}")
                    edit_desc = st.text_area("설명", prog["desc"], key=f"desc_{pid}")
                    uploaded_edit = st.file_uploader("사진 변경", type=["jpg","png","jpeg"], key=f"upload_{pid}")

                    if uploaded_edit:
                        image_path = os.path.join(IMAGE_DIR, uploaded_edit.name)
                        with open(image_path, "wb") as f:
                            f.write(uploaded_edit.getbuffer())
                        st.session_state.programs[pid]["image"] = image_path
                        st.success("✅ 사진이 변경되었습니다!")

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("💾 수정 저장", key=f"save_{pid}"):
                            st.session_state.programs[pid].update({
                                "name": edit_name,
                                "period": edit_period,
                                "desc": edit_desc
                            })
                            save_programs(st.session_state.programs)
                            st.success("✅ 수정 완료!")
                            st.rerun()
                    with col2:
                        if st.button("🗑 삭제", key=f"del_{pid}"):
                            del st.session_state.programs[pid]
                            save_programs(st.session_state.programs)
                            st.success("🗑 프로그램이 삭제되었습니다!")
                            st.rerun()

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
                        if st.button(f"❌ 취소하기", key=f"cn_{i}"):
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
                        if st.button(f"❌ 취소하기", key=f"cw_{i}"):
                            waitlist = waitlist.drop(i)
                            save_data(waitlist, "대기자목록.csv")
                            st.success("취소되었습니다!")
                            st.rerun()

# ====================== 사이트 하단 ======================
st.markdown("---")
st.markdown("""
    <p style="text-align: center; color: #666; font-size: 14px;">
        © 한국생태관광협회 | 
        <a href="#" style="color: #1a5f3a;">개인정보 보호정책</a>
    </p>
""", unsafe_allow_html=True)