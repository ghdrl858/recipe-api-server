from http import HTTPStatus
from flask import Response, request
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

    # 가져오기
    def get(self) :
        # 쿼리 스트링으로 오는 데이터는 아래처럼 처리해준다.
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        # DB로부터 데이터를 받아서, 클라이언트에 보내준다.
        try :
            connection = get_connection()

            query = '''select * 
                    from recipe
                    limit ''' +offset+''', '''+limit+''';'''

            # select문은 dictionary = True를 해준다.
            cursor = connection.cursor(dictionary = True)

            cursor.execute(query)

            # select문은 아래 함수를 이용해서 데이터를 가져온다.
            result_list = cursor.fetchall()

            print(result_list)

            # 중요 ! DB에서 가져온 timestamp는 파이썬의 datetime으로 자동 변경된다.
            # 문제는 이 데이터를 json으로 바로 보낼 수 없으므로 문자열로 바꿔서 다시 저장시킨 후 보낸다.
            i=0
            for record in result_list :
                result_list[i]['created_at'] = record['created_at'].isoformat()
                result_list[i]['update_at'] = record['update_at'].isoformat()
                i = i+1

            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"error" : str(e)}, 503

        return {"result" : "success",
                "count" : len(result_list),
                "result_list" : result_list}, 200