# streamlit_app.py
# 유리함수(y = a/x)를 시각적·상호작용적으로 학습할 수 있는 Streamlit 앱
# 사용법: 이 파일을 저장한 뒤 터미널에서
#    streamlit run streamlit_app.py
# 실행

import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="유리함수 학습앱", layout="wide")

# --- 사이드바 설정 ---
st.sidebar.header("매개변수 설정")
a = st.sidebar.slider("a 값 (y = a / x)", min_value=-10.0, max_value=10.0, value=2.0, step=0.1)
show_grid = st.sidebar.checkbox("그래프 격자 보이기", value=True)
show_asymptotes = st.sidebar.checkbox("점근선 표시", value=True)
show_point = st.sidebar.checkbox("특정 x에서 값 표시", value=True)

# x 선택 (0을 피함)
col_x1, col_x2 = st.sidebar.columns([1,1])
with col_x1:
    x_choice = st.sidebar.number_input("관찰할 x (0 제외)", value=1.0, format="%f")
with col_x2:
    if abs(x_choice) < 1e-8:
        x_choice = 0.1

# 페이지 레이아웃
st.title("📘 유리함수(y = a/x) 학습 앱")
st.write("이 앱은 유리함수의 정의, 기본 성질(정의역·치역), 그리고 점근선을 인터랙티브하게 이해하도록 돕습니다.")

# 설명 섹션
with st.expander("유리함수의 정의 (펼치기/접기)", expanded=True):
    st.markdown(
        """
        **유리함수(有理函數)**는 분자와 분모가 다항식인 함수이며, 분모가 0이 되는 점에서는 정의되지 않습니다.\
        여기서는 가장 기본 형태인 **y = a / x** (a는 상수)를 집중적으로 다룹니다.
        """
    )

# 기본 성질
st.header("기본 성질 — y = a / x")
col1, col2 = st.columns([1,1])
with col1:
    st.subheader("정의역 (domain)")
    st.write("분모 x가 0이 되면 함수가 정의되지 않으므로 정의역은 모든 실수 x 중에서 x ≠ 0 입니다.")
    st.code("정의역: \{ x ∈ R | x ≠ 0 \}")

with col2:
    st.subheader("치역 (range)")
    if abs(a) < 1e-12:
        st.write("a = 0인 경우: y = 0 (단, x = 0에서는 정의되지 않음). 이때 치역은 {0} 입니다.")
        st.code("치역: \{0\}")
    else:
        st.write("a ≠ 0인 경우: y는 0이 될 수 없고 모든 다른 실수 값을 가질 수 있으므로 치역은 실수 전체에서 0을 제외한 집합입니다.")
        st.code("치역: \{ y ∈ R | y ≠ 0 \}")

# 점근선
st.subheader("점근선 (asymptotes)")
st.write("y = a/x의 경우 다음과 같은 점근선이 있습니다:")
st.markdown("- 수직 점근선: x = 0 (분모가 0이기 때문에)  ")
st.markdown("- 수평 점근선: y = 0 (x → ±∞일 때 a/x → 0)")
if abs(a) < 1e-12:
    st.info("참고: a = 0이면 함수 자체가 거의 y = 0(단, x = 0 제외)이므로 수평 점근선 y=0이 함수와 일치합니다.")

# 그래프 그리기
st.header("그래프로 보기")
# x 범위 구성 (0 근처는 건너뜀)
x_left = np.linspace(-10, -0.2, 500)
x_right = np.linspace(0.2, 10, 500)
x = np.concatenate([x_left, x_right])

y = a / x

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f'y = {a}/x'))

# 점근선 표시
if show_asymptotes:
    # vertical x=0 as a dashed line (drawn by adding a very large line at x=0)
    fig.add_vline(x=0, line=dict(dash='dash'), annotation_text='x=0', annotation_position='top left')
    fig.add_hline(y=0, line=dict(dash='dash'), annotation_text='y=0', annotation_position='bottom right')

# 표시할 점
if show_point:
    if abs(x_choice) < 1e-8:
        st.warning("x는 0일 수 없습니다. 다른 값을 입력해주세요.")
    else:
        y_choice = a / x_choice
        fig.add_trace(go.Scatter(x=[x_choice], y=[y_choice], mode='markers+text', name='관찰점',
                                 text=[f'({x_choice:.3f}, {y_choice:.3f})'], textposition='top center', marker=dict(size=10)))

# 레이아웃
fig.update_layout(title=f'y = {a} / x', xaxis_title='x', yaxis_title='y', showlegend=False)
if show_grid:
    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)

st.plotly_chart(fig, use_container_width=True)

# 함수 성질 요약
st.header("빠른 요약")
col3, col4 = st.columns([1,1])
with col3:
    st.markdown(f"**지정한 a 값:** {a}")
    st.markdown("**정의역:** 모든 실수 x 중 x ≠ 0")
    if abs(a) < 1e-12:
        st.markdown("**치역:** {0} (y는 항상 0, 단 x=0에서는 정의되지 않음)")
    else:
        st.markdown("**치역:** 모든 실수 y 중 y ≠ 0")
with col4:
    st.markdown("**점근선:** 수직 x=0, 수평 y=0")
    st.markdown("**대칭성:** 함수 y = a/x는 원점에 대해 중심대칭 (odd function) 입니다. 즉 f(-x) = -f(x).")

# 직관을 돕는 애니메이션(단계별 a 변화)
with st.expander("a 값에 따른 그래프 변화(애니메이션) — 펼치기", expanded=False):
    st.write("슬라이더를 움직여 a 값이 그래프에 어떤 영향을 주는지 관찰하세요. a의 부호에 따라 그래프가 1·사분면/2·사분면으로 이동합니다.")
    st.write("- a > 0: 1사분면(우측 위)과 3사분면(좌측 아래)에 그래프가 존재합니다.\n- a < 0: 2사분면(좌측 위)과 4사분면(우측 아래)에 그래프가 존재합니다.")

# 연습 문제
st.header("연습 문제")
q1 = "1) a = 3일 때 정의역과 치역을 쓰시오."
q2 = "2) a = -2일 때 함수가 어떤 사분면에 위치하는가?"
q3 = "3) x → ∞ 일 때 y의 극한값은?"
st.markdown(f"1) {q1}\n2) {q2}\n3) {q3}")

with st.expander("정답 보기", expanded=False):
    st.markdown("**정답 1:** 정의역: x ≠ 0, 치역: y ≠ 0")
    st.markdown("**정답 2:** a = -2이면 그래프는 2사분면(좌상)과 4사분면(우하)에 위치합니다.")
    st.markdown("**정답 3:** x → ±∞일 때 y → 0")

# 추가 설명 및 참고
st.header("추가 설명 — 왜 이런 성질이 나오는가?")
st.markdown(
    """
    - 정의역이 x ≠ 0인 이유: 분모가 0이면 식이 성립하지 않습니다.\
    - 치역이 y ≠ 0인 이유 (a ≠ 0일 때): a/x = 0 이 되려면 a = 0 이어야 하므로 a ≠ 0일 때 y는 0이 될 수 없습니다.\
    - 점근선이 y=0인 이유: x를 크게 하면 a/x의 값이 0에 한없이 가까워지지만 절대 0이 되지는 않습니다 (a ≠ 0).
    """
)

st.info("필요하면 이 앱을 기반으로 'y = (ax + b)/(cx + d)' 같은 일반적인 유리함수로 확장해드릴게요 — 원하는 추가 기능을 말해 주세요!")

# 푸터
st.markdown("---")
st.caption("앱 제작: Streamlit — 기본 형태 y = a/x 학습용 (Korean)")
