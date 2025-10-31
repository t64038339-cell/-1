import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 제목
st.title("📘 유리함수의 그래프 변형 학습")

# --- 1️⃣ 개념 탐구 단계 ---
with st.expander("📖 단계 1. 기본 개념 이해하기", expanded=True):
    st.markdown("""
    ### 🧩 **유리함수의 기본형**
    유리함수는 다음과 같은 형태를 가집니다.  

    \\[
    y = \\frac{a}{x - p} + q
    \\]

    여기서 각 문자의 의미는 다음과 같습니다.  
    - **a** : 그래프의 모양을 결정합니다.  
      - a > 0 → 1, 3사분면에 위치  
      - a < 0 → 2, 4사분면에 위치  
      - |a|가 커질수록 그래프가 y축에 가까워집니다.  
    - **p** : 그래프의 **좌우 이동**을 결정합니다.  
      - x = p는 **수직 점근선**이 됩니다.  
    - **q** : 그래프의 **상하 이동**을 결정합니다.  
      - y = q는 **수평 점근선**이 됩니다.

    👉 즉, 유리함수의 그래프는 **점근선을 기준으로 평행이동**하는 형태를 가집니다.
    """)

# --- 2️⃣ 탐구 활동 안내 ---
with st.expander("🔍 단계 2. 그래프 변화를 탐구하기", expanded=True):
    st.markdown("""
    ### 🎯 **탐구 과제**
    1. 아래 슬라이더를 움직여 a, p, q 값을 바꿔보세요.  
    2. 그래프가 어떻게 이동하고, 점근선이 어떻게 바뀌는지 관찰하세요.  
    3. 특히, p와 q 값이 그래프의 위치에 어떤 영향을 주는지 주의 깊게 살펴봅시다.

    아래는 기준함수 \\( y = \\frac{1}{x} \\) 를 함께 표시하여  
    변화를 비교할 수 있도록 구성되어 있습니다.
    """)

# --- 3️⃣ 조작과 시각화 영역 ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🎛️ 조절 패널")
    a = st.slider("a (그래프의 모양)", -5.0, 5.0, 1.0, 0.1)
    p = st.slider("p (좌우 이동)", -5.0, 5.0, 0.0, 0.1)
    q = st.slider("q (상하 이동)", -5.0, 5.0, 0.0, 0.1)

with col2:
    st.subheader("📊 그래프 시각화")

    x = np.linspace(-10, 10, 400)
    y = a / (x - p) + q

    fig = go.Figure()

    # 현재 유리함수 그래프
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='y = a/(x - p) + q', line=dict(color='black')))

    # 기준 그래프 y = 1/x
    y_ref = 1 / x
    fig.add_trace(go.Scatter(x=x, y=y_ref, mode='lines', name='기준함수 y=1/x', line=dict(color='gray', dash='dot')))

    # 점근선 표시
    fig.add_vline(x=p, line=dict(color="red", dash="dash"), name="수직 점근선")
    fig.add_hline(y=q, line=dict(color="blue", dash="dash"), name="수평 점근선")

    fig.update_layout(
        title=f"현재 함수: y = {a:.1f}/(x - {p:.1f}) + {q:.1f}",
        xaxis_title="x",
        yaxis_title="y",
        width=700,
        height=500,
        template="plotly_white",
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

# --- 4️⃣ 탐구 결과 해석 ---
with st.expander("🧠 단계 3. 결과 해석하기", expanded=True):
    st.markdown(f"""
    ### 🔎 **관찰 결과 요약**

    - 현재 함수:  \\( y = \\frac{{{a:.1f}}}{{x - ({p:.1f})}} + ({q:.1f}) \\)
    - 수직 점근선: \\( x = {p:.1f} \\)
    - 수평 점근선: \\( y = {q:.1f} \\)

    #### 📌 분석
    - **p** 값이 증가하면 그래프 전체가 **오른쪽으로 평행이동**합니다.  
    - **q** 값이 증가하면 그래프 전체가 **위쪽으로 평행이동**합니다.  
    - **a**의 부호가 바뀌면 그래프가 **x축에 대해 대칭 이동**합니다.  

    즉, 유리함수의 그래프는 점근선을 기준으로  
    **상하, 좌우 이동**하며 형태를 유지합니다.
    """)

# --- 5️⃣ 정리 ---
with st.expander("🧾 단계 4. 정리하기", expanded=True):
    st.markdown("""
    ### ✅ **학습 정리**
    1. 유리함수의 기본형은 \\( y = \\frac{a}{x - p} + q \\) 이다.  
    2. 수직 점근선은 x = p, 수평 점근선은 y = q 이다.  
    3. a, p, q의 변화는 그래프의 위치와 모양을 평행이동 형태로 바꾼다.  
    4. 그래프를 직접 조작하며 점근선의 위치가 이동하는 이유를 이해하는 것이 핵심이다.
    """)

st.info("""
💬 **탐구 활동 팁:**  
p와 q를 동시에 바꿔가며 그래프가 두 점근선에 따라 어떻게 이동하는지 관찰해 보세요.  
이 과정이 바로 ‘함수의 평행이동’을 시각적으로 이해하는 방법입니다.
""")
