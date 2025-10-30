import streamlit as st
import random

# 로또 번호 생성 함수
def generate_lotto_numbers():
    """1부터 45 사이의 중복 없는 6개 숫자를 생성합니다."""
    # random.sample(population, k) 함수는 population에서 k개의 고유한 요소를 무작위로 선택합니다.
    return sorted(random.sample(range(1, 46), 6))

# Streamlit 앱 설정
st.title("🍀 대한민국 로또 6/45 번호 생성기")
st.markdown("---")

# 1. 게임 수 입력 받기 (숫자 입력 위젯으로 변경)
# st.number_input을 사용하여 1부터 10까지의 정수 값을 직접 입력받습니다.
num_games = st.number_input(
    "몇 게임을 생성하시겠습니까? (1~10)",
    min_value=1,
    max_value=10,
    value=1, # 초기값
    step=1,  # 1 단위로 증가/감소
    format="%d" # 정수 형식으로 설정
)

st.write(f"**선택된 게임 수:** {num_games} 게임")
st.markdown("---")

# 2. '생성' 버튼
# 버튼을 누르면 번호 생성 로직이 실행됩니다.
if st.button("✨ 행운의 번호 생성"):
    st.subheader(f"💫 행운의 로또 번호 ({num_games} 게임)")

    # 선택된 게임 수만큼 번호를 생성하여 출력
    for i in range(1, num_games + 1):
        lotto_numbers = generate_lotto_numbers()
        
        # 번호를 쉼표로 구분하여 문자열로 표시
        number_display = " ".join([f"**{num:02d}**" for num in lotto_numbers])
        
        # 결과 출력
        st.markdown(f"**게임 {i}:** {number_display}")
