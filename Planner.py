import math
import numpy as np
import streamlit as st

st.set_page_config(page_title="Asset Financing Split Calculator", page_icon="💸", layout="wide")

# ----------------------------
# Helper functions
# ----------------------------

def pmt(rate: float, nper: int, pv: float) -> float:
    """Monthly payment for an amortizing loan.
    rate: periodic interest rate (per period, e.g., monthly APR/12)
    nper: total number of periods
    pv: present value (loan principal), positive number
    Returns positive payment amount per period.
    """
    if nper <= 0:
        return 0.0
    if rate == 0:
        return pv / nper
    return rate * pv / (1.0 - (1.0 + rate) ** (-nper))


def loan_amount_from_payment(rate: float, nper: int, payment: float) -> float:
    """Inverse of PMT: principal affordable for a given payment."""
    if nper <= 0:
        return 0.0
    if rate == 0:
        return payment * nper
    return payment * (1.0 - (1.0 + rate) ** (-nper)) / rate


def remaining_balance(principal: float, rate: float, nper: int, periods_paid: int) -> float:
    """Outstanding balance after `periods_paid` payments on a fully amortizing loan."""
    if nper <= 0:
        return 0.0
    if rate == 0:
        # Straight-line principal reduction
        paid = principal * (periods_paid / nper)
        return max(0.0, principal - paid)
    payment = pmt(rate, nper, principal)
    # Standard amortization remaining balance formula
    return principal * (1 + rate) ** periods_paid - payment * (((1 + rate) ** periods_paid - 1) / rate)


def npv(rate: float, cashflows: list[float]) -> float:
    """NPV for a series of cashflows CF_0..CF_n at a periodic discount rate."""
    return sum(cf / ((1 + rate) ** t) for t, cf in enumerate(cashflows))


def irr(cashflows: list[float], guess: float = 0.1, max_iter: int = 100, tol: float = 1e-7) -> float | None:
    """IRR using Newton's method on periodic cashflows. Returns None if not found."""
    r = guess
    for _ in range(max_iter):
        # f(r) = NPV(r)
        f = 0.0
        df = 0.0
        for t, cf in enumerate(cashflows):
            denom = (1 + r) ** t
            f += cf / denom
            if denom != 0:
                df -= t * cf / denom / (1 + r)
        if abs(df) < 1e-12:
            break
        new_r = r - f / df
        if abs(new_r - r) < tol:
            return new_r
        r = new_r
    return None

# ----------------------------
# UI
# ----------------------------

st.title("💸 Asset Financing Split Calculator")
st.write(
    "Plan how to split an acquisition between **down payment** and **loan**,\n"
    "based on expected monthly returns and a target risk profile."
)

with st.sidebar:
    st.header("Inputs")
    mode = st.radio(
        "Analysis mode",
        ["Given Target Price", "Compute Max Affordable Price"],
        index=0,
        help="Choose whether you already have a price or want to know the most you should pay.",
    )

    # Cashflow & horizon
    monthly_return = st.number_input(
        "Expected net monthly cashflow (₹)", min_value=0.0, value=50000.0, step=1000.0,
        help="Your best estimate of net cash generated per month by the asset after expenses."
    )
    horizon_months = st.number_input(
        "Planning horizon (months)", min_value=1, value=60, step=1,
        help="How long you plan to hold the asset for this analysis."
    )
    resale_value = st.number_input(
        "Expected resale/scrap value at end (₹)", min_value=0.0, value=200000.0, step=10000.0
    )

    # Debt inputs
    loan_apr = st.number_input(
        "Loan APR (annual %)", min_value=0.0, value=12.0, step=0.25,
        help="Nominal annual percentage rate."
    )
    loan_term = st.number_input(
        "Loan term (months)", min_value=1, value=60, step=1,
        help="Total number of monthly payments."
    )

    # Risk / policy controls
    dscr = st.number_input(
        "Minimum DSCR (cashflow ÷ debt service)", min_value=0.5, value=1.25, step=0.05,
        help="Debt Service Coverage Ratio. 1.25 is a common covenant."
    )
    min_down_pct = st.number_input(
        "Minimum down payment (%)", min_value=0.0, max_value=100.0, value=20.0, step=1.0,
        help="Some lenders require 10–30% down."
    )

    # Equity hurdle rate
    equity_required_apy = st.number_input(
        "Required equity return (annual %)", min_value=0.0, value=15.0, step=0.5,
        help="Your hurdle rate for equity. Used to value the deal and compute IRR/NPV."
    )

    # Price when in price-known mode
    target_price = None
    if mode == "Given Target Price":
        target_price = st.number_input(
            "Target purchase price (₹)", min_value=0.0, value=1000000.0, step=10000.0
        )

