from flask import request

class HelperController:
    @classmethod
    def get_token_from_request(cls):
        token = request.headers['Authorization']
        fetched_token = token.split(" ")[1]
        return fetched_token
    
    @classmethod
    def query_database_details(cls, table, column, value):
        sql = """ SELECT * FROM {} WHERE {} = '{}'"""
        sql_command = sql.format(table, column, value)
        return sql_command

  
