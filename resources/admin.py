from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query
import datetime

class Admin(Resource):
    def __init__(self, id, password):
        self.id=id
        self.password=password
    @classmethod
    def getAdminById(cls, id):
        result= query(f"""Select id, password from admin where id='{id}'""", return_json=False)
        if len(result)>0:
            return Admin(result[0]['id'], result[0]['password']) 
            
        return None

class AdminLogin(Resource):
    def post(self):
        parser= reqparse.RequestParser()
        parser.add_argument('id',type=int,required=True,help="ID cannot be  blank!")
        parser.add_argument('password',type=str,required=True,help="Password cannot be  blank!")
        data=parser.parse_args()
        admin1= Admin.getAdminById(data['id'])
        if(admin1 and safe_str_cmp(admin1.password,data['password'])):
            access_token=create_access_token(identity=admin1.id,expires_delta=False)
            return {'access_token':access_token},200
        else:
            return {"message": "Invalid credentials"}



class DenyAuthorisation(Resource):
    @jwt_required
    def post(self):
        parser= reqparse.RequestParser()
        parser.add_argument('event_id',type=int,required=True,help="ID cannot be  blank!")
        parser.add_argument('event_name',type=str,required=True,help="event name cannot be  blank!")
        data= parser.parse_args()

        try:
            query(f"""update eventregister set allow=0 
            where event_id= '{data['event_id']}' and event_name='{data['event_name']}' """)
            return {"message":"Event Authorisation denied"}
        except:
            return {"message":"Couldn't access the table"}