# Derived rates
r_m = loan_apr / 100.0 / 12.0  # monthly loan rate
hurdle_m = equity_required_apy / 100.0 / 12.0  # monthly equity discount/IRR target

# Coverage-based max payment and loan
pmt_max = (monthly_return / max(dscr, 1e-9))  # ₹ per month allowed for debt service
loan_by_coverage = loan_amount_from_payment(r_m, int(loan_term), pmt_max)

# NPV-based fair value (maximum price you should be willing to pay for the asset itself)
# PV of monthly returns + PV of resale value
pv_returns = 0.0
if hurdle_m > -1:
    if hurdle_m == 0:
        pv_returns = monthly_return * horizon_months
        pv_resale = resale_value
    else:
        pv_returns = monthly_return * (1 - (1 + hurdle_m) ** (-horizon_months)) / hurdle_m
        pv_resale = resale_value / ((1 + hurdle_m) ** horizon_months)
else:
    pv_returns = float("nan"); pv_resale = float("nan")

fair_value = pv_returns + pv_resale

# Minimum down payment by policy
min_down_fraction = min_down_pct / 100.0

# Function to summarize a given price

def analyze_price(price: float):
    price = max(0.0, float(price))
    min_down_amt = price * min_down_fraction

    # Max loan allowed by coverage (DSCR)
    max_loan_coverage = loan_by_coverage

    # Max loan allowed by down payment policy (can't borrow more than price - min_down)
    max_loan_ltv = max(0.0, price - min_down_amt)

    # Actual allowable loan is the smaller of the two
    recommended_loan = min(max_loan_coverage, max_loan_ltv)

    # Recommended down payment is the rest
    recommended_down = price - recommended_loan

    # Debt service & cashflow to equity
    pay = pmt(r_m, int(loan_term), recommended_loan) if recommended_loan > 0 else 0.0

    # Build equity cashflows over the horizon
    months = int(horizon_months)
    cashflows = [-recommended_down]

    # If horizon differs from loan term, account for remaining balance or extra time w/o debt
    for t in range(1, months + 1):
        # Cash to equity each month = operating CF minus debt service if within loan term
        debt_service = pay if t <= loan_term and recommended_loan > 0 else 0.0
        cashflows.append(monthly_return - debt_service)

    # Add terminal cash: resale proceeds minus remaining loan balance (if any)
    rem_bal = 0.0
    if recommended_loan > 0 and horizon_months < loan_term:
        # Balloon remains if selling before loan fully amortizes
        rem_bal = remaining_balance(recommended_loan, r_m, int(loan_term), int(horizon_months))
    # If horizon exceeds loan term, rem_bal stays 0 because loan is paid off before sale

    terminal = resale_value - rem_bal
    cashflows[-1] += terminal

    # Metrics
    equity_npv = npv(hurdle_m, cashflows)
    equity_irr = irr(cashflows)

    return {
        "price": price,
        "min_down_amt": min_down_amt,
        "max_loan_coverage": max_loan_coverage,
        "max_loan_ltv": max_loan_ltv,
        "recommended_loan": max(0.0, recommended_loan),
        "recommended_down": max(0.0, recommended_down),
        "monthly_payment": pay,
        "coverage_used": (pmt_max / pay) if pay > 0 else float("inf"),
        "equity_cashflows": cashflows,
        "equity_npv": equity_npv,
        "equity_irr": equity_irr,
        "remaining_balance_at_sale": rem_bal,
    }

