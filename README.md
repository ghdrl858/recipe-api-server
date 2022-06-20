# recipe-api-server

- 파이썬을 이용한 다양한 기능의 recipe API

- app.py : 메인화면
- mysql_conncection.py : mysql를 사용가능하게 파이썬으로 불러오기
- test.py : test 기능
- config.py : 환경설정(암호화키, 토큰 등등)

< resources 폴더 >
 - recipe.py : 입력하기 및 목록가져오기
 - recipe_info.py : id로 정보 가져오기, 데이터 업데이트하기 및 삭제하기
 - recipe_publish.py : 공개설정 및 임시저장하기
 - user.py : 비밀번호 암호화 기능 및 이메일 기능 작업하기

  ! id 숫자 초기화 - 테이블 - 옵션 - auto increment에서 수정