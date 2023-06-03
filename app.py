from flask import Flask
from connector import Connector
app = Flask(__name__)

database = Connector()

@app.post("/api/user")
def create_user():
    return database.create_user()

@app.post("/api/eventType")
def create_event_type():
    return database.create_event_type()

@app.get("/api/users")
def fetch_users():
    return database.get_users()

@app.get("/api/<int:user_id>/events")
def fetch_events(user_id):
    return database.get_events(user_id)

@app.post("/api/<int:user_id>/updateUser")
def update_user(user_id):
    return database.update_user(user_id)

@app.post("/api/<int:event_id>/updateEvent")
def update_event(event_id):
    return database.update_event(event_id)

@app.post("/api/<int:event_type_id>/updateEventType")
def update_event_type(event_type_id):
    return database.update_event_type(event_type_id)