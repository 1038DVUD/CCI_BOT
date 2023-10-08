import time
import pyupbit
import pandas as pd
import talib

# Upbit API 인증 정보 입력
access_key = 'cSaAhvgRaMwoIxFCdIFhkzxho0hyWxXXKhcgbHqy'
secret_key = 'I5B7wVUV24voI8I5sCH2yNKLdcjV1xFUHxTr793y'

# 매매할 가상화폐 선택 (멀티버스엑스 - EGLD)
symbol = 'KRW-ETH'  # 멀티버스엑스 (EGLD) / 한국 원화 (KRW)

# CCI 계산을 위한 데이터 차트 시간 간격과 기간 설정 (15분봉)
interval = 'minute60'
cci_period = 20

upbit = pyupbit.Upbit(access_key, secret_key)

# 백테스트 기간 설정 (2021년 1월 1일부터 2022년 12월 31일까지)
start_date = pd.Timestamp('2021-09-14')
end_date = pd.Timestamp('2021-11-15')

# 백테스트를 위한 과거 데이터 가져오기
df = pyupbit.get_ohlcv(symbol, interval=interval, to=end_date)

# CCI 지표 계산
cci = talib.CCI(df['high'], df['low'], df['close'], timeperiod=cci_period)

# 백테스트 결과 저장할 데이터프레임 생성
backtest_results = pd.DataFrame(index=df.index)
backtest_results['Close'] = df['close']
backtest_results['CCI'] = cci

# 매매 시그널과 수익률 계산
buy_signal = (backtest_results['CCI'] < -100).shift(1)  # CCI가 -100 미만이면 매수 신호
sell_signal = (backtest_results['CCI'] >= 100).shift(1)  # CCI가 100 이상이면 매도 신호

buy_price = None  # 매수 가격 초기화
total_profit_rate = 0.0  # 총 수익률 초기화

for i in range(len(backtest_results)):
    if buy_signal[i]:  # 매수 신호 발생 시
        if buy_price is None:  # 아직 매수하지 않은 경우에만 실행
            buy_price = backtest_results.iloc[i]['Close']

    elif sell_signal[i]:  # 매도 신호 발생 시
        if buy_price is not None:  # 이미 매수한 경우에만 실행
            sell_price = backtest_results.iloc[i]['Close']
            profit_rate = ((sell_price - buy_price) / buy_price) * 100.0
            total_profit_rate += profit_rate

            print(f"매도: {sell_price:.2f} KRW, 수익률: {profit_rate:.2f}%")

            buy_price = None  # 매도 후 매수 가격 초기화

# 총 수익률 출력
print(f"총 수익률: {total_profit_rate:.2f}%")
