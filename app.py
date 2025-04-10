import streamlit as st
from math import log, sqrt, exp
from scipy.stats import norm

# --- Black-Scholes Call Option Price ---
def black_scholes_call_price(S, K, T, r, sigma):
    d1 = (log(S/K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    call_price = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
    delta = norm.cdf(d1)
    return round(call_price, 2), round(delta, 3)

# --- Streamlit App ---
st.set_page_config(page_title="Option Opening Price Estimator", layout="centered")
st.title("📈 Option Opening Price Estimator")
st.caption("Predict tomorrow's option price based on GIFT Nifty gap-up/down")

st.header("🔢 Inputs")

current_option_price = st.number_input("Current Option Price (LTP)", value=10.0, step=0.5)
spot_price = st.number_input("Current Nifty Spot", value=22500)
strike_price = st.number_input("Strike Price", value=22700)
days_to_expiry = st.slider("Days to Expiry", 1, 30, 7)
gift_change_percent = st.slider("GIFT Nifty % Change", -5.0, 5.0, 3.0, 0.1)

T = days_to_expiry / 365
r = 0.06  # Risk-free rate
sigma = 0.25  # You can make this dynamic later

# --- Calculation ---
gap = (gift_change_percent / 100) * spot_price
expected_open_spot = spot_price + gap

opening_price, opening_delta = black_scholes_call_price(expected_open_spot, strike_price, T, r, sigma)

st.header("📊 Results")
st.success(f"Expected Opening Option Price: ₹{opening_price}")
st.write(f"🔄 Change from Current: ₹{round(opening_price - current_option_price, 2)}")
st.write(f"📐 Delta at Open: {opening_delta}")
st.info(f"Expected Opening Nifty Spot: {round(expected_open_spot)}")

st.caption("💡 Based on Black-Scholes and projected GIFT Nifty movement. Actual price may vary with IV changes.")

