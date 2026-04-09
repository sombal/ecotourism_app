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
st.sidebar.info("🌱 생태관광 프로그램 신청 시스템\n버전 1.0")

# ====================== 데이터 불러오기 ======================
try:
    df = pd.read_csv("신청목록.csv", encoding="utf-8-sig")
except:
    df = pd.DataFrame(columns=["신청시간", "프로그램", "날짜", "이름", "전화번호", "이메일", "생년월일", "요청사항", "금액"])

# ====================== 프로그램 목록 (메인 페이지) ======================
if menu == "🏠 프로그램 목록":
    st.markdown('<p class="title">🌿 생태관광</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">자연과 주민, 여행자가 함께하는 특별한 여행</p>', unsafe_allow_html=True)

    # 공지사항
    st.markdown("""
        <div class="notice">
            <strong>📢 공지사항 및 안내</strong><br>
            • 모든 프로그램은 <strong>선착순</strong>으로 진행됩니다.<br>
            • 취소는 신청일 기준 <strong>7일 전</strong>까지 가능합니다.<br>
            • 날씨에 따라 일정이 변경될 수 있습니다.<br>
            • 문의 : 02-723-8677
        </div>
    """, unsafe_allow_html=True)

    # 프로그램 정보 (여기서만 수정하면 됩니다!)
    programs = {
        1: {"name": "정기 생태관광(5월)", "period": "2026년 5월 22일 (금) ~ 23일 (토)", "desc": "대암산 용늪과 함께하는 양구 생태관광 프로그램", "max": 20, "emoji": "🏔️", "deadline": date(2026, 5, 7), "price": 60000, "image": "https://raw.githubusercontent.com/sombal/ecotourism-app/main/images/양구1.jpg"},
        2: {"name": "정기 생태관광(6월)", "period": "2026년 6월 19일 (금) ~ 20일 (토)", "desc": "고창의 주민들과 함께하는 힐링 생태관광 프로그램", "max": 20, "emoji": "🌺", "deadline": date(2026, 6, 11), "price": 60000, "image": "https://raw.githubusercontent.com/sombal/ecotourism-app/main/images/고창.jpg"},
        3: {"name": "정기 생태관광(7월)", "period": "2026년 7월 17일 (금) ~ 18일 (토)", "desc": "여름 하늘처럼 시원한 괴산호 트레킹 생태관광 프로그램", "max": 20, "emoji": "🏞️", "deadline": date(2026, 7, 9), "price": 60000, "image": "https://raw.githubusercontent.com/sombal/ecotourism-app/main/images/괴산.jpg"},
        4: {"name": "정기 생태관광(9월)", "period": "2026년 9월 11일 (금) ~ 12일 (토)", "desc": "국토 정중앙 양구의 가을을 만낄할 수 있는 생태관광 프로그램", "max": 20, "emoji": "🌲", "deadline": date(2026, 9, 3), "price": 60000, "image": "https://raw.githubusercontent.com/sombal/ecotourism-app/main/images/양구2.jpg"},
        5: {"name": "정기 생태관광(10월)", "period": "2026년 10월 16일 (금) ~ 17일 (토)", "desc": "생태수도, 순천만의 아름다운 가을을 만나볼 수 있는 생태관광 프로그램", "max": 20, "emoji": "🍁", "deadline": date(2026, 10, 7), "price": 60000, "image": "https://raw.githubusercontent.com/sombal/ecotourism-app/main/images/순천.jpg"}
    }

    cols = st.columns(2)

    for idx, prog in programs.items():
        current = len(df[df["프로그램"] == prog["name"]]) if not df.empty else 0
        is_closed = date.today() > prog["deadline"]
        is_full = current >= prog["max"]

        with cols[(idx-1) % 2]:
            with st.container(border=True):
                st.markdown(f'<img src="{prog["image"]}" class="program-image">', unsafe_allow_html=True)
                
                st.markdown(f"""
                    <h3>{prog['emoji']} {prog['name']}</h3>
                    <p><strong>📅 {prog['period']}</strong></p>
                    <p>{prog['desc']}</p>
                    <p><small>참가비: {prog['price']:,}원 | 최대 인원: {prog['max']}명 | 현재 신청: {current}명</small></p>
                """, unsafe_allow_html=True)

                if is_closed:
                    st.markdown(f'<p class="deadline">🔒 접수 마감되었습니다 ({prog["deadline"]})</p>', unsafe_allow_html=True)
                    st.button("신청 불가", disabled=True, use_container_width=True)
                elif is_full:
                    st.markdown('<p class="full">🔒 정원이 마감되었습니다</p>', unsafe_allow_html=True)
                    st.button("신청 불가", disabled=True, use_container_width=True)
                else:
                    if st.button(f"✨ {prog['name']} 신청하기", key=f"apply_{idx}", use_container_width=True):
                        st.session_state.selected_program = prog
                        st.rerun()

    # 신청 폼
    if "selected_program" in st.session_state:
        prog = st.session_state.selected_program
        st.divider()
        st.subheader(f"📝 {prog['name']} 신청하기")
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

        요청사항 = st.text_area("추가 요청사항 (선택)", placeholder="예: 채식 식사 부탁드려요")

        if st.button("✅ 최종 신청하기", type="primary", use_container_width=True):
            if 이름.strip() and 전화번호.strip() and 이메일.strip():
                신청시간 = datetime.now().strftime("%Y-%m-%d %H:%M")
                
                새신청 = pd.DataFrame([{
                    "신청시간": 신청시간,
                    "프로그램": prog["name"],
                    "날짜": prog["period"],
                    "이름": 이름.strip(),
                    "전화번호": 전화번호.strip(),
                    "이메일": 이메일.strip(),
                    "생년월일": 생년월일,
                    "요청사항": 요청사항,
                    "금액": prog["price"]
                }])
                
                if df.empty:
                    새신청.to_csv("신청목록.csv", index=False, encoding="utf-8-sig")
                else:
                    pd.concat([df, 새신청], ignore_index=True).to_csv("신청목록.csv", index=False, encoding="utf-8-sig")
                
                st.balloons()
                st.success(f"🎉 {이름.strip()}님! {prog['name']} 신청이 완료되었습니다!")
                
                time.sleep(2)
                del st.session_state.selected_program
                st.rerun()
            else:
                st.error("이름, 전화번호, 이메일을 모두 입력해주세요!")

