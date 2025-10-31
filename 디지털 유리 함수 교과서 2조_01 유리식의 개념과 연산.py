# streamlit_rational_steps.py
import streamlit as st
import sympy as sp

st.set_page_config(page_title="유리식 연산 단계별 학습", layout="centered")
st.title("📘 유리식 연산 — 단계별 풀이 앱")
st.write("---")

st.header("유리식의 개념 (요약)")
st.markdown("""
유리식은 두 다항식의 나눗셈으로 나타나는 식입니다.  
예: \\(\\frac{P(x)}{Q(x)}\\), 단 \\(Q(x)\\neq 0\\).
""")

# 심볼
x = sp.Symbol('x')

# 미리 정한 예시들 (교육용)
examples = {
    "덧셈": ((x + 1)/(x - 2), (2*x)/(x + 3)),
    "뺄셈": ((2*x)/(x + 1), (x - 3)/(x - 2)),
    "곱셈": ((x**2 - 1)/(x + 2), (x + 2)/(x + 1)),
    "나눗셈": ((x + 3)/(x - 1), (x + 1)/(x + 2)),
}

st.subheader("예시 유리식")
for name, (a, b) in examples.items():
    st.markdown(f"**{name} 예시:**")
    st.latex(sp.latex(a) + " , " + sp.latex(b))

st.write("---")
operation = st.selectbox("보기를 선택하세요 (예시 기반)", ["덧셈", "뺄셈", "곱셈", "나눗셈"])

# helper: latex display for sympy expressions with explanation line
def show_step(title, expr=None):
    st.markdown(f"**{title}**")
    if expr is not None:
        st.latex(sp.latex(expr))

def denom_zeros(expr):
    # find denominator and solve denom = 0
    num, den = sp.fraction(sp.together(expr))
    # den may be multiplied factors; solve den == 0
    sols = sp.solve(sp.Eq(sp.simplify(den), 0), x)
    return sols

# compute steps for addition/subtraction using cross-multiplication approach
def addition_steps(e1, e2, sign="+"):
    a_num, a_den = sp.fraction(sp.together(e1))
    b_num, b_den = sp.fraction(sp.together(e2))

    show_step("원래 식", sp.Rational(1,1)* (e1) if sign=="+" else (e1) )
    st.latex(("+" if sign=="+" else "-"))
    st.latex(sp.latex(e2))
    st.write("")

    # 공통분모 (간단히 b_den * a_den)
    common = sp.simplify(a_den * b_den)
    show_step("1) 공통분모 구하기 (교과서적 방법: 분모끼리 곱함)", common)
    # 분자 바꾸기 (교차 곱)
    if sign == "+":
        new_num = sp.simplify(a_num * b_den + b_num * a_den)
        show_step("2) 분자 변형 (교차 곱):", new_num)
    else:
        new_num = sp.simplify(a_num * b_den - b_num * a_den)
        show_step("2) 분자 변형 (교차 곱):", new_num)

    # 전개 (필요시)
    show_step("3) 분자 전개/정리 (필요 시)", sp.expand(new_num))

    # 인수분해 및 약분
    fact_num = sp.factor(new_num)
    fact_den = sp.factor(common)
    show_step("4) 분자 인수분해", fact_num)
    show_step("   분모 인수분해", fact_den)

    canceled = sp.cancel(sp.Rational(1,1) * (new_num / common))
    show_step("5) 약분하여 정리", canceled)

    # 정의역 제외값 안내
    zeros = sorted(set(denom_zeros(e1) + denom_zeros(e2)))
    if zeros:
        st.warning("정의역에서 제외되는 값(분모 0이 되는 값): " + ", ".join([sp.latex(z) for z in zeros]))
    else:
        st.info("정의역에서 제외되는 값 없음")

def multiplication_steps(e1, e2):
    a_num, a_den = sp.fraction(sp.together(e1))
    b_num, b_den = sp.fraction(sp.together(e2))

    show_step("원래 식", e1 * e2)

    show_step("1) 분자끼리, 분모끼리 곱하기", sp.simplify(a_num * b_num) )
    show_step("   분모: ", sp.simplify(a_den * b_den))

    # 인수분해해서 약분
    fact_num = sp.factor(a_num * b_num)
    fact_den = sp.factor(a_den * b_den)
    show_step("2) 분자 인수분해", fact_num)
    show_step("   분모 인수분해", fact_den)

    canceled = sp.cancel((a_num * b_num) / (a_den * b_den))
    show_step("3) 가능한 약분을 적용한 결과", canceled)

    zeros = sorted(set(denom_zeros(e1) + denom_zeros(e2)))
    if zeros:
        st.warning("정의역에서 제외되는 값(분모 0이 되는 값): " + ", ".join([sp.latex(z) for z in zeros]))
    else:
        st.info("정의역에서 제외되는 값 없음")

def division_steps(e1, e2):
    show_step("원래 식", e1 / e2)
    # 뒤집기
    show_step("1) 나누는 식을 뒤집음(역수)", sp.simplify(sp.inverse(e2) if hasattr(sp, "inverse") else 1/e2))
    show_step("   따라서 곱셈으로 바꾼 식:", sp.simplify(e1 * sp.simplify(1/e2)))

    # reuse multiplication steps on e1 and 1/e2
    multiplication_steps(e1, sp.simplify(1/e2))

    zeros = sorted(set(denom_zeros(e1) + denom_zeros(e2)))
    if zeros:
        st.warning("정의역에서 제외되는 값(분모 0이 되는 값): " + ", ".join([sp.latex(z) for z in zeros]))
    else:
        st.info("정의역에서 제외되는 값 없음")

# 실행
e1, e2 = examples[operation]

st.write("---")
st.header(f"선택: {operation} — 단계별 풀이")

if operation == "덧셈":
    addition_steps(e1, e2, sign="+")
elif operation == "뺄셈":
    addition_steps(e1, e2, sign="-")
elif operation == "곱셈":
    multiplication_steps(e1, e2)
elif operation == "나눗셈":
    division_steps(e1, e2)

st.write("---")
st.success("참고: 각 단계의 표현은 SymPy로 계산되어 LaTeX로 표시됩니다. 직접 식을 입력해 연습 문제 기능을 추가하길 원하면 알려주세요!")
