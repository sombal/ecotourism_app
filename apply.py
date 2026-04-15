import streamlit as st
import pandas as pd
from datetime import datetime, date
import time

st.title("📝 신청하기")

if "selected_program" not in st.session_state:
    st.error("잘못된 접근입니다. 프로그램 목록에서 신청하기 버튼을 눌러주세요.")
    st.stop()

prog = st.session_state.selected_program
is_wait = st.session_state.get("is_waitlist", False)

st.subheader(f"{prog['name']} {'대기자' if is_wait else ''} 신청")

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

요청사항 = st.text_area("추가 요청사항", placeholder="예: 채식 식사 부탁드려요")

if st.button("✅ 신청 완료하기", type="primary"):
    if 이름 and 전화번호 and 이메일:
        # 여기서 데이터 저장 로직 (기존 코드와 동일)
        st.success("신청이 완료되었습니다!")
        time.sleep(2)
        st.switch_page("app.py")
    else:
        st.error("필수 정보를 모두 입력해주세요.")