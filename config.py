# 환경설정
class Config :
    # 암호화 키
    JWT_SECRET_KEY = "yhacademy1029##heelo"
    JWT_ACCESS_TOKEN_EXPIRES = False
    # 예외처리를 JWT로 처리
    PROPAGATE_EXCEPTIONS = True