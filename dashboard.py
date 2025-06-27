import streamlit as st
from bot_logic import TradingBot

st.title("Day Trading Bot Dashboard")

api_key = st.text_input("Alpaca API Key", type="password")
api_secret = st.text_input("Alpaca API Secret", type="password")
symbol = st.text_input("Ticker Symbol (e.g. AAPL)", value="AAPL")
profit_target = st.number_input("Profit Target %", min_value=0.1, max_value=10.0, value=2.0, step=0.1)
stop_loss = st.number_input("Stop Loss %", min_value=0.1, max_value=10.0, value=1.0, step=0.1)

if st.button("Start Bot"):
    if not api_key or not api_secret or not symbol:
        st.error("Please fill all inputs!")
    else:
        bot = TradingBot(api_key, api_secret, symbol, profit_target, stop_loss)
        st.success("Bot started for " + symbol)
        bot.run()

if st.button("Stop Bot"):
    st.warning("Stop functionality not implemented in this demo")
