import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="2026 전략 투자 대시보드", layout="wide")

st.title("📊 2026 핵심 투자 지표 대시보드")
st.markdown("---")

# 2. 데이터 가져오기 함수
def get_indicators():
    try:
        # 1d 대신 5d(5일치)를 가져오면 주말이라도 금요일 데이터를 찾을 수 있습니다.
        vix_data = yf.Ticker("^VIX").history(period="5d")
        vix = vix_data['Close'].iloc[-1] if not vix_data.empty else 0
        
        # 하이일드 스프레드 (고정치 또는 FRED 연동)
        hys = 2.81 # 2026년 1월 기준 예시 수치
        
        # 버핏 지수 계산 (시장 전체 시총 대용으로 S&P 500 지수 활용 권장)
        # ^W5000이 안될 경우 ^GSPC(S&P 500)를 사용해 보세요.
        mcap_data = yf.Ticker("^GSPC").history(period="5d")
        if not mcap_data.empty:
            last_price = mcap_data['Close'].iloc[-1]
            # 버핏 지수는 실제 GDP 대비 시총이라 수동 업데이트가 더 정확할 수 있습니다.
            buffett_idx = (last_price / 2500) * 100 # 임시 계산식
        else:
            buffett_idx = 230.0 # 데이터 없을 때 기본 과열 수치 표시
            
        return vix, hys, buffett_idx
    except Exception as e:
        # 에러 발생 시 프로그램이 멈추지 않고 0을 반환하게 함
        return 0, 0, 0

vix, hys, b_idx = get_indicators()

# 3. 상단 지표 요약 (Metric)
col1, col2, col3, col4 = st.columns(4)
col1.metric("VIX (공포지수)", f"{vix:.2f}", "-1.2%")
col2.metric("하이일드 스프레드", f"{hys}%", "0.05%")
col3.metric("버핏 지수", f"{b_idx:.1f}%", "과열")
col4.metric("공탐 지수", "45", "Neutral")

st.markdown("---")

# 4. 섹션 분할 (차트 및 전략)
left_col, right_col = st.columns([2, 1])

    
# 공포와 탐욕 지수 외부 링크
st.link_button("CNN Fear & Greed 확인하기", "https://edition.cnn.com/markets/fear-and-greed")
