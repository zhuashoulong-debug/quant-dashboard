import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="A股量化看板", layout="wide")
st.title("A股量化交易看板")

page = st.sidebar.radio("功能选择", ["策略回测", "选股筛选"])

def calc_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()
    rs = gain / loss
    return 100 - 100 / (1 + rs)

def calc_macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    hist = macd - signal_line
    return macd, signal_line, hist

if page == "策略回测":
    st.subheader("策略回测（均线 + RSI + MACD + 风控）")
    stock_code = st.sidebar.text_input("股票代码", value="600036.SS")
    start_date = st.sidebar.text_input("开始日期", value="2024-01-01")
    end_date = st.sidebar.text_input("结束日期", value="2025-01-01")
    initial_cash = st.sidebar.number_input("初始资金", value=100000, step=10000)
    ma_short = st.sidebar.slider("短期均线", 5, 30, 10)
    ma_long = st.sidebar.slider("长期均线", 10, 60, 30)

    st.sidebar.markdown("---")
    st.sidebar.subheader("RSI 参数")
    rsi_period = st.sidebar.slider("RSI 周期", 7, 21, 14)
    rsi_buy = st.sidebar.slider("RSI 买入阈值（低于此值才买）", 20, 60, 45)
    rsi_sell = st.sidebar.slider("RSI 卖出阈值（高于此值才卖）", 50, 85, 70)

    st.sidebar.markdown("---")
    st.sidebar.subheader("风控参数")
    stop_loss = st.sidebar.slider("止损比例(%)", 1, 20, 5)
    take_profit = st.sidebar.slider("止盈比例(%)", 5, 50, 15)
    max_position = st.sidebar.slider("单次最大仓位(%)", 10, 100, 80)

    if st.sidebar.button("开始回测"):
        with st.spinner("回测中..."):
            df = yf.download(stock_code, start=start_date, end=end_date)
            df = df[["Open","High","Low","Close","Volume"]].copy()
            df.columns = ["开盘","最高","最低","收盘","成交量"]

            df["MA_S"] = df["收盘"].rolling(ma_short).mean()
            df["MA_L"] = df["收盘"].rolling(ma_long).mean()
            df["RSI"] = calc_rsi(df["收盘"], rsi_period)
            df["MACD"], df["Signal"], df["Hist"] = calc_macd(df["收盘"])

            cash = initial_cash
            shares = 0
            buy_price = 0
            portfolio = []
            trades = []

            for i in range(1, len(df)):
                price = float(df["收盘"].iloc[i])
                s = float(df["MA_S"].iloc[i])
                l = float(df["MA_L"].iloc[i])
                sp = float(df["MA_S"].iloc[i-1])
                lp = float(df["MA_L"].iloc[i-1])
                rsi = float(df["RSI"].iloc[i])
                macd = float(df["MACD"].iloc[i])
                sig = float(df["Signal"].iloc[i])
                macd_prev = float(df["MACD"].iloc[i-1])
                sig_prev = float(df["Signal"].iloc[i-1])

                if shares > 0:
                    change = (price - buy_price) / buy_price * 100
                    if change <= -stop_loss:
                        cash += shares * price
                        trades.append({"日期": df.index[i], "操作": "止损", "价格": round(price,2), "数量": shares, "盈亏%": round(change,2)})
                        shares = 0
                        buy_price = 0
                    elif change >= take_profit:
                        cash += shares * price
                        trades.append({"日期": df.index[i], "操作": "止盈", "价格": round(price,2), "数量": shares, "盈亏%": round(change,2)})
                        shares = 0
                        buy_price = 0
                    elif sp > lp and s < l and rsi > rsi_sell:
                        cash += shares * price
                        trades.append({"日期": df.index[i], "操作": "均线+RSI卖", "价格": round(price,2), "数量": shares, "盈亏%": round(change,2)})
                        shares = 0
                        buy_price = 0

                # 买入条件：金叉 + RSI未超买 + MACD金叉
                ma_cross = sp < lp and s > l
                macd_cross = macd_prev < sig_prev and macd > sig
                rsi_ok = rsi < rsi_buy

                if shares == 0 and price > 0 and ma_cross and rsi_ok:
                    max_cash = cash * max_position / 100
                    shares = int(max_cash / price / 100) * 100
                    if shares > 0:
                        cash -= shares * price
                        buy_price = price
                        trades.append({"日期": df.index[i], "操作": "买入", "价格": round(price,2), "数量": shares, "盈亏%": 0})

                portfolio.append(cash + shares * price)

            final_value = cash + shares * float(df["收盘"].iloc[-1])
            total_return = (final_value - initial_cash) / initial_cash * 100
            buy_hold = (float(df["收盘"].iloc[-1]) / float(df["收盘"].iloc[0]) - 1) * 100
            max_dd = ((pd.Series(portfolio) - pd.Series(portfolio).cummax()) / pd.Series(portfolio).cummax() * 100).min()

            trade_df = pd.DataFrame(trades) if trades else pd.DataFrame()
            sells = trade_df[trade_df["操作"] != "买入"] if len(trade_df) > 0 else pd.DataFrame()
            win_trades = len(sells[sells["盈亏%"] > 0]) if len(sells) > 0 else 0
            loss_trades = len(sells[sells["盈亏%"] <= 0]) if len(sells) > 0 else 0

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("最终资产", "¥{:,.0f}".format(final_value), "{:+.2f}%".format(total_return))
            c2.metric("策略收益", "{:.2f}%".format(total_return))
            c3.metric("买入持有收益", "{:.2f}%".format(buy_hold))
            c4.metric("最大回撤", "{:.2f}%".format(max_dd))

            c5, c6, c7 = st.columns(3)
            c5.metric("总交易笔数", str(len(trades)))
            c6.metric("盈利次数", str(win_trades))
            c7.metric("亏损次数", str(loss_trades))

            st.subheader("资金曲线")
            st.line_chart(pd.DataFrame({"资金曲线": portfolio}, index=df.index[1:]))

            st.subheader("收盘价与均线")
            chart = df[["收盘","MA_S","MA_L"]].copy()
            chart.columns = ["收盘","短期均线","长期均线"]
            st.line_chart(chart)

            st.subheader("RSI 指标")
            st.line_chart(df[["RSI"]])

            st.subheader("MACD 指标")
            st.line_chart(df[["MACD","Signal"]])

            if trades:
                st.subheader("交易记录 共" + str(len(trades)) + "笔")
                st.dataframe(pd.DataFrame(trades), use_container_width=True)
            else:
                st.warning("该时间段内没有触发交易信号")

