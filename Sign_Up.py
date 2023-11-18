#POST METHOD:
#       URL: BASE + "/Sign_up/<Password>/<First_name>/<Last_name>". + form containing 'Email' (full form of email including "@")
#GET METHOD:
#       URL: BASE + "/Sign_up" + form  containing 'Email' (''''')
#PATCH METHOD:
#       URL: BASE + "/Sign_up" + form containing 'Email' ('''') + 'Attribute' (Field you wish to change, pay attention to spelling of the fields) + 'Info' (what you wish to place in the field)
#DELETE METHOD:
#       URL: BASE + "/Sign_up" + form containing 'Email" (all ordered in forms)
from flask import Flask, make_response
from flask_restful import Api, Resource, reqparse, abort
from DB import *

app = Flask(__name__)
api = Api(app)

us_Acc_info = reqparse.RequestParser()
us_Acc_info.add_argument("Email", type=str, help="Enter Email", required = True)
us_Acc_info.add_argument("Attribute", type=str, help="Enter attribute", required = False)
us_Acc_info.add_argument("Info", type=str, help="Enter info", required = False)

class Sign_Up(Resource):

    def post(self, Password, First_name, Last_name):
        args = us_Acc_info.parse_args()
        Email = args["Email"]
        if (is_Email_Taken(Email)):
            abort(409,message="Email Taken")
        insert_New_User(Email, Password, First_name, Last_name)
        return {"Completed": 201}
api.add_resource(Sign_Up, "/Sign_up/<string:Password>/<string:First_name>/<string:Last_name>")

class Change(Resource):
    def get(self):
        args = us_Acc_info.parse_args()
        Email = args["Email"]
        if not(is_Email_Taken(Email)):
            abort("User doesnt exist.")
        return {"Information": get_User(Email)}

    def patch(self):
        args = us_Acc_info.parse_args()
        Email = args["Email"]
        if (update_User(Email,args["Attribute"],args["Info"]) == False):
            abort(404, message="User not found.")
        update_User(Email,args["Attribute"],args["Info"])
        return {"Completed": 201}

    def delete(self):
        args = us_Acc_info.parse_args()
        Email = args["Email"]
        if not(is_Email_Taken(Email)):
            abort(404, message="User not found.")
        delete_User(Email)
        return {"Completed":201}

api.add_resource(Change, "/Sign_up")

if __name__ == "__main__":
    app.run(debug=True)

