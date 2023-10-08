import pyupbit
import talib

# 매매할 가상화폐 선택
symbol = 'KRW-BTC'  # 비트코인 / 한국 원화

# CCI 계산을 위한 데이터 차트 시간 간격과 기간 설정 (일봉)
interval = 'minute5'
cci_period = 20  # 일반적으로 CCI 계산 시 14일 기간을 사용합니다.

# 최근 데이터 불러오기
df = pyupbit.get_ohlcv(symbol, interval=interval, count=cci_period + 20)

# CCI 지표 계산
cci = talib.CCI(df['high'], df['low'], df['close'], timeperiod=cci_period)

print(cci)