import streamlit as st
import ast
import operator

st.markdown(
    """
    <h1 style='text-align: right; color: orange;'>
    Calculator 💸
    </h1>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("Calculators 🏦")

calculator = st.sidebar.selectbox(
    "Choose Calculator",
    ["Financial", "Simple", "Scientific"]
)

# Operators Mapping
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow
}

# Evaluation Function
def evaluate(expression):

    def _eval(node):

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise TypeError("Only numeric values allowed")

        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)

            op_type = type(node.op)
            if op_type in OPERATORS:
                return OPERATORS[op_type](left, right)
            else:
                raise TypeError("Operator not supported")

        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)

            if isinstance(node.op, ast.USub):
                return -operand

            elif isinstance(node.op, ast.UAdd):
                return operand

            else:
                raise TypeError("Unary operator not supported")

        else:
            raise TypeError("Unsupported expression")

    tree = ast.parse(expression, mode='eval')
    return _eval(tree.body)


def simple_interest(p, r, t):
    return (p * r * t) / 100

def present_value(fv, r , n):
    r = r/100
    return fv/(1+r)**n

def compound_value(pv, r, n):
    r = r/100
    return pv*(1+r)**n

def compound_interest(pv, r, n):
    fv = compound_value(pv, r, n)
    return fv - pv

if calculator == "Financial":

    st.title("Financial Calculator")

    select = st.selectbox(
        "What do you want to know?",
        ["Simple Interest", "Compound Interest", "Present Value", "Future Value"]
    )

    if select == "Simple Interest":

        p = st.number_input("Principal", key="si_p")
        r = st.number_input("Rate (%)", key="si_r")
        t = st.number_input("Time (years)", key="si_t")

        if st.button("Calculate", key="si_button"):
            result = simple_interest(p, r, t)
            st.success(f"Simple Interest = {result}")

    elif select == "Present Value":

        fv = st.number_input("Future Value", key="pv_fv")
        r = st.number_input("Rate (%)", key="pv_r")
        n = st.number_input("Time (years)", key="pv_n")

        if st.button("Calculate", key="pv_button"):
            result = present_value(fv, r, n)
            st.success(f"Present Value = {result}")

    elif select == "Compound Interest":

        pv = st.number_input("Principal", key="ci_pv")
        r = st.number_input("Rate (%)", key="ci_r")
        n = st.number_input("Time (years)", key="ci_n")

        if st.button("Calculate", key="ci_button"):
            result = compound_interest(pv, r, n)
            st.success(f"Compound Interest = {result}")

    elif select == "Future Value":

        pv = st.number_input("Present Value", key="fv_pv")
        r = st.number_input("Rate (%)", key="fv_r")
        n = st.number_input("Time (years)", key="fv_n")

        if st.button("Calculate", key="fv_button"):
            result = compound_value(pv, r, n)
            st.success(f"Future Value = {result}")
            
if st.button("Calculate", key="simple_calc"):

    if expression.strip() == "":
        st.warning("Please enter a mathematical expression")

    else:
        try:
            result = evaluate(expression)
            st.success(f"Result: {result}")

        except ZeroDivisionError:
            st.warning("Result is undefined (division by zero)")

        except TypeError:
            st.error("Invalid mathematical expression")

        except Exception:
            st.error("Something went wrong while evaluating the expression")
