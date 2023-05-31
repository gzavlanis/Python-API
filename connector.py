from flask import Flask, request
import os, psycopg2
from dotenv import load_dotenv

class Connector(object):
    # Singleton
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    
    def __init__(self):
        load_dotenv()
        # app = Flask(__name__)
        url = os.environ.get('DATABASE_URL')
        try:
            self.connection = psycopg2.connect(url)
        except Exception as error:
            print("Error:", error)
            self.connection = psycopg2.connect(url)
            print("Connection was restored.")

    def create_user(self):
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        firstname = data["firstname"]
        lastname = data["lastname"]
        with self.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_USER, (username, password, firstname, lastname))
                user_id = cursor.fetchone()[0]
        return {"id": user_id, "message": f"User {username} created."}, 201
    
    def create_event_type(self):
        data = request.get_json()
        name = data["name"]
        color = data["color"]
        description = data["description"]
        with self.connection as connection:
            with connection.cursor as cursor:
                cursor.execute(CREATE_EVENT_TYPE, (name, color, description))
        return {"message": f"Event type {name} added."}, 201

    def create_event(self):
        return       
    