# ====================== 내 신청 확인 / 취소 ======================
elif menu == "🔄 내 신청 확인 / 취소":
    st.title("🔄 내 신청 확인 / 취소")
    phone = st.text_input("📱 전화번호를 입력하세요", placeholder="010-1234-5678")

    if phone:
        my_df = df[df["전화번호"].astype(str).str.strip() == phone.strip()]
        if my_df.empty:
            st.warning("해당 전화번호로 신청된 내용이 없습니다.")
        else:
            for i, row in my_df.iterrows():
                with st.container(border=True):
                    st.write(f"**{row['프로그램']}** | {row['날짜']} | {row.get('금액', 0):,}원")
                    st.write(f"신청일시: {row['신청시간']}")
                    if st.button(f"❌ 이 신청 취소하기", key=f"cancel_{i}"):
                        df = df.drop(i)
                        df.to_csv("신청목록.csv", index=False, encoding="utf-8-sig")
                        st.success("✅ 신청이 취소되었습니다!")
                        st.rerun()

# ====================== 관리자 페이지 ======================
elif menu == "🔑 관리자 페이지":
    st.title("🔑 관리자 페이지")
    st.write("관리자 전용 페이지입니다. (아이디: admin / 비밀번호: admin1234)")

    admin_id = st.text_input("관리자 아이디", placeholder="admin")
    admin_pw = st.text_input("관리자 비밀번호", type="password")

    if st.button("로그인", type="primary", use_container_width=True):
        if admin_id == "admin" and admin_pw == "admin1234":
            st.success("✅ 관리자 로그인 성공!")
            st.divider()
            st.subheader("📊 전체 신청 관리")

            if df.empty:
                st.info("아직 신청된 내용이 없습니다.")
            else:
                search_term = st.text_input("🔍 검색 (이름, 전화번호, 프로그램명)", "")
                if search_term:
                    filtered_df = df[
                        df["이름"].astype(str).str.contains(search_term, case=False, na=False) |
                        df["전화번호"].astype(str).str.contains(search_term, case=False, na=False) |
                        df["프로그램"].astype(str).str.contains(search_term, case=False, na=False)
                    ]
                else:
                    filtered_df = df

                st.dataframe(filtered_df.sort_values(by="신청시간", ascending=False), use_container_width=True, height=700)
                st.success(f"총 {len(filtered_df)} 건의 신청이 있습니다.")
                
                csv = filtered_df.to_csv(index=False, encoding="utf-8-sig")
                st.download_button("📥 전체 신청 목록 다운로드", csv, "전체_신청목록.csv", "text/csv")
        else:
            st.error("❌ 아이디 또는 비밀번호가 틀렸습니다.")