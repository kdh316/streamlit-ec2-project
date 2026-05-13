import streamlit as st

st.title("10년 전 가격 맞추기 퀴즈")
st.write("학번: 2022204015")
st.write("이름: 김도형")

@st.cache_data
def load_quiz():
    return [
        {"name": "과자 짱구", "old_price": 1000, "new_price": 1700, "image": "짱구.jpg"},
        {"name": "삼각김밥", "old_price": 900, "new_price": 1200, "image": "삼각김밥.jpg"},
        {"name": "황금올리브 치킨", "old_price": 18000, "new_price": 23000, "image": "황올.jpg"},
        {"name": "짜장면", "old_price": 4500, "new_price": 7000, "image": "짜장면.jpg"},
        {"name": "영화티켓(주말)", "old_price": 9000, "new_price": 15000, "image": "영화티켓.jpg"},
        {"name": "대중교통", "old_price": 1200, "new_price": 1500, "image": "대중교통.jpg"}
    ]

quiz_data = load_quiz()

if "login" not in st.session_state:
    st.session_state.login = False
if "current" not in st.session_state:
    st.session_state.current = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "total_error_percent" not in st.session_state:
    st.session_state.total_error_percent = 0
if "show_result" not in st.session_state:
    st.session_state.show_result = False
if "user_answer" not in st.session_state:
    st.session_state.user_answer = 0
if "result_message" not in st.session_state:
    st.session_state.result_message = ""

if st.session_state.login == False:
    st.subheader("로그인")

    user_id = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        if user_id == "2022204015" and password == "1234":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("로그인 실패")

else:
    current = st.session_state.current

    if current < len(quiz_data):
        quiz = quiz_data[current]

        if st.session_state.show_result == False:
            st.subheader(f"문제 {current + 1} / {len(quiz_data)}")
            st.write("현재 가격을 보고 **10년 전 가격**을 맞춰보세요.")

            col1, col2 = st.columns(2)

            with col1:
                st.image(quiz["image"], width=250)

            with col2:
                st.markdown(f"### {quiz['name']}")
                st.metric("현재 가격", f"{quiz['new_price']}원")

                user_answer = st.number_input(
                    "10년 전 가격 입력",
                    min_value=0,
                    step=100
                )

                if st.button("정답 확인"):
                    answer = quiz["old_price"]
                    error = abs(user_answer - answer)
                    error_percent = error / answer * 100

                    st.session_state.user_answer = user_answer
                    st.session_state.error_percent = error_percent
                    st.session_state.total_error_percent += error_percent

                    if error_percent == 0:
                        st.session_state.score += 3
                        st.session_state.result_message = "정답입니다! 완벽한 물가 감각입니다."
                    elif error_percent <= 10:
                        st.session_state.score += 2
                        st.session_state.result_message = "거의 맞았습니다! 꽤 정확합니다."
                    elif error_percent <= 30:
                        st.session_state.score += 1
                        st.session_state.result_message = "조금 차이가 있지만 방향은 괜찮습니다."
                    else:
                        st.session_state.result_message = "오차가 큽니다. 과거 가격이 생각보다 달랐습니다."

                    st.session_state.show_result = True
                    st.rerun()

        else:
            col1, col2, col3 = st.columns([1.2, 2, 1])

            with col2:
                st.image(quiz["image"], width=250)

            col4, col5, col6 = st.columns([2, 2, 1])

            with col5:
                st.metric("10년 전 가격", f"{quiz['old_price']}원")

            st.write(f"오차율: **{st.session_state.error_percent:.1f}%**")

            if st.session_state.error_percent == 0:
                st.success(st.session_state.result_message)
            elif st.session_state.error_percent <= 10:
                st.info(st.session_state.result_message)
            elif st.session_state.error_percent <= 30:
                st.warning(st.session_state.result_message)
            else:
                st.error(st.session_state.result_message)

            if st.button("다음 문제"):
                st.session_state.current += 1
                st.session_state.show_result = False
                st.rerun()

    else:
        st.subheader("최종 결과")

        average_error = st.session_state.total_error_percent / len(quiz_data)
        final_score = max(0, 100 - average_error)

        st.write(f"최종 점수: **{final_score:.1f}점 / 100점**")
        st.write(f"평균 오차율: **{average_error:.1f}%**")

        st.progress(int(final_score))

        if final_score >= 90:
            st.success("물가 기억력 만점 수준입니다!")
        elif final_score >= 75:
            st.info("과거 가격 감각이 뛰어납니다.")
        elif final_score >= 60:
            st.warning("평균적인 가격 감각입니다.")
        else:
            st.error("현재 물가에 익숙해져 과거 가격 기억이 흐려졌습니다.")

        if st.button("다시 시작"):
            st.session_state.current = 0
            st.session_state.score = 0
            st.session_state.total_error_percent = 0
            st.session_state.show_result = False
            st.session_state.user_answer = 0
            st.session_state.result_message = ""
            st.rerun()