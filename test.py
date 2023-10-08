import pyupbit

#로그인
access = "cSaAhvgRaMwoIxFCdIFhkzxho0hyWxXXKhcgbHqy"          # 본인 값으로 변경
secret = "I5B7wVUV24voI8I5sCH2yNKLdcjV1xFUHxTr793y"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

#잔고 조회
print(upbit.get_balance("KRW-MASK"))     # KRW-XRP 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회

