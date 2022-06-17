from http import HTTPStatus
from flask import request
from flask_restful import Resource
from mysql.connector.errors import Error
from mysql_connection import get_connection
import mysql.connector

# API를 만들기 위한 클래스 작성
# class(클래스) : 변수와 함수로 구성된 묶음이다.
# class는 상속이 가능하다.
# API를 만들기 위한 클래스는 flask_restful 라이브러리의 Resource class를 상속해서 만들어야한다.

class RecipeListResource(Resource) :
    # restful api의 method에 해당하는 함수를 작성한다.
    # callback 함수와 의미가 비슷하다.
    def post(self) :
        # api 실행 코드를 여기에 작성한다.
        # 클라이언트에서 body 부분에 작성한 json을 받아오는 코드
        data = request.get_json()

        # 받아온 데이터를 DB에 저장하면 된다.
        try :
            # 데이터 insert
            # 1. DB에 연결
            connection = get_connection()

            # 2. 쿼리문 만들기
            query = '''insert into recipe
                    (name, description, cook_time, directions)
                    values
                    (%s, %s, %s, %s);'''

            # %s에 맞게 튜플로 작성한다.
            record = (data['name'], data['description'], data['cook_time'], data['directions'])
            
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
            return {'error' : str(e)}, 503 # HTTPStatus.SERVICE_UNAVAILABLE

        return {'result' : 'success'}, 200 # 생략해도 200ok