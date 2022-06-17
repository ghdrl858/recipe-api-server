import mysql.connector

def get_connection() :
    connection = mysql.connector.connect(
        host = 'yh-db.cmb3i3z0gn3a.ap-northeast-2.rds.amazonaws.com',
        database = 'recipe_db',
        user = 'recipe_user',
        password = 'recipe1234'
    )
    return connection