else:
    st.subheader("选股筛选")
    codes_input = st.text_input("股票代码列表（逗号分隔）", value="600519.SS,600036.SS,000858.SZ,000001.SZ,601318.SS")
    col1, col2, col3 = st.columns(3)
    screen_start = col1.text_input("开始日期", value="2024-01-01")
    screen_end = col2.text_input("结束日期", value="2025-01-01")
    min_return = col3.number_input("最低涨幅(%)", value=-100.0, step=5.0)

    if st.button("开始筛选"):
        codes = [c.strip() for c in codes_input.split(",")]
        results = []
        progress = st.progress(0)
        status = st.empty()

        for idx, code in enumerate(codes):
            status.text("正在获取 " + code + "...")
            try:
                df = yf.download(code, start=screen_start, end=screen_end, progress=False)
                if len(df) < 30:
                    continue
                close = df["Close"].squeeze()
                ma5 = close.rolling(5).mean()
                ma20 = close.rolling(20).mean()
                delta = close.diff()
                gain = delta.clip(lower=0).rolling(14).mean()
                loss = -delta.clip(upper=0).rolling(14).mean()
                rsi = float((100 - 100 / (1 + gain / loss)).iloc[-1])
                total_ret = (float(close.iloc[-1]) / float(close.iloc[0]) - 1) * 100
                max_dd = float(((close - close.cummax()) / close.cummax()).min() * 100)
                results.append({
                    "代码": code,
                    "最新价": round(float(close.iloc[-1]), 2),
                    "区间涨幅%": round(total_ret, 2),
                    "最大回撤%": round(max_dd, 2),
                    "RSI": round(rsi, 1),
                    "价格>MA20": "是" if float(close.iloc[-1]) > float(ma20.iloc[-1]) else "否",
                    "MA5>MA20": "是" if float(ma5.iloc[-1]) > float(ma20.iloc[-1]) else "否",
                })
            except:
                pass
            progress.progress((idx+1) / len(codes))

        status.empty()
        if results:
            result_df = pd.DataFrame(results)
            filtered = result_df[result_df["区间涨幅%"] >= min_return]
            st.success("筛选完成，共" + str(len(filtered)) + "只符合条件")
            st.dataframe(filtered.sort_values("区间涨幅%", ascending=False), use_container_width=True)
            st.subheader("涨幅对比")
            st.bar_chart(result_df.set_index("代码")["区间涨幅%"])
        else:
            st.error("未获取到数据，请检查股票代码")