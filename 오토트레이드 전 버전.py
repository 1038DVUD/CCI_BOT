import time
import pyupbit
import talib
from slack_sdk import WebClient
# Slack API Token
slack_api_token = 'xoxb-5962399874407-5970441637446-QLrtFoZ5pRmELQhwAYHbMTzx'
slack_channel = '#stock'  # 메시지를 보낼 채널명
# Upbit API 인증 정보 입력
access_key = 'cSaAhvgRaMwoIxFCdIFhkzxho0hyWxXXKhcgbHqy'
secret_key = 'I5B7wVUV24voI8I5sCH2yNKLdcjV1xFUHxTr793y'
# Slack 클라이언트 초기화
slack_client = WebClient(token=slack_api_token)
# 매매할 가상화폐 선택 (멀티버스엑스 - EGLD)
symbol = 'KRW-STMX'  # 멀티버스엑스 (EGLD) / 한국 원화 (KRW)
# CCI 계산을 위한 데이터 차트 시간 간격과 기간 설정 (15분봉)
interval = 'minute5'
cci_period = 20
upbit = pyupbit.Upbit(access_key, secret_key)
# 이전 매수 가격 초기화
buy_price = None
# 매수 주문 상태 초기화
buy_order_executed = 0
# 이전 매수 주문 시각 초기화
last_buy_time = None
# 자동매매 시작 메시지 Slack으로 보내기
slack_client.chat_postMessage(
    channel=slack_channel,
    text="자동매매 시작"
)
print("자동매매 시작")
while True:
    current_time = time.localtime()
    if current_time.tm_min % 5 == 0:
        try:
            # 최근 데이터 불러오기
            df = pyupbit.get_ohlcv(symbol, interval=interval, count=cci_period)
            # CCI 지표 계산
            cci = talib.CCI(df['high'], df['low'], df['close'], timeperiod=cci_period)
            # 이전 15분봉의 CCI 값을 가져오려면 마지막 값(-1)을 사용합니다.
            previous_cci = cci.iloc[-2]  # -1은 현재 봉의 CCI, -2는 이전 봉의 CCI
            # 최근 CCI 값 가져오기
            current_cci = cci.iloc[-1]
            # 현재 시간 기록
            current_time = time.time()
            # 매수 조건에서 KRW 잔고 초기화
            krw_balance = upbit.get_balance("KRW")
            slack_client.chat_postMessage(
                channel=slack_channel,
                text=f"5분,이전CCI: {previous_cci}, 현재CCI: {current_cci}"
            )
            # 매수 조건
            if previous_cci < -100 and current_cci > -100 and krw_balance > 6000 and buy_order_executed < 3 and (last_buy_time is None or (current_time - last_buy_time) >= 600): # 원래값 1800
                # 매수 조건에서 실제 KRW 잔고를 기반으로 매수하도록 수정
                # KRW 잔고의 60분에 1 만큼 매수
                buy_amount = krw_balance / 60
                upbit.buy_market_order(symbol, buy_amount)
                buy_price = pyupbit.get_current_price(symbol)
                last_buy_time = current_time
                buy_order_executed += 1  # 매수 주문 실행 횟수 증가
                message = f"{buy_order_executed}번째 매수 주문 실행 - CCI: {current_cci}"
                slack_client.chat_postMessage(
                    channel=slack_channel,
                    text=message
                )
               # krw_balance = upbit.get_balance("KRW")
            # 매도 조건
            if previous_cci >= 100 and current_cci <= 100:
                current_price = pyupbit.get_current_price(symbol)
                slack_client.chat_postMessage(
                    channel=slack_channel,
                    text="이전 CCI 100 진입 현재 CCI 100 하향돌파"
                )
                profit_rate = ((current_price - buy_price) / buy_price) * 100
                upbit.sell_market_order(symbol, upbit.get_balance(symbol))
                message = f"매도 주문 실행 - CCI: {current_cci}, 수익률: {profit_rate:.2f}%"
                slack_client.chat_postMessage(
                    channel=slack_channel,
                    text=message
                )
                # 매도 후 buy_order_executed 초기화
                buy_order_executed = 0
        except Exception as e:
            error_message = f"에러 발생: {e}"
            slack_client.chat_postMessage(
                channel=slack_channel,
                text=error_message
            )
    time.sleep(30)