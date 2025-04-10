import streamlit as st
from math import log, sqrt, exp
from scipy.stats import norm

# --- Black-Scholes Call Option Price ---
def black_scholes_call_price(S, K, T, r, sigma):
    d1 = (log(S/K) + (r + sigma**2 / 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    call_price = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
    delta = norm.cdf(d1)
    return round(call_price, 2), round(delta, 3)

# --- Auto IV spike estimator based on % change or events ---
def estimate_iv_spike(gift_nifty_change, event_type):
    spike = 0
    if abs(gift_nifty_change) >= 3:
        spike += 0.25
    elif abs(gift_nifty_change) >= 2:
        spike += 0.18
    elif abs(gift_nifty_change) >= 1:
        spike += 0.12
    else:
        spike += 0.07

    event_boost = {
        "None": 0.00,
        "RBI Policy": 0.05,
        "US CPI Data": 0.08,
        "Fed Meeting": 0.10,
        "Budget Day": 0.20,
        "Quarterly Results": 0.04
    }
    spike += event_boost.get(event_type, 0)
    return round(spike, 2)

# --- UI ---
st.set_page_config(page_title="Option Estimator", layout="centered")
st.title("📈 Option Price & Delta Estimator")
st.markdown("Smart tool to auto-estimate IV and option prices from GIFT Nifty change and market events.")

st.header("🔢 Option Parameters")
spot_price = st.number_input("Nifty Spot Price", value=22500)
strike_price = st.number_input("Strike Price", value=22700)
days_to_expiry = st.slider("Days to Expiry", 1, 30, 7)
T = days_to_expiry / 365
r = 0.06  # Risk-free rate

st.header("📊 GIFT Nifty & Events")
gift_nifty_change = st.slider("GIFT Nifty % Change", -5.0, 5.0, 1.5, 0.1)
event_type = st.selectbox("Market Event", [
    "None", "RBI Policy", "US CPI Data", "Fed Meeting", "Budget Day", "Quarterly Results"
])

manual_iv = st.toggle("🔧 Manually Enter IV?", value=False)

if manual_iv:
    implied_volatility = st.slider("Enter IV (0.01 to 1.0)", 0.01, 1.0, 0.25, 0.01)
else:
    estimated_iv = estimate_iv_spike(gift_nifty_change, event_type)
    implied_volatility = estimated_iv
    st.info(f"Estimated IV: **{round(implied_volatility * 100, 2)}%**")

price, delta = black_scholes_call_price(spot_price, strike_price, T, r, implied_volatility)

st.success(f"💰 Estimated Option Price: ₹ {price}")
st.warning(f"📐 Delta: {delta}")

st.caption("⚡ Built by your trading assistant. Deploy on Streamlit, mobile-friendly by design.")
