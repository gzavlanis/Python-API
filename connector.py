from flask import Flask, request
import os, psycopg2
from dotenv import load_dotenv
from helpers.queries import *

class Connector(object):
    # Singleton
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    
    def __init__(self):
        load_dotenv()
        url = os.environ.get('DATABASE_URL')
        try:
            self.connection = psycopg2.connect(url)
            print("Connection with Postgres was successfull")
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
        try:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(CREATE_USER, (username, password, firstname, lastname))
                    user_id = cursor.fetchone()[0]
            return {"id": user_id, "message": f"User {username} created."}, 201
        except Exception as error:
            print("Error:", error)
            return
    
    def create_event_type(self):
        data = request.get_json()
        name = data["name"]
        color = data["color"]
        description = data["description"]
        try:
            with self.connection as connection:
                with connection.cursor as cursor:
                    cursor.execute(CREATE_EVENT_TYPE, (name, color, description))
            return {"message": f"Event type {name} added."}, 201
        except Exception as error:
            print("Error:", error)
            return

    def create_event(self, user_id):
        data = request.get_json()
        title = data["title"]
        start_time = data["start_time"]
        end_time = data["end_time"]
        description = data["description"]
        if title == None:
            print("Title is required.")
            return
        try:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(CREATE_EVENT, (title, start_time, end_time, description, user_id))
            return {"message": f"Event {title} created."}, 201
        except Exception as error:
            print("Error:", error)
            return
    
    def get_users(self):
        try:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(GET_ALL_USERS)
                    users = cursor.fetchall()
            return users
        except Exception as error:
            print("Error:", error)
            return
    
    def get_events(self, user_id):
        if user_id is None:
            print("User id is required!")
            return
        else:
            try:
                with self.connection as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(GET_EVENTS, (user_id))
                        events = cursor.fetchall()
                return events
            except Exception as error:
                print("Error:", error)
                return
    
    def update_user(self, user_id):
        if user_id is None:
            print("User id is required!")
            return
        else:
            data = request.get_json()
            username = data["username"]
            password = data["password"]
            firstname = data["firstname"]
            lastname = data["lastname"]
            if username == None or password == None or firstname == None or lastname == None:
                print("You have empty fields! Try again.")
                return
            else:
                with self.connection as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(CREATE_USER, (username, password, firstname, lastname))
                        user_id = cursor.fetchone()[0]
                return {"id": user_id, "message": f"User {username} updated."}, 201
        
    def update_event(self, event_id):
        if event_id is None:
            print("User id is required!")
            return
        data = request.get_json()
        title = data["title"]
        start_time = data["start_time"]
        end_time = data["end_time"]
        description = data["description"]
        if title == None:
            print("Title of the event is required.") 
            return
        else:
            try:
                with self.connection as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(CREATE_EVENT, (title, start_time, end_time, description, event_id))
                return {"message": f"Event {title} updated."}, 201
            except Exception as error:
                print("Error:", error)
                return
            
    def update_event_type(self, event_type_id):
        if event_type_id is None:
            print("User id is required!")
            return
        data = request.get_json()
        title = data["title"]
        color = data["color"]
        description = data["description"]
        if title == None or color == None:
            print("There are missing fields. try again")
            return
        else:
            try:
                with self.connection as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(CREATE_EVENT, (title, color, description, event_type_id))
                return {"message": f"Event {title} created."}, 201
            except Exception as error:
                print("Error:", error)
                return
              