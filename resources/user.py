from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query

class User(Resource):
    def __init__(self, user_id, name, password, branch):
        self.user_id=user_id
        self.name= name
        self.password= password
        self.branch=branch

    @classmethod
    def getUserById(cls, user_id):
        result= query(f"""Select user_id, name, branch, password from user where user_id='{user_id}'""", return_json=False)
        if len(result)>0:
            return User(result[0]['user_id'], result[0]['name'], 
            result[0]['password'], result[0]['branch'])
        return None

class UserRegister(Resource):
    def post(self):
        parser= reqparse.RequestParser()
        parser.add_argument('user_id',type=int,required=True,help="ID cannot be  blank!")
        parser.add_argument('name',type=str,required=True,help="username cannot be  blank!")
        parser.add_argument('branch',type=str,required=True,help="branch cannot be left blank!")
        parser.add_argument('password',type=str,required=True,help="Password cannot be  blank!")
        data=parser.parse_args()
        if User.getUserById(data['user_id']):
            return {"message":"User already exists"}, 400
        try:
            query(f"""insert into user values('{data['user_id']}',
            '{data['name']}','{data['password']}', '{data['branch']}')""")
        except:
            return {"message": "An error occurred while registering."}, 500
        return {"message": "User created successfully."}, 201


class UserLogin(Resource):
    def post(self):
        parser= reqparse.RequestParser()
        parser.add_argument('user_id',type=int,required=True,help="ID cannot be  blank!")
        parser.add_argument('password',type=str,required=True,help="Password cannot be  blank!")
        data=parser.parse_args()
        user1= User.getUserById(data['user_id'])
        if(user1 and safe_str_cmp(user1.password,data['password'])):
            access_token=create_access_token(identity=user1.user_id,expires_delta=False)
            return {'access_token':access_token},200
        else:
            return {"message": "Invalid credentials"}


                





    