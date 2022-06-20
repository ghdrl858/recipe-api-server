from http import HTTPStatus
from flask import request
from flask_restful import Resource
from mysql.connector.errors import Error
from mysql_connection import get_connection
import mysql.connector
from email_validator import validate_email, EmailNotValidError
from utils import hash_password

class UserRegisterResource(Resource) :
    def post(self) :
        
        # {
        #     "user_name": "홍길동",
        #     "email": "abc@naver.com",
        #     "password": "1234"
        # }

        # 1. 클라이언트가 body에 보내준 json을 받아온다.
        data = request.get_json()

        # 2. 이메일 주소형식이 제대로 된 주소형식인지 확인하는 코드 작성한다.
        try :
            validate_email(data['email'])

        except EmailNotValidError as e :
            print(str(e))
            return {"error" : str(e)}, 400

        # 3. 비밀번호의 길이가 유효한지 체크한다.
        # 비밀번호의 길이는 4자리 이상, 12자리 이하로만 받겠다.
        if len(data["password"]) < 4 or len(data["password"]) > 12 :
            return {"error" : "비밀번호 길이를 확인하세요."}, 400

        # 4. 비밀번호를 암호화한다.
        # data["password"]

        hashed_password = hash_password(data["password"])

        print(hashed_password)

        # 5. DB에 회원정보를 저장한다.
    
        try :
            # 데이터 insert
            # 1. DB에 연결
            connection = get_connection()

            # 2. 쿼리문 만들기
            query = '''insert into user
                    (username, email, password)
                    values
                    (%s, %s, %s);'''

            # %s에 맞게 튜플로 작성한다.
            record = (data['username'], data['email'], hashed_password)
            
            # 3. 커서를 가져온다.
            cursor = connection.cursor()

            # 4. 쿼리문을 커서를 이용해서 실행한다.
            cursor.execute(query, record)

            # 5. 커넥션을 커밋해줘야 한다. -> DB에 영구적으로 반영하라는 뜻
            connection.commit()

            # 6. 자원 해제
            cursor.close()
            connection.close()

        # 예외처리
        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {'error' : str(e)}, 503


        return {"result" : "success"}, 200
