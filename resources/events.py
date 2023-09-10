from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query
from .user import *
import datetime

class Events(Resource):
    def __init__(self, event_id, event_name, event_details, head, certificate, allow, event_date):
        self.event_id=event_id
        self.event_name=event_name
        self.event_details=event_details
        self.head=head
        self.certificate=certificate
        self.allow=allow
        self.event_date=event_date

    @classmethod
    def getEventById(cls, event_id):
        result= query(f"""select event_id, event_name, event_details, head, certificate, allow, event_date
         from eventregister where allow=1 and 
        event_id='{event_id}'""", return_json=False)
        if result:
            return Events(result[0]['event_id'],result[0]['event_name'],
                result[0]['event_details'],result[0]['head'], result[0]['certificate'], result[0]['allow'], result[0]['event_date'])
        return None


class EventRegister(Resource):
    def post(self):
        parser= reqparse.RequestParser()
        parser.add_argument('event_id',type=int,required=True,help="ID cannot be  blank!")
        parser.add_argument('event_name',type=str,required=True,help="event name cannot be  blank!")
        parser.add_argument('event_details',type=str,required=True,help="branch cannot be left blank!")
        parser.add_argument('head',type=str,required=True,help="Head name cannot be  blank!")
        parser.add_argument('certificate',type=str,required=True,help="Certificate cannot be  blank!")
        parser.add_argument('allow',type=int)
        parser.add_argument('event_date',type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),required=True,help="date cannot be left blank!")
        
        data=parser.parse_args()
        event1= Events.getEventById(data['event_id'])
        if event1:
            return {"message":"Event with those credentials exists"}
        try:
            query(f"""Insert into eventregister values('{data['event_id']}',
            '{data['event_name']}', '{data['event_details']}', 
            '{data['head']}', '{data['certificate']}', '{data['allow']}', '{data['event_date']}')""")
        except:
            return {"message": "There was an error connecting to eventregister table"}, 500

class AllApprovedEvents(Resource):
    @jwt_required
    def get(self):
        try:
            return query("""Select event_id, event_name, event_details, head, certificate, allow, event_date from 
        eventregister where allow=1""")
        except:
            return {"message": "couldn't show all events"}




