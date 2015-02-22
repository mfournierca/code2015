import flask
import psycopg2


def connect_db():
    return psycopg2.connect(
        database="code2015", user="app_user", password="app_user_password")


