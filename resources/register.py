from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query
from .user import *
from .events import *

class UserRegisterEvent(Resource):
    def post(self):
        parser= reqparse.RequestParser()
        parser.add_argument('user_id',type=int,required=True,help="ID cannot be  blank!")
        parser.add_argument('password',type=str,required=True,help="Password cannot be  blank!")
        parser.add_argument('event_id',type=int,required=True,help="ID cannot be  blank!")
        parser.add_argument('event_name',type=str,required=True,help="event name cannot be  blank!")
        data=parser.parse_args()
        user1= User.getUserById(data['user_id']) 
        event1=Events.getEventById('event_id')
        if user1 and safe_str_cmp(user1.password, data['password']) and event1:
            if event1.allow==1:
                query(f"""insert into userregister values('{data['event_id']}', '{data['event_name']}','{data['user_id']}')""")
                return{"message":"Value inserted"}
            else:
                return{"message":"Event does not exist"}
        else:
            return{"message":"User does not exist"}








