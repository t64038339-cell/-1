# streamlit_rational_explanation.py
import streamlit as st
import sympy as sp

st.set_page_config(page_title="유리식 연산 서술형 학습", layout="centered")
st.title("📘 유리식의 연산 — 서술형 단계별 풀이 앱")
st.write("---")

st.header("1️⃣ 유리식의 개념")
st.markdown("""
- **유리식**은 두 다항식의 나눗셈으로 표현되는 식입니다.  
  즉,  
  $$ \\frac{P(x)}{Q(x)} \\quad (Q(x) \\neq 0) $$  
  의 형태를 가지며, 분모에 문자가 포함된 식도 유리식입니다.
""")

st.subheader("예시 유리식")
examples = [
    "\\( \\frac{x}{x+1} \\),  \\( \\frac{3}{x-2} \\),  \\( \\frac{2x^2 + 1}{x^2 - 4} \\)"
]
for ex in examples:
    st.markdown(ex)

st.write("---")

# 공통 변수 설정
x = sp.Symbol('x')

# 예시 유리식들
exprs = {
    "덧셈": ((x + 1)/(x - 2), (2*x)/(x + 3)),
    "뺄셈": ((2*x)/(x + 1), (x - 3)/(x - 2)),
    "곱셈": ((x**2 - 1)/(x + 2), (x + 2)/(x + 1)),
    "나눗셈": ((x + 3)/(x - 1), (x + 1)/(x + 2)),
}

operation = st.selectbox("연산을 선택하세요", ["덧셈", "뺄셈", "곱셈", "나눗셈"])
expr1, expr2 = exprs[operation]

st.write("---")
st.header(f"2️⃣ {operation} 단계별 서술형 풀이")

def print_domain_warning(e1, e2):
    den1 = sp.denom(sp.together(e1))
    den2 = sp.denom(sp.together(e2))
    zeros = sorted(set(sp.solve(sp.Eq(den1,0), x) + sp.solve(sp.Eq(den2,0), x)))
    if zeros:
        st.warning("⚠️ 정의역에서 제외되는 값: " + ", ".join([sp.latex(z) for z in zeros]))

if operation == "덧셈":
    st.subheader("➕ 유리식의 덧셈")
    st.markdown("""
    유리식의 덧셈은 분모가 다를 경우 **공통분모를 만들어 분자를 변형한 뒤 더하는 것**이 핵심입니다.
    """)
    st.latex(sp.latex(expr1) + " + " + sp.latex(expr2))

    st.markdown("① **공통분모 구하기**  
    분모가 각각 $(x-2)$, $(x+3)$이므로 공통분모는 두 분모를 곱한 $(x-2)(x+3)$입니다.")
    st.latex("(x-2)(x+3)")

    st.markdown("② **분자를 공통분모에 맞게 바꾸기**  
    첫 번째 분수는 분모 $(x-2)$에 $(x+3)$을 곱하고, 두 번째 분수는 $(x+3)$에 $(x-2)$를 곱합니다.")
    st.latex("\\frac{(x+1)(x+3) + 2x(x-2)}{(x-2)(x+3)}")

    st.markdown("③ **분자를 전개하여 정리합니다.**")
    numerator = sp.expand((x+1)*(x+3) + 2*x*(x-2))
    st.latex(sp.latex(numerator) + " = " + sp.latex(sp.expand(numerator)))
    st.latex(f"\\frac{{{sp.latex(numerator)}}}{{(x-2)(x+3)}}")

    st.markdown("④ **필요한 경우 인수분해하거나 약분합니다.**")
    simplified = sp.simplify(expr1 + expr2)
    st.latex("\\Rightarrow " + sp.latex(simplified))

    print_domain_warning(expr1, expr2)

elif operation == "뺄셈":
    st.subheader("➖ 유리식의 뺄셈")
    st.markdown("""
    유리식의 뺄셈도 덧셈과 같은 원리로 **공통분모를 구한 뒤 분자끼리 뺍니다.**
    """)
    st.latex(sp.latex(expr1) + " - " + sp.latex(expr2))

    st.markdown("① **공통분모 구하기**  
    분모가 각각 $(x+1)$, $(x-2)$이므로 공통분모는 $(x+1)(x-2)$입니다.")
    st.latex("(x+1)(x-2)")

    st.markdown("② **분자를 공통분모에 맞게 바꾸기**")
    st.latex("\\frac{2x(x-2) - (x-3)(x+1)}{(x+1)(x-2)}")

    st.markdown("③ **분자를 전개하여 정리합니다.**")
    numerator = sp.expand(2*x*(x-2) - (x-3)*(x+1))
    st.latex(sp.latex(numerator) + " = " + sp.latex(sp.expand(numerator)))
    st.latex(f"\\frac{{{sp.latex(numerator)}}}{{(x+1)(x-2)}}")

    st.markdown("④ **인수분해 및 약분 후 정리합니다.**")
    simplified = sp.simplify(expr1 - expr2)
    st.latex("\\Rightarrow " + sp.latex(simplified))

    print_domain_warning(expr1, expr2)

elif operation == "곱셈":
    st.subheader("✖️ 유리식의 곱셈")
    st.markdown("""
    유리식의 곱셈은 **분자끼리, 분모끼리 곱한 후 공통인 인수를 약분**합니다.
    """)
    st.latex(sp.latex(expr1) + " \\times " + sp.latex(expr2))

    st.markdown("① **분자끼리, 분모끼리 곱합니다.**")
    st.latex("\\frac{(x^2 - 1)(x + 2)}{(x + 2)(x + 1)}")

    st.markdown("② **분자와 분모를 인수분해합니다.**")
    st.latex("\\frac{(x - 1)(x + 1)(x + 2)}{(x + 2)(x + 1)}")

    st.markdown("③ **공통 인수 $(x+1)$, $(x+2)$를 약분합니다.**")
    st.latex("\\frac{x - 1}{1} = x - 1")

    st.markdown("④ **따라서 최종 결과는 다음과 같습니다.**")
    st.latex("x - 1")

    print_domain_warning(expr1, expr2)

elif operation == "나눗셈":
    st.subheader("➗ 유리식의 나눗셈")
    st.markdown("""
    나눗셈은 **나누는 분수를 뒤집어서 곱셈으로 바꾼 뒤 계산**합니다.
    """)
    st.latex(sp.latex(expr1) + " \\div " + sp.latex(expr2))

    st.markdown("① **나누는 식을 뒤집어 곱셈으로 바꿉니다.**")
    st.latex("\\frac{x+3}{x-1} \\times \\frac{x+2}{x+1}")

    st.markdown("② **분자끼리, 분모끼리 곱합니다.**")
    st.latex("\\frac{(x+3)(x+2)}{(x-1)(x+1)}")

    st.markdown("③ **전개 후 정리하면 다음과 같습니다.**")
    simplified = sp.simplify(expr1 / expr2)
    st.latex("\\Rightarrow " + sp.latex(simplified))

    print_domain_warning(expr1, expr2)

st.write("---")
st.info("💡 모든 연산에서 분모가 0이 되는 값은 정의역에서 제외되어야 합니다.")