# ----------------------------
# Main logic & output
# ----------------------------

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Fair Value (NPV-based)")
    st.metric("PV of monthly returns", f"₹{pv_returns:,.0f}")
    st.metric("PV of resale value", f"₹{pv_resale:,.0f}")
    st.metric("Fair value (max price at hurdle)", f"₹{fair_value:,.0f}")

with col2:
    st.subheader("Coverage-Limited Debt Capacity")
    st.metric("Max affordable monthly payment", f"₹{pmt_max:,.0f}")
    st.metric("Max loan by DSCR", f"₹{loan_by_coverage:,.0f}")

st.markdown("---")

if mode == "Given Target Price":
    result = analyze_price(target_price)
    st.subheader("Recommendation for Target Price")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Target price", f"₹{result['price']:,.0f}")
    c2.metric("Recommended loan", f"₹{result['recommended_loan']:,.0f}")
    c3.metric("Down payment", f"₹{result['recommended_down']:,.0f}")
    c4.metric("Monthly payment", f"₹{result['monthly_payment']:,.0f}")

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("Min down (policy)", f"₹{result['min_down_amt']:,.0f}")
    c6.metric("Loan cap (coverage)", f"₹{result['max_loan_coverage']:,.0f}")
    c7.metric("Loan cap (LTV)", f"₹{result['max_loan_ltv']:,.0f}")
    irr_txt = "N/A" if result["equity_irr"] is None else f"{result['equity_irr']*12*100:,.2f}% p.a."
    c8.metric("Equity IRR (annualized)", irr_txt)

    st.caption(
        "Equity IRR computed from cashflows: initial down payment, monthly net cash after debt service, and terminal sale net of any remaining loan balance."
    )

else:
    # Compute the maximum price that satisfies both (a) fair value and (b) coverage/LTV constraints
    # Approach: iterate over price grid to find the highest price where recommended_loan respects coverage and min down.
    # Also do not exceed fair value (optional: user might pay above FV but we cap at FV by default).
    grid = np.linspace(0, max(fair_value * 1.25, 1), 1000)
    best = None
    for price in grid:
        res = analyze_price(price)
        # We enforce price <= fair_value to avoid overpaying vs hurdle
        if price <= fair_value + 1e-6:
            best = res
    if best is None:
        best = analyze_price(0)

    st.subheader("Max Affordable Price (subject to hurdle & DSCR)")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Max price", f"₹{best['price']:,.0f}")
    c2.metric("Recommended loan", f"₹{best['recommended_loan']:,.0f}")
    c3.metric("Down payment", f"₹{best['recommended_down']:,.0f}")
    c4.metric("Monthly payment", f"₹{best['monthly_payment']:,.0f}")

    irr_txt = "N/A" if best["equity_irr"] is None else f"{best['equity_irr']*12*100:,.2f}% p.a."
    st.metric("Equity IRR at max price (annualized)", irr_txt)

st.markdown("---")

# Cashflow table preview
st.subheader("Equity Cashflows (₹)")
if mode == "Given Target Price":
    cf = result["equity_cashflows"]
else:
    cf = best["equity_cashflows"]

rows = [(t, cf[t]) for t in range(len(cf))]
st.dataframe({"Month": [r[0] for r in rows], "Cashflow": [r[1] for r in rows]})

st.caption(
    "Month 0 is the initial down payment (negative). The last month's cashflow includes resale proceeds net of any remaining loan balance."
)

st.info(
    """
**How this works**
- **Fair value** is the present value of expected monthly cashflows plus the discounted resale value using your **required equity return**.
- **Coverage-limited loan** uses DSCR: max debt service = monthly net cash ÷ DSCR. We back into the largest loan such that its monthly payment ≤ that amount.
- The **recommended split** picks the smaller of (i) loan allowed by coverage and (ii) loan allowed by your minimum down payment policy.
- We compute **Equity IRR/NPV** using the down payment as initial outflow, monthly equity cashflows, and terminal sale net of remaining loan.
"""
